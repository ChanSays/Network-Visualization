from django.db import models


# Create your models here.
class Asics(models.Model):
    asic = models.CharField(primary_key=True, max_length=30)
    testbeds = models.TextField(blank=True, null=True)
    short_name = models.CharField(max_length=30, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'asics'


class ChangePriorityReq(models.Model):
    submit_id = models.PositiveIntegerField(primary_key=True)
    requester = models.CharField(max_length=30, blank=True, null=True)
    req_priority = models.IntegerField(blank=True, null=True)
    req_reason = models.TextField(blank=True, null=True)
    req_status = models.CharField(max_length=8, blank=True, null=True)
    status_reason = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'change_priority_req'


class FlagDetails(models.Model):
    flag_name = models.CharField(primary_key=True, max_length=30)
    flag_id = models.CharField(unique=True, max_length=3)

    class Meta:
        managed = False
        db_table = 'flag_details'


class CompletedJobs(models.Model):
    submit_id = models.BigIntegerField(primary_key=True)
    submit_date = models.DateTimeField()
    submitter = models.CharField(max_length=30)
    build = models.TextField()
    testsuite = models.CharField(max_length=30)
    testbed = models.CharField(max_length=30, blank=True, null=True)
    asic = models.CharField(max_length=30, blank=True, null=True)
    priority = models.PositiveIntegerField()
    eta = models.IntegerField(blank=True, null=True)
    status = models.CharField(max_length=9)
    status_date = models.DateTimeField()
    start_time = models.DateTimeField(blank=True, null=True)
    end_time = models.DateTimeField(blank=True, null=True)
    results = models.TextField(blank=True, null=True)
    logs = models.TextField(blank=True, null=True)
    final_image_path = models.TextField(blank=True, null=True)
    final_issu_image_path = models.TextField(blank=True, null=True)
    scheduled_testsuite = models.CharField(max_length=30, blank=True, null=True)
    flags = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'completed_jobs'


class SubmittedJobs(models.Model):
    submit_id = models.BigAutoField(primary_key=True)
    submit_date = models.DateTimeField()
    submitter = models.CharField(max_length=30)
    build = models.TextField()
    testsuite = models.CharField(max_length=30)
    testbed = models.CharField(max_length=30, blank=True, null=True)
    asic = models.CharField(max_length=30, blank=True, null=True)
    priority = models.PositiveIntegerField()
    eta = models.IntegerField(blank=True, null=True)
    status = models.CharField(max_length=9)
    status_date = models.DateTimeField()
    start_time = models.DateTimeField(blank=True, null=True)
    end_time = models.DateTimeField(blank=True, null=True)
    results = models.TextField(blank=True, null=True)
    logs = models.TextField(blank=True, null=True)
    final_image_path = models.TextField(blank=True, null=True)
    final_issu_image_path = models.TextField(blank=True, null=True)
    scheduled_testsuite = models.CharField(max_length=30, blank=True, null=True)
    flags = models.TextField(blank=True, null=True)
    percentage = models.IntegerField(blank=True, null=True)
    remaining = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'submitted_jobs'


class Testbeds(models.Model):
    testbed = models.CharField(primary_key=True, max_length=30)
    description = models.CharField(max_length=100)
    asic = models.CharField(max_length=10)
    devicetype = models.CharField(max_length=10)
    support = models.CharField(max_length=20)
    status = models.CharField(max_length=6)
    lock_status = models.CharField(max_length=8)
    lock_owner = models.CharField(max_length=30, blank=True, null=True)
    lock_msg = models.TextField(blank=True, null=True)
    itgen_ip = models.CharField(max_length=20, blank=True, null=True)
    current_job = models.BigIntegerField(blank=True, null=True)
    topology = models.BinaryField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'testbeds'


class Testsuites(models.Model):
    testsuite = models.CharField(primary_key=True, max_length=30)
    eta = models.PositiveIntegerField()
    unsupported_asics = models.CharField(max_length=45, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'testsuites'


class UserMsgs(models.Model):
    id = models.AutoField(primary_key=True)
    submit_id = models.IntegerField(blank=True, null=True)
    user = models.CharField(max_length=30, blank=True, null=True)
    msg = models.TextField(blank=True, null=True)
    msg_type = models.CharField(max_length=6, blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'user_msgs'
