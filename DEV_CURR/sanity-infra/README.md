# n9k-sanity

New Framework fro submitting and scheduling N9K sanity jobs

Requirements:

1. Need to install screen utility in all iTgen's
   yum install screen
2. Check connection to MySQL DB from iTgen's.



The codebase needs to be updated in three places:
1. In insieme servers - /ws/cbhagwat-sjc/repos/n9k-sanity
   Going forward this path needs to be updated with a dedicated directory for N9K sanity in Insieme servers.
   This would be used by production pipeline in the jenkins.
   The Submitter, Scheduler and Health Monitor stages in Jenkins needs to source the env_file before executing.
2. In Sanity server - /auto/n9k-sanity/jenkins-sanity
   This directory can also be moved to a more appropriate place id the current place is not satisfactory.
   Sanity server side handler script needs to source the handler_env_file file.
3. At eor-qa golden directory - /vol/eor-qa/sanity/golden/eor/systest/lib
   When moving to production, the db_update.py file and basic_sanity.py file changes need to be included here.
   A bash script - start_sanity.sh also needs to be included at /vol/eor-qa/sanity/golden
   Right now these scripts are up at /vol/eor-qa/sanity/cbhagwat-cvs


Jenkins Stages:
1. submitter - uses submitter/submitter.py
2. sceduler - uses scheduler/scheduler.py
3. health_monitor - uses health_monitor/health_monitor.py


Jenkins:
https://engci-jenkins-sjc2.cisco.com/jenkins/job/team_basic_sanity/

new sanity server: inno-lnx2
this has /auto, /ws and /vol mounted

New Database:
Host: inno-lnx
Port: 3306
Database: sanity-gui
User: djangouser
Password: iloveDC3.

generic bot user: basicsanitybot.gen@cisco.com
password: Insieme123.

Server to host Django GUI: GUI Hazem UCS: inno-lnx: 172.29.151.141 (iloveDC3)
Generic account for Django folders: djangouser, iloveDc3

MYSQL: djangouser, iloveDC3.

Django: admin, iloveDC3

Old Database:
Host: sjc-dbpl-mysql5
Port: 3306
Database: n9ksanity
User: n9ksanity
Password: n9ksanity

Django official page:
https://www.djangoproject.com/start/

Legacy infra scripts location: /vol/eor-qa/sanity/scripts/eor/sanity-infra
server: ins-sanity-02

