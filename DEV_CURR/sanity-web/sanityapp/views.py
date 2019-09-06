import logging
import json
from django.core import serializers
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import SubmittedJobs, CompletedJobs, Testbeds, Testsuites, UserMsgs, Asics
from .ssh_client import SSHClient
from django.db import connection

log = logging.getLogger(__name__)


# Create your views here.
def index(request):
    return render(request, 'index.html')


@login_required
def testbed_status(request):
    testbedsInfo = Testbeds.objects.all()
    username = request.user.username
    rjobs = SubmittedJobs.objects.filter(submitter=username)
    context = {
        'testbedsInfo': testbedsInfo,
        'rjobs': rjobs
    }
    return render(request, 'testbed_status.html', context)


### GET each ASIC testbeds info.
def display_testbed_info(request):
    asic = request.GET.get("asic")
    testbedsInfo = Testbeds.objects.filter(asic=asic)
    rjobs = SubmittedJobs.objects.filter(status='running')
    context = {
        'testbedsInfo': testbedsInfo,
        'asic': asic,
        'rjobs': rjobs
    }
    return render(request, 'displaytestbedinfo.html', context)


@login_required
def get_job_details(request):
    submit_id = request.GET.get("submit_id")
    job = SubmittedJobs.objects.filter(submit_id=submit_id)
    if job.count() == 0:
        log.info("not in submitted jobs")
        job = CompletedJobs.objects.filter(submit_id=submit_id)
    job = job[0]
    log.info("Getting logs for job {0} submitter {1}".format(job.submit_id, job.submitter))

    context = {
        'job': job
    }
    return render(request, 'job_details.html', context)


@login_required
def get_logs(request):
    submit_id = request.GET.get("submit_id")
    job = SubmittedJobs.objects.filter(submit_id=submit_id)
    if job.count() == 0:
        log.info("not in submitted jobs")
        job = CompletedJobs.objects.filter(submit_id=submit_id)
    job = job[0]
    log.info("Getting logs for job {0} submitter {1}".format(job.submit_id, job.submitter))

    log_path = "/vol/eor-qa/sanity/logs/{0}/{1}/{2}-{3}.log".format(job.submitter, job.submit_id, job.testsuite,
                                                                   job.testbed)
    sftp = SSHClient()
    contents = sftp.get_file_contents(log_path)
    log.info("contents")
    return HttpResponse(contents)


@login_required
def user_jobs(request):
    username = request.user.username
    job_filter = request.GET.get("filter")
    s_jobs = None
    c_jobs = None

    if job_filter is None:
        c_jobs = CompletedJobs.objects.filter(submitter=username)
        s_jobs = SubmittedJobs.objects.filter(submitter=username)
    elif job_filter == 'active':
        s_jobs = SubmittedJobs.objects.filter(submitter=username)
    elif job_filter == 'completed':
        c_jobs = CompletedJobs.objects.filter(submitter=username)
    context = {
        's_jobs': s_jobs,
        'c_jobs': c_jobs,
    }
    if request.method == "POST":
        submit_id = int(request.POST.get("submit_id", ""))
        kill_this_job(submit_id)
        context['deleted_submit_id'] = submit_id
    return render(request, 'user_jobs.html', context)


def kill_this_job(submit_id):
    this_job = SubmittedJobs.objects.filter(submit_id=submit_id)[0]
    log.info(this_job)
    SubmittedJobs.objects.filter(submit_id=submit_id).delete()
    delete_job = CompletedJobs(
        submit_id=submit_id,
        submit_date=this_job.submit_date,
        submitter=this_job.submitter,
        build=this_job.build,
        testsuite=this_job.testsuite,
        testbed=this_job.testbed,
        asic=this_job.asic,
        status='deleted',
        status_date=this_job.status_date,
        priority=6
    )
    delete_job.save()
    return

def lock_this_testbed(request):
    return


@login_required
def view_all_jobs(request):
    return render(request, 'all_jobs.html')


@login_required
def get_all_jobs(request):
    limit = request.GET.get('limit') or "False"

    # making a raw sql command because of django command limitations
    cmd = """
    SELECT S.submit_id, S.submitter, S.submit_date, S.status, S.testsuite, S.asic, S.testbed, S.priority, S.eta
    FROM submitted_jobs S
    LEFT JOIN completed_jobs C
    ON S.submit_id = C.submit_id
    UNION ALL
    SELECT C.submit_id, C.submitter, C.submit_date, C.status, C.testsuite, C.asic, C.testbed, C.priority, C.eta
    from submitted_jobs S
    RIGHT JOIN completed_jobs C
    ON S.submit_id = C.submit_id
    ORDER BY submit_id DESC
    """
    if limit == "True":
        cmd = cmd + "LIMIT 1000 "

    log.info(cmd)

    with connection.cursor() as cursor:
        cursor.execute(cmd)
        jobs = cursor.fetchall()
        columns = [col[0] for col in cursor.description]
        dict_data = [ dict(zip(columns, row)) for row in jobs ]

    # replace dartetime with string
    for row in dict_data:
        row['submit_date'] = row['submit_date'].strftime("%Y-%m-%d %H:%M:%S")
        # row['start_time'] = "" if row['start_time'] is None else row['start_time'].strftime("%Y-%m-%d %H:%M:%S")
        # row['end_time'] = "" if row['end_time'] is None else row['end_time'].strftime("%Y-%m-%d %H:%M:%S")
        row['eta'] = "" if row['eta'] is None else row['eta']

    single_dict = {
        'data': dict_data
    }
    data = json.dumps(single_dict)
    log.info(data)
    return HttpResponse(data, content_type='application/json')


@login_required
def view_msgs(request):
    return render(request, 'view_msgs.html')


@login_required
def get_msgs(request):
    user = request.user.username
    msgs = UserMsgs.objects.filter(user=user).order_by('-id')

    data = serializers.serialize('json', msgs)
    log.info(msgs, data)
    return HttpResponse(data, content_type='application/json')


# if request.user.is_superuser:
@login_required
def add_new_testbed(request):
    if not request.user.is_superuser:
        return HttpResponse('Unauthorized', status=401)

    context = {}
    if request.method == 'POST':
        testbed = request.POST.get('testbed')
        description = request.POST.get('description')
        asic = request.POST.get('asic')
        devicetype = request.POST.get('devicetype')
        support = request.POST.get('support')
        itgen_ip = request.POST.get('itgen_ip')
        new_tb = Testbeds(testbed=testbed,
                          description=description,
                          asic=asic,
                          devicetype=devicetype,
                          support=support,
                          itgen_ip=itgen_ip,
                          status="busy",
                          lock_status="locked")
        new_tb.save()
        context['new_tb'] = testbed

        asic_obj = Asics.objects.filter(asic=asic)[0]
        tb_list = asic_obj.testbeds
        asic_obj.testbeds = "{},{}".format(tb_list,testbed)
        asic_obj.save()

    return render(request, 'add_new_testbed.html', context)
