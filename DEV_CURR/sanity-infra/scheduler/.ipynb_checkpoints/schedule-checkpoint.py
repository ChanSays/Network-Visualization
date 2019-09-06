""" Job scheduler - cron job
    Sort jobs on priority and submission date.
    Try to schedule each job from this list, one at a time and move on to next job.
"""

import logging
from datetime import datetime
import sys
from utils.dbconnect import DBConnect
from utils.invoke_jenkins import jenkins_start_invoke_job
from utils.logger import Logger

log = Logger(__name__)
log.setup_log(console_level=logging.DEBUG)


class Scheduler:

    pending_jobs = None
    dbcon = None

    def __init__(self):
        """ get all pending jobs as named tuple
        """
        try:
            self.dbcon = DBConnect()
            get_jobs_cmd = "select * from submitted_jobs where status='pending' order by priority, submit_date;"
            self.pending_jobs = self.dbcon.fetch(get_jobs_cmd, type="_tuple")
            free_testbed_cmd = """select testbed, asic from testbeds where status='free' and lock_status='unlocked' """
            free_tbs = self.dbcon.fetch(free_testbed_cmd, type="_tuple")
            log.info("Free testbeds: {0}".format(repr(free_tbs)))
        except Exception as e:
            log.error("Scheduler failed:"+repr(e))
            sys.exit(-1)

    def __del__(self):
        log.info("Scheduler exiting!")
        if self.dbcon is not None:
            self.dbcon.close_connection()

    def abort_job(self, job=None, msg=None):
        # TODO
        log.error("abort job "+repr(job.submit_id)+" reason="+repr(msg))

    def get_an_available_testbed(self, job=None):
        """get all free testbeds of asic type """
        if job is None:
            log.error("get_available_testbeds: job can't be None")
            sys.exit(-1)
        asic = job.asic
        try:
            if asic == "":
                # filter out using unsupported asics
                asic_cmd = "select unsupported_asics from testsuites" \
                           " where testsuite='{0}';".format(job.testsuite)
                asic_data = self.dbcon.fetch(asic_cmd, type="_tuple")
                asic_data = asic_data[0].unsupported_asics.split(",")
                asic_list = ', '.join("'{0}'".format(w) for w in asic_data)
                free_testbed_cmd = """select * from testbeds where asic not in ({0})
                                      and status='free' and lock_status='unlocked' limit 1 
                                      """.format(asic_list)
            else:
                # get a free testbed of asic type
                free_testbed_cmd = """select * from testbeds where asic='{0}' and status='free' 
                                      and lock_status='unlocked' limit 1 """.format(asic)

            testbeds = self.dbcon.fetch(free_testbed_cmd, type="_tuple")
            if len(testbeds) == 0:
                # no free testbeds available
                return None
            else:
                log.info("Available testbeds are: "+repr(testbeds))
                return testbeds[0]
        except Exception as e:
            log.error("Scheduler failed in get_an_available_testbed:"+repr(e))
            return None

    def get_testbed_if_free(self, testbed=None):
        """ check is testbed is free """
        if testbed is None:
            log.error("is_testbed_free: testbed can't be None")
            sys.exit(-1)
        log.info("Checking to see if testbed {0} is free.".format(testbed))
        try:
            testbed_cmd = "select * from testbeds where testbed='{0}'".format(testbed)
            testbed = self.dbcon.fetch(testbed_cmd, type="_tuple")
            status = testbed[0].status
            lock_status = testbed[0].lock_status
            if status != "free" or lock_status != "unlocked":
                return None
            return testbed[0]
        except Exception as e:
            log.error("Scheduler failed in get_testbed_if_free:"+repr(e))
            sys.exit(-1)

    def schedule_job_on(self, job=None, testbed=None):
        if job is None or testbed is None:
            log.error("Unable to schedule, invalid params. job/testbed is None")
            sys.exit(-1)

        log.info("scheduling job {0} on {1}".format(job.submit_id, testbed.testbed))
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        try:
            # update tb_status
            tbstatus_cmd = """ update testbeds set status='busy',current_job={0}
                           where testbed='{1}'
                           """.format(job.submit_id, testbed.testbed)
            self.dbcon.execute(tbstatus_cmd)

            # update status in accepted jobs
            update_job_cmd = """ update submitted_jobs set testbed='{0}', status='{1}',
                             status_date='{2}', start_time='{2}', asic='{3}' where submit_id={4}
                             """.format(testbed.testbed, "running", now, testbed.asic,
                                        job.submit_id)
            self.dbcon.execute(update_job_cmd)

            result, msg = self.start_job(job)
            if not result:
                self.abort_job(job, msg)
            else:
                log.info("job {0} was sent to sanity server".format(job.submit_id))

        except Exception as e:
            log.error("Scheduler failed in schedule_job_on:"+repr(e))
            sys.exit(-123)

    def start_job(self, job=None):
        """ start invoke_job stage using job id """
        if job is None:
            log.error("Unable to start job, invalid params")
            sys.exit(-123)
        return jenkins_start_invoke_job(job.submit_id)

    def schedule_jobs(self):
        """schedule based on priority and fcfs policy"""
        for job in self.pending_jobs:
            log.info("Trying to schedule job: {0}".format(job.submit_id))
            testbed = job.testbed
            if testbed != "":
                free_tb = self.get_testbed_if_free(testbed=testbed)
                if free_tb is not None:
                    self.schedule_job_on(job=job, testbed=free_tb)
            else:
                free_tb = self.get_an_available_testbed(job=job)
                if free_tb is not None:
                    self.schedule_job_on(job=job, testbed=free_tb)


def main():
    log.info("Scheduler started!!!")
    sch = Scheduler()
    sch.schedule_jobs()


if __name__ == "__main__":
    main()
