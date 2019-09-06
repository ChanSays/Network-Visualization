import jenkins
import sys
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
import logging
from sanityapp.models import Asics, Testsuites, Testbeds


logger = logging.getLogger(__name__)


@login_required
def submit_job(request):
    asics = Asics.objects.all()
    testsuites = Testsuites.objects.all()
    testbeds = Testbeds.objects.all()
    context = {
        'asics': asics,
        'testsuites': testsuites,
        'testbeds': testbeds,
    }
    if request.method == 'POST':
        try:
            build = request.POST.get("build")
            testsuite = request.POST.get("testsuite")
            asic = request.POST.get("asic")
            if asic == 'any':
                asic =''
            testbed = request.POST.get("testbed")
            if testbed == 'any':
                testbed = ''
            username = request.user.username
            params = {'BUILD': build,
                      'TESTSUITE': testsuite,
                      'ASIC': asic,
                      'SUBMITTER': username,
                      'TESTBED': testbed,
                      }
            email = request.POST.get("email", None)
            if email is not None:
                params["EMAIL"] = email.strip()

            send_update = request.POST.get("send_update", None)
            if send_update is not None:
                params["SEND_UPDATE"] = send_update

            issu_build = request.POST.get("issu_build", None)
            if issu_build is not None:
                params["ISSU_BUILD_SRCDIR"] = issu_build

            download_image = request.POST.get("download_image", None)
            if issu_build is not None:
                params["DOWNLOAD_IMAGE"] = download_image

            boot_mode = request.POST.get("boot_mode", None)
            if boot_mode is not None:
                params[boot_mode] = "1"

            on_fail = request.POST.get("on_fail", None)
            if on_fail is not None:
                params[on_fail] = "1"

            new_change = request.POST.get("new_change", None)
            if new_change is not None:
                params["NEW_CHANGE"] = "1"

            download_only = request.POST.get("download_only", None)
            if download_only is not None:
                params["DOWNLOAD_ONLY"] = "1"

            sanity_jenkins = build_submit_job()
            if sanity_jenkins is None:
                return HttpResponse('Unable to connect to jenkins')

            logging.debug(f" params are {params}")

            job = "team_basic_sanity/basic_sanity/submit_sanity"
            sanity_jenkins.build_job(job, params)
            logging.debug("sanity job was submitter for user:"+username)
            context['submission'] = "Successfully Submitted"
        except Exception as e:
            logger.error("Exception happened in submissionsapp.submit_job:")
            logger.error(repr(e))
            return HttpResponse('Unexpected error occurred in submissionsapp.submit_job')

    return render(request, 'submit_job.html', context)


def build_submit_job():
    try:
        ci_jenkins_url = "https://engci-jenkins-sjc2.cisco.com/jenkins/"
        username = "cbhagwat"
        token = "11a0ffc6c446a95f525a9d8ef7c0b3bd63"
        sanity_jenkins = jenkins.Jenkins(ci_jenkins_url, username=username, password=token)
        return sanity_jenkins
    except Exception as e:
        logger.error("Exception happened in submissionsapp.build_submit_job:")
        logger.error(repr(e))
        return None
