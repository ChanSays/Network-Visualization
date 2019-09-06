import logging
from .models import Asics, UserMsgs,SubmittedJobs

log = logging.getLogger(__name__)

def navagation_data(request):
    fetch_asics = Asics.objects.all()
    username = request.user.username
    fetch_all_jobs = SubmittedJobs.objects.filter(submitter=username)
    msgs = UserMsgs.objects.filter(user=username).order_by('-updated_at')[:4]
    context = {
        'asics': fetch_asics,
        'msgs': msgs,
        'user_submitted_jobs': fetch_all_jobs
    }
    return context
