# Generated by Django 2.2.4 on 2019-08-22 21:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sanityapp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ChangePriorityReq',
            fields=[
                ('submit_id', models.PositiveIntegerField(primary_key=True, serialize=False)),
                ('requester', models.CharField(blank=True, max_length=30, null=True)),
                ('req_priority', models.IntegerField(blank=True, null=True)),
                ('req_reason', models.TextField(blank=True, null=True)),
                ('req_status', models.CharField(blank=True, max_length=8, null=True)),
                ('status_reason', models.TextField(blank=True, null=True)),
            ],
            options={
                'db_table': 'change_priority_req',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='UserMsgs',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('submit_id', models.IntegerField(blank=True, null=True)),
                ('user', models.CharField(blank=True, max_length=30, null=True)),
                ('msg', models.TextField(blank=True, null=True)),
                ('msg_type', models.CharField(blank=True, max_length=6, null=True)),
                ('updated_at', models.DateTimeField(blank=True, null=True)),
            ],
            options={
                'db_table': 'user_msgs',
                'managed': False,
            },
        ),
    ]
