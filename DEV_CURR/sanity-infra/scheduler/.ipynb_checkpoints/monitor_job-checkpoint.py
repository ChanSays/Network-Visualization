from ats.topology import Testbed, Device, Interface, Link
import unicon
import time
import argparse
from datetime import datetime
import sys
import os
from pathlib import Path
from utils.dbconnect import DBConnect
from utils.logger import Logger
from utils.j2 import J2Env
from utils.mailer import Mailer

log = Logger(__name__)


class MonitorJob:
    """
    Monitor invoked job
    """

    job = None
    device = None
    itgen = None
    email = None

    def __init__(self, submit_id=None, email=None):
        """ get all running jobs as named tuple
        """
        if submit_id is None:
            log.error("Submit id is None")
            sys.exit(-1)
        try:
            dbcon = DBConnect()
            job_cmd = """ select * from submitted_jobs where submit_id={0}""".format(submit_id)
            complete_job_data = dbcon.fetch(job_cmd, type="_tuple")
            self.job = complete_job_data[0]
            log.info("Monitoring the job: " + repr(self.job))
            testbed_cmd = """select * from testbeds where testbed='{0}'""".format(self.job.testbed)
            testbed_cmd_data = dbcon.fetch(testbed_cmd, type="_tuple")
            self.testbed = testbed_cmd_data[0]
            self.job_log_dir = """/vol/eor-qa/sanity/logs/{0}/{1}""".format(self.job.submitter, self.job.submit_id)

            self.email = email
            if email is None:
                self.email = self.job.submitter
        except Exception as e:
            log.error("Monitor job failed:"+repr(e))
            sys.exit(-1)
        finally:
            dbcon.close_connection()

    def init_device_connector(self):
        self.device = Device('iTgen',
                        os='linux',
                        type='linux',
                        tacacs={'username': 'root'},
                        passwords={'linux': 'insieme', 'line': 'lab', 'tacacs': 'lab', 'enable': 'lab'},
                        connections={
                            'defaults': {'class': unicon.Unicon},
                            'cli': {
                                'protocol': 'ssh',
                                'ip': '{0}'.format(self.testbed.itgen_ip),
                            }
                        })
        testbed_itgen = Testbed('manualtestbed')
        self.device.testbed = testbed_itgen
        self.itgen = testbed_itgen.devices['iTgen']

    def send_email(self, subject="Finished" ,reason="Sanity Job Completed"):
        try:
            dir_path = "/tmp"
            email_to = self.email
            input_dict = {}
            input_dict["submitter"] = self.job.submitter
            input_dict["submit_id"] = self.job.submit_id
            input_dict["status"] = subject
            input_dict["reason"] = "{0} on testbed {1}".format(reason, self.job.testbed)

            subject = "N9k Sanity Job {0} Status: {1}".format(self.job.submit_id, subject)

            j2env = J2Env()

            template_file = 'job_submission_email.html'
            out_file = "{0}/{1}".format(dir_path, "req_creation_mail.html")
            # print(out_file)
            j2env.create_file(template_file, input_dict, out_file)
            mailer = Mailer(email_to)
            mailer.send_html_mail(subject, out_file)
        except BaseException as e:
            log.error("Exception in send mail:"+repr(e))

    def check_job(self):
        """ is the job running in the itgen server?
            is the time limit exceeded ? """
        try:
            log.info("ssh into itgen server and check pid")
            self.itgen.connect(alias='cli', via='cli')
            pid_list = self.itgen.cli.execute("ps aux | grep '[/]basic_sanity'")
            pid_list = pid_list.splitlines()
            log.info("pid list :"+repr(pid_list))

            # if len < 1, basic_sanity is not running
            if (len(pid_list) < 1):
                results = "job was deleted, pid not found in iTgen server"
                self.delete_job_from_db(self.job, results)
                return True

            # check run time
            now = datetime.now()
            diff = now - self.job.start_time
            diff = diff.total_seconds() / 60
            if diff > self.job.eta:
                # kill all pid's (usually one for screen and one for python),
                for py_pid in pid_list:
                    pid = py_pid.spit()[1]
                    self.itgen.cli.execute("kill {0}".format(pid))
                results = "job was aborted for exceeding time limit"
                self.delete_job_from_db(self.job, results)
                self.send_email(subject="Aborted", reason=results)
                return True
            return False
        except Exception as e:
            log.error("Monitor Job failed:"+repr(e))
            sys.exit(-1)
        finally:
            self.itgen.disconnect()

    def check_reports(self):
        report_file = "{0}/{1}-{2}.report".format(self.job_log_dir, self.job.testsuite, self.job.testbed)
        log.info("checking for report file: {0}".format(report_file))
        if os.path.exists(report_file) and os.path.isfile(report_file):
            report = Path(report_file).read_text()
            if report == "":
                report = "Report file was empty. Please check the logs"
            return report
        return None

    def delete_job_from_db(self, job, results):
        """ delete the job """
        status = "deleted"
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        report = self.check_reports()
        if report is not None:
            status = 'completed'
            results = report
        try:
            dbcon = DBConnect()
            # free testbed
            tbstatus_cmd = """ update testbeds set status='free' where testbed='{0}'; """.format(job.testbed)
            dbcon.execute(tbstatus_cmd)

            # remove job from submitted job
            delete_cmd = """ delete from submitted_jobs where submit_id={0}
                             """.format(job.submit_id)
            dbcon.execute(delete_cmd)
            # insert into accepted queue
            insert_sql_str = """ INSERT INTO completed_jobs (submit_id, submit_date, submitter, build, testsuite,
                                 asic, testbed, priority, eta, status, status_date, start_time, end_time, results, logs,
                                 flags, final_image_path, final_issu_image_path, scheduled_testsuite) VALUES (
                                 {submit_id}, '{submit_date}', '{submitter}', '{build}', '{testsuite}', '{asic}',
                                 '{testbed}', {priority}, {eta}, '{status}', '{status_date}', '{start_time}',
                                 '{end_time}', '{results}', '{logs}', '{flags}', '{final_image_path}',
                                 '{final_issu_image_path}', '{scheduled_testsuite}'); """
            insert_sql_str = insert_sql_str.format(submit_id=self.job.submit_id,
                                                   submit_date=self.job.submit_date,
                                                   submitter=self.job.submitter,
                                                   build=self.job.build,
                                                   testsuite=self.job.testsuite,
                                                   asic=self.job.asic,
                                                   testbed=self.job.testbed,
                                                   priority=self.job.priority,
                                                   eta=self.job.eta,
                                                   status=status,
                                                   status_date=now,
                                                   start_time=self.job.start_time,
                                                   end_time=now,
                                                   results=results,
                                                   logs=self.job_log_dir,
                                                   flags=self.job.flags,
                                                   final_image_path=self.job.final_image_path,
                                                   final_issu_image_path=self.job.final_issu_image_path,
                                                   scheduled_testsuite=self.job.scheduled_testsuite
                                                   )
            dbcon.execute(insert_sql_str)
        except Exception as e:
            print("HealthMonitor failed:"+repr(e))
            sys.exit(-1)
        finally:
            dbcon.close_connection()

    def monitor_job(self):
        self.init_device_connector()
        while True:
            status = self.check_job()
            if status:
                break
            # sleep for 2 minutes
            time.sleep(120)
        log.info("Monitor Job finished executing")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--submit_id')
    args = parser.parse_args()

    submit_id = args.submit_id or None
    if submit_id is None:
        log.error("Error in stage, submit_id is None. Exiting..")
        sys.exit(-1)

    log.info("Starting monitor_job for job:{0}".format(submit_id))
    monitor = MonitorJob(submit_id)
    monitor.monitor_job()


if __name__ == "__main__":
    main()
