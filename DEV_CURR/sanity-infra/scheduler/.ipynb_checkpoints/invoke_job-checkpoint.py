""" Post scheduling.
    JOb was decided to be scheduled on a testbed.
    Setup remaining job data and start basic_snaity.py
"""

import sys
import os
import argparse
import shutil
import logging
from utils.dbconnect import DBConnect
from utils.ssh_client import SSHClient
from utils.logger import Logger
from scheduler.monitor_job import MonitorJob
from utils.j2 import J2Env
from utils.mailer import Mailer
from utils import constants

log = Logger(__name__)
log.setup_log(console_level=logging.DEBUG)


class InvokeJob:

    job = None
    job_flags = {}
    testbed = None
    job_log_dir = None
    sanity_args = {}
    flag_details = None

    def __init__(self, submit_id):
        if submit_id is None:
            raise ValueError('submit_id param is required to invoke job')
        try:
            dbcon = DBConnect()
            job_cmd = """ select * from submitted_jobs where submit_id={0}""".format(submit_id)
            complete_job_data = dbcon.fetch(job_cmd, type="_tuple")
            self.job = complete_job_data[0]
            log.info("Job info: "+repr(self.job))

            get_flag_details = " select * from flag_details;"
            self.flag_details = dbcon.fetch(get_flag_details, type="_tuple")

            testbed_cmd = """select * from testbeds where testbed='{0}'""".format(self.job.testbed)
            testbed_cmd_data = dbcon.fetch(testbed_cmd, type="_tuple")
            self.testbed = testbed_cmd_data[0]

            self.populate_flags()
        except Exception as e:
            log.error("handler failed:"+repr(e))
            sys.exit(-1)
        finally:
            dbcon.close_connection()

    def populate_flags(self):
        """ populate flags from DB """
        log.error("populating flags")
        complete_flags = self.job.flags
        flag_detail_dict = {}

        # construct a dict [short_name] -> [full_name]
        for flag_detail in self.flag_details:
            flag_detail_dict[flag_detail.flag_id] = flag_detail.flag_name

        # using the above dict, populate flags
        for flag in complete_flags.split(","):
            if flag == "":
                continue
            flag = flag.split("=")
            flag_name = flag_detail_dict[flag[0]]
            self.job_flags[flag_name] = flag[1]
        log.info("job flag dict: "+repr(self.job_flags))

    def binary_to_bool_str(self, val):
        """ 0: False, 1: True """
        if val == 1:
            return "True"
        return "False"

    def update_job_details(self, column, value):
        """ for updating the submitted job table values """
        try:
            dbcon = DBConnect()
            update_flags = """ update submitted_jobs set {column}='{value}'
                               where submit_id={submit_id} """
            update_flags = update_flags.format(column=column, value=value,
                                               submit_id=self.job.submit_id)
            dbcon.execute(update_flags)
        except Exception as e:
            log.error("update_job_details failed:" + repr(e))
            sys.exit(-1)
        finally:
            dbcon.close_connection()

    def populate_sanity_args(self):
        """ populate flags for basic_sanity.py script """
        new_change = ""
        if self.job_flags["newChange"] == constants.NEW_CHANGE:
            new_change = constants.NEW_CHANGE_PATH
        img_name = os.path.basename(self.job.final_image_path)
        self.sanity_args["build"] = "{0}/{1}".format(constants.TFTP_PATH, img_name)
        self.sanity_args["testsuite"] = "{0}/{1}{2}.yml".format(self.job_log_dir,
                                                                self.job_flags["scheduled_testsuite"],
                                                                new_change)
        self.sanity_args["logicaldict"] = "{0}/logical_dict{1}.yml".format(self.job_log_dir, new_change)
        self.sanity_args["testbed"] = "{0}/{1}-testbed{2}.yml".format(self.job_log_dir, self.job.testbed, new_change)
        self.sanity_args["logfile"] = "{0}/{1}-{2}.log".format(self.job_log_dir, self.job.testsuite, self.job.testbed)
        self.sanity_args["reportfile"] = "{0}/{1}-{2}.report".format(self.job_log_dir, self.job.testsuite,
                                                                     self.job.testbed)
        email_list = self.job_flags["email"].replace(" ", "")
        email_flag = "{0}@cisco.com".format(self.job.submitter)
        for email in email_list.split(','):
            if email == "":
                continue
            if not email.endswith("@cisco.com"):
                email += "@cisco.com"
            email_flag = "{0},{1}".format(email_flag, email)
        self.sanity_args["email"] = email_flag
        self.sanity_args["jobid"] = self.job.submit_id
        self.sanity_args["pauseonfail"] = self.binary_to_bool_str(self.job_flags["pauseOnFail"])
        self.sanity_args["basemode"] = self.binary_to_bool_str(self.job_flags["basemode"])
        self.sanity_args["dockermode"] = self.binary_to_bool_str(self.job_flags["dockermode"])
        self.sanity_args["containermode"] = self.binary_to_bool_str(self.job_flags["containermode"])
        self.sanity_args["mparams"] = self.binary_to_bool_str(self.job_flags["mparams"])
        self.sanity_args["stopOnFail"] = self.binary_to_bool_str(self.job_flags["stopOnFail"])
        self.sanity_args["pauseOnFail"] = self.binary_to_bool_str(self.job_flags["pauseOnFail"])
        issu_build = self.job.final_issu_image_path
        if issu_build == "" or issu_build is None:
            self.sanity_args["issu_build"] = "skip"
        else:
            issu_img = "{0}/{1}".format(constants.TFTP_PATH, os.path.basename(issu_build))
            self.sanity_args["issu_build"] = issu_img
        self.sanity_args["reportsubject"] = "NXOS-{0}-{1}{2}".format(self.job.asic, self.job.testsuite, new_change)
        self.sanity_args["terminal_logs"] = "{0}/terminalLogs".format(self.job_log_dir)
        log.info("Starting sanity job with flags:"+repr(self.sanity_args))

    def start_sanity(self):
        """ start the sanity script in a screen """
        try:
            conn = SSHClient(self.testbed.itgen_ip, "root", "insieme")
            start_script = constants.START_SCRIPT
            if self.job_flags["newChange"]:
                # TODO: change to non golden dir
                start_script = constants.START_SCRIPT
            command = "sh -x {start_script} " \
                      "{build} {testsuite} {logical_dict} {testbed} {logfile} {reportfile} " \
                      "{email} {job_id} {pauseonfail} {basemode} {containermode} {dockermode} " \
                      "{issu_build} {reportsubject} {terminal_logs} {log_dir} "
            command = command.format(start_script=start_script, build=self.sanity_args["build"],
                                     testsuite=self.sanity_args["testsuite"],
                                     logical_dict=self.sanity_args["logicaldict"],
                                     testbed=self.sanity_args["testbed"],
                                     logfile=self.sanity_args["logfile"],
                                     reportfile=self.sanity_args["reportfile"],
                                     email=self.sanity_args["email"],
                                     job_id=self.sanity_args["jobid"],
                                     pauseonfail=self.sanity_args["pauseonfail"],
                                     basemode=self.sanity_args["basemode"],
                                     containermode=self.sanity_args["containermode"],
                                     dockermode=self.sanity_args["dockermode"],
                                     issu_build=self.sanity_args["issu_build"],
                                     reportsubject=self.sanity_args["reportsubject"],
                                     terminal_logs=self.sanity_args["terminal_logs"],
                                     log_dir=self.job_log_dir)

            log.info("sending cmd to iTen server:" + repr(command))
            res = conn.send_command(command)
            if not res:
                return False, "ssh client failed to invoke sanity on ITGen server"
            return True, "job handed over to ITGen server"
        except Exception as e:
            log.error("handler failed:" + repr(e))
            sys.exit(-1)

    def copy_config_files(self):
        """ copy testsuite and testbed yam; files """
        new_change = ""
        if self.job_flags["newChange"] == constants.NEW_CHANGE:
            new_change = constants.NEW_CHANGE_PATH
        working_dir = "/vol/eor-qa/sanity"
        testbed_file = "{0}/configs/{1}-testbed{2}.yml".format(working_dir, self.job.testbed, new_change)
        log.info("Copying config files")
        try:
            dbcon = DBConnect()
            # testbed
            shutil.copy(testbed_file, self.job_log_dir)

            # testsuite
            # get short name from asics. ex: hw for homewood.
            asic_shortname_cmd = "select short_name from asics where asic='{asic}'"
            asic_shortname_cmd = asic_shortname_cmd.format(asic=self.job.asic)
            asic_data = dbcon.fetch(asic_shortname_cmd, type="_tuple")
            asic_shortname = asic_data[0].short_name
            testsuite = "{0}_{1}".format(asic_shortname, self.job.testsuite)
            suite_file = "/vol/eor-qa/sanity/jobs/{0}{1}.yml".format(testsuite, new_change)
            shutil.copy(suite_file, self.job_log_dir)
            # update flags
            self.update_job_details("scheduled_testsuite", testsuite)
            self.job_flags["scheduled_testsuite"] = testsuite

        except Exception as e:
            log.error("copy_config_files failed:" + repr(e))
            sys.exit(-123)
        finally:
            dbcon.close_connection()

    def send_email(self, subject="Started" ,reason="Sanity Job started"):
        try:
            dir_path = "/tmp"
            email_to = self.sanity_args["email"]
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

    def invoke_sanity_job(self):
        """ invoke hlite job and monitor """
        self.job_log_dir = """/vol/eor-qa/sanity/logs/{0}/{1}""".format(self.job.submitter,
                                                                        self.job.submit_id)
        self.copy_config_files()
        self.populate_sanity_args()
        self.start_sanity()
        if self.job.send_updates:
            self.send_email()

        # call monitor
        log.info("calling monitor job")
        monitor = MonitorJob(self.job.submit_id, )
        monitor.monitor_job()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--submit_id')
    args = parser.parse_args()

    submit_id = args.submit_id or None
    if submit_id is None:
        log.error("Error in stage, submit_id is None. Exiting..")
        sys.exit(-1)

    log.info("Starting invoke_job for job:{0}".format(submit_id))
    invoke_sanity = InvokeJob(submit_id)
    invoke_sanity.invoke_sanity_job()


if __name__ == "__main__":
    main()
