""" Submit job stage. Validate and accept job into job queue """

import argparse
from datetime import datetime
import sys
import logging
from utils.dbconnect import DBConnect
from utils.j2 import J2Env
from utils.mailer import Mailer
from submitter.validator import Validator
from submitter.setup_data import SetupJobData
from utils.logger import Logger
from utils import constants

log = Logger(__name__)
log.setup_log(console_level=logging.DEBUG)


class Submitter:
    params = None

    def __init__(self, args):
        self.params = {}
        self.params["submitter"] = args.submitter
        self.params["build"] = args.build or ""
        self.params["testsuite"] = args.testsuite
        self.params["asic"] = args.asic or ""
        self.params["testbed"] = args.testbed or ""
        self.params["basemode"] = args.basemode or 0
        self.params["dockermode"] = args.dockermode or 0
        self.params["containermode"] = args.containermode or 0
        self.params["issu_build_srcdir"] = args.issu_build_srcdir or ""
        self.params["download_image"] = args.download_image or ""
        self.params["mparams"] = args.mparams or ""
        self.params["stopOnFail"] = args.stopOnFail or 0
        self.params["pauseOnFail"] = args.pauseOnFail or 0
        self.params["newChange"] = args.stopOnFail or 0
        self.params["download_only"] = args.download_only or 0
        self.params["email"] = args.email or ""
        self.params["send_updates"] = args.email or 0

    def abort_submission(self, reason=None):
        '''
        abort a submission
        '''
        if reason is None:
            reason = "Unexpected error occurred in submit job stage"
        try:
            dbcon = DBConnect()
            abort_cmd = """ delete from submitted_jobs where submit_id={0} """.format(self.params["submit_id"])
            dbcon.execute(abort_cmd)
            # insert into accepted queue
            insert_sql_str = """ INSERT INTO completed_jobs (submit_id, submit_date, submitter, build, testsuite, asic,
                                 testbed, priority, status, status_date, results, flags) VALUES ( {submit_id},
                                 '{submit_date}', '{submitter}', '{build}', '{testsuite}', '{asic}', '{testbed}',
                                 {priority}, '{status}', '{status_date}', '{results}', '{flags}'); """
            insert_sql_str = insert_sql_str.format(submit_id=self.params["submit_id"],
                                                   submit_date=self.params["now"],
                                                   submitter=self.params["submitter"],
                                                   build=self.params["build"],
                                                   testsuite=self.params["testsuite"],
                                                   asic=self.params["asic"],
                                                   testbed=self.params["testbed"],
                                                   priority=self.params["priority"],
                                                   status='aborted',
                                                   status_date=self.params["now"],
                                                   results=reason,
                                                   flags=self.params["flags"])
            dbcon.execute(insert_sql_str)
        except Exception as e:
            log.error("error occured in submit job:abort_submission" + repr(e))
            sys.exit(-1)
        finally:
            dbcon.close_connection()


    def record_job_submission(self):
        """ Record the job submission as a row in submitted_jobs """
        try:
            self.params["now"] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            dbcon = DBConnect()
            self.params["priority"] = 6
            if self.params["submitter"] == "snoopy":
                self.params["priority"] = 1

            get_flag_details = " select * from flag_details;"
            flag_details = dbcon.fetch(get_flag_details, type="_tuple")
            submitted_flags = ""
            for flag_detail in flag_details:
                flag_id = flag_detail.flag_id
                flag_value = self.params[flag_detail.flag_name]
                submitted_flags = "{0}={1},{2}".format(flag_id, flag_value, submitted_flags)
            self.params["flags"] = submitted_flags

            # insert into accepted queue
            insert_sql_str = """ INSERT INTO submitted_jobs 
                                 (submit_date, submitter, build, testsuite, asic, testbed, priority,
                                 status_date, flags, send_updates) VALUES 
                                 ( '{submit_date}', '{submitter}', '{build}', '{testsuite}', 
                                 '{asic}', '{testbed}', {priority}, '{status_date}', '{flags}', {send_updates}); """
            insert_sql_str = insert_sql_str.format(submit_date=self.params["now"],
                                                   submitter=self.params["submitter"],
                                                   build=self.params["build"],
                                                   testsuite=self.params["testsuite"],
                                                   asic=self.params["asic"],
                                                   testbed=self.params["testbed"],
                                                   priority=self.params["priority"],
                                                   status_date=self.params["now"],
                                                   flags=self.params["flags"],
                                                   send_updates=self.params["send_updates"])
            dbcon.execute(insert_sql_str)
            # get the submit id from last insert
            submit_id = dbcon.fetch("SELECT LAST_INSERT_ID();")[0][0]
            self.params["submit_id"] = submit_id
            log.debug("Job was recorded into submitted_jobs table with submit_id:{0}".format(submit_id))
        except Exception as e:
            log.error("error occured in submit job:record_job_submission" + repr(e))
            self.abort_submission()
        finally:
            dbcon.close_connection()

    def accept_job(self):
        """ accept the job and add it to appropriate table. """
        try:
            dbcon = DBConnect()

            # get eta from testsuites table
            suite_data_cmd = "select eta from testsuites where testsuite='{0}';".format(
                self.params["testsuite"])
            suite_data = dbcon.fetch(suite_data_cmd)
            self.params["eta"] = suite_data[0][0]

            update_eta = """ update submitted_jobs set eta='{eta}' where submit_id='{submit_id}' """
            update_eta = update_eta.format(eta=self.params["eta"],
                                           submit_id=self.params["submit_id"])
            dbcon.execute(update_eta)

            # Mark job as completed if download_only flag set
            if self.params["download_only"] == constants.DOWNLOAD_ONLY:
                results = "download_only flag is set. Files were downloaded and job was marked complete"
                # insert into accepted queue
                insert_sql_str = """ INSERT INTO completed_jobs (submit_id, submit_date, submitter, build, testsuite,
                                     asic, testbed, priority, status, status_date, results, flags) VALUES ( {submit_id},
                                     '{submit_date}', '{submitter}', '{build}', '{testsuite}', '{asic}', '{testbed}',
                                     {priority}, '{status}', '{status_date}', '{results}', '{flags}'); """
                insert_sql_str = insert_sql_str.format(submit_id=self.params["submit_id"],
                                                       submit_date=self.params["now"],
                                                       submitter=self.params["submitter"],
                                                       build=self.params["build"],
                                                       testsuite=self.params["testsuite"],
                                                       asic=self.params["asic"],
                                                       testbed=self.params["testbed"],
                                                       priority=self.params["priority"],
                                                       status='completed',
                                                       status_date=self.params["now"],
                                                       results=results,
                                                       flags=self.params["flags"])
                dbcon.execute(insert_sql_str)
            log.info("Job submitted successfully, submit_id is {0}".format(self.params["submit_id"]))
        except Exception as e:
            log.error("error occured in submit job: accept_validated_job" + repr(e))
            self.abort_submission()
        finally:
            dbcon.close_connection()

    def send_email(self, subject="Submitted" ,reason="Job submission successful"):
        try:
            dir_path = "/tmp"
            email_list = self.params["email"].replace(" ", "")
            email_to = "{0}@cisco.com".format(self.params["submitter"])
            for email in email_list.split(','):
                if email == "":
                    continue
                if not email.endswith("@cisco.com"):
                    email += "@cisco.com"
                email_to = "{0},{1}".format(email_to, email)
            input_dict = {}
            input_dict["submitter"] = self.params["submitter"]
            input_dict["submit_id"] = self.params["submit_id"]
            input_dict["status"] = subject
            input_dict["reason"] = reason

            subject = "N9k Sanity Job {0} Submission: {1}".format(self.params["submit_id"], subject)

            j2env = J2Env()

            template_file = 'job_submission_email.html'
            out_file = "{0}/{1}".format(dir_path, "req_creation_mail.html")
            # print(out_file)
            j2env.create_file(template_file, input_dict, out_file)
            mailer = Mailer(email_to)
            mailer.send_html_mail(subject, out_file)
        except BaseException as e:
            log.error("Exception in send mail:"+repr(e))

    def submit_job(self):
        """ parse params, validate and accept the submission """
        self.record_job_submission()
        validator = Validator(self.params)
        validity, reason = validator.validate()
        if not validity:
            # Validation failed, exit with status
            # update accepted jobs to show why the submission was rejected.
            log.error("Parameter validation failed, reason:" + reason)
            self.abort_submission(reason=reason)
            self.send_email(subject="Failed", reason=reason)
            sys.exit(-1)
        else:
            log.debug("Validation passed...")
        # Move file copying from scheduler stage to here
        setup_data = SetupJobData(self.params)
        setup_data.setup_job_data()
        self.accept_job()
        if self.params["send_updates"]:
            self.send_email()


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument('--submitter')
    parser.add_argument('--build')
    parser.add_argument('--testsuite')
    parser.add_argument('--asic')
    parser.add_argument('--testbed')
    parser.add_argument('--basemode')
    parser.add_argument('--dockermode')
    parser.add_argument('--containermode')
    parser.add_argument('--issu_build_srcdir')
    parser.add_argument('--download_image')
    parser.add_argument('--mparams')
    parser.add_argument('--stopOnFail')
    parser.add_argument('--pauseOnFail')
    parser.add_argument('--newChange')
    parser.add_argument('--download_only')
    parser.add_argument('--email')
    parser.add_argument('--send_updates')

    args = parser.parse_args()
    log.debug("Starting Submit job with below flags: "+repr(args))

    submitter = Submitter(args)
    submitter.submit_job()


if __name__ == "__main__":
    main()
