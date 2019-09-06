""" invoke jenkins stage : invoker_job. """

import jenkins
from utils import constants
from utils.logger import Logger

log = Logger(__name__)


def get_jenkins_handle():
    try:
        ci_jenkins_url = "https://engci-jenkins-sjc2.cisco.com/jenkins/"
        sanity_jenkins = jenkins.Jenkins(ci_jenkins_url, username=constants.JENKINS_USER,
                                         password=constants.JENKINS_TOKEN)
        return sanity_jenkins
    except Exception as e:
        log.error("Exception happened in invoke_jenkins:")
        log.error(repr(e))
        return None


def jenkins_start_invoke_job(submit_id=None):
    if submit_id is None:
        return False, "submit_id is None"
    sanity_jenkins = get_jenkins_handle()
    if sanity_jenkins is None:
        return False, "failed to connect to jenkins server"
    job = "team_basic_sanity/basic_sanity/invoke_job"
    params = {'SUBMIT_ID': submit_id}
    try:
        log.info("Starting invoke job on jenkins for job: {0}".format(submit_id))
        sanity_jenkins.build_job(job, params)
    except Exception as e:
        print("caught an exception "+repr(e))
    return True, "job submitted to jenkins server."
