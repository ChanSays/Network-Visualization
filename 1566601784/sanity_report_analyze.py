#!/usr/local/bin/python2.7
import re
import glob
import requests, json

### get testsuite 
yamlfiles = glob.glob('*.yml')
for file in yamlfiles:
    if 'uls' in file or '_sanity' in file:
        testsuite = file

### open report file to get failed cases 
reportfile = glob.glob('./*.report')[0]
report = open(reportfile,"r")
reportContent = report.read()
report.close()
failCase = re.findall('(test[a-zA-Z0-9]+)\s+fail',reportContent)
#print failCase

#testFexSviPingVrf: END
#testFexSviPingVrf: START

### get each failed case logs
logfile = glob.glob('./*.log')[0]
log = open(logfile,'r')
logContent = log.read()
log.close()


### get image versions.
#2019-05-25 13:59:23,331 - PYLOG - INFO - version: 9.3(1)
#2019-05-25 13:59:23,331 - PYLOG - INFO - build: 9.3(0.340)
#2019-05-25 19:06:11,156 - PYLOG - INFO - version: 9.2(2v)
#2019-05-25 19:06:11,156 - PYLOG - INFO - build: 9.2#(2v)IIP9#(0.14)
#test = "2019-05-25 18:19:02,832 - PYLOG - INFO - build: 9.2#(1)IDW9#(0.318)"
ver_match = re.search('PYLOG - INFO - version: (.*)', logContent)
if ver_match:
    version =  ver_match.group(1)

build_match = re.search('PYLOG - INFO - build: (.*)',logContent)
if build_match:
    build = build_match.group(1) 

if 'IDW' in build:
    branch = 'udb_wolf'
elif 'IIP' in build:
    branch = 'ironcity'
elif 'IDI' in build:
    branch = 'iplus_dev'
elif '9.2(' in version:
    branch = 'hamilton'
elif '7.0(3)' in version:
    branch = 'greensboro'
else:
    branch = 'irvine' #all else use default irvine branch 

### get case last working build
def getFailCaseLastWorkingBuild(branch,testcase):
    '''API provided by release team
    checking with Divakar for more details
    http://rapido1:8000'''

    res = requests.post('http://rapido1.cisco.com:8000/search_sanity.info',
                        json ={"branch": branch,"testcase": testcase})
    msg = ''
    if res.ok:
        data = res.json()
        for i in range(1,200):
         
            try:
                if  data[str(i)]['status'] == 'pass' and 'NXOSv' not in data[str(i)]['class']:
                    msg = 'Last Working Build: {0}. ASIC: {1}. Run in: {2}. Nightly Job: "{3}"'\
                        .format(data[str(i)]['tag'],data[str(i)]['class'],data[str(i)]['sanity_type'],data[str(i)]['job_id'])
                    break
            except KeyError:
                msg = "No pass data Found"
            else:
                msg = 'No Running Data Found'
    else:
        msg = 'No Running Data Found'   
    return msg

analyzefile = open('./AnalyzeReport.html','w+')
analyzefile.write('<a name="top"></a>')
analyzefile.write('<h2><a href="https://wiki.cisco.com/display/NEXUS9K/N9K+Sanity" target="_blank">SANITY-WIKI</a></h2>\n')
analyzefile.write('<h2><a href="https://wiki.cisco.com/display/NEXUS9K/How+to+check+sanity+logs" target="_blank"> HOW TO CHECK SANITY FULL LOGS </a></h2>\n')
analyzefile.write('<h2><a href="http://wwwin-ins-sw-web.cisco.com/build/branch_build_info.shtml?branch={0}" target="_blank"> CHECK IN BUILD PAGE</a></h2>\n'.format(branch))
analyzefile.write('<h3>FAILED CASES: </h3>')
for case in failCase:
    analyzefile.write('<li><a href = "#{0}"> {0} </a></li>'.format(case))

for case in failCase:
    history = getFailCaseLastWorkingBuild(branch,case)
    analyzefile.write("<p>++++++++++++++++++++++++++++++++++++++++++++++++</p>")
    analyzefile.write("<h4 id = '{0}'> FAILD CASE  :  {0}</h4>".format(case))
    analyzefile.write('<p>History:</p>')
    analyzefile.write('<p><font color = "blue">{0}</font></p>'.format(history))
    analyzefile.write("<p>++++++++++++++++++++++++++++++++++++++++++++++++</p>")

    case_start = case + ': START'
    case_end = case + ': END'
    failLogs = re.search('{0}(.*){1}'.format(case_start,case_end),logContent,re.DOTALL)
    oneFailcaselog=failLogs.group().split('\n')
    for log in oneFailcaselog:
        if 'PYLOG - ERROR - FAIL' in log:
            analyzefile.write("<p>{0}</p>".format(log))
        if 'ERROR:' in log:
            analyzefile.write('<p><font color="red">{0}</font></p>'.format(log))
    analyzefile.write('<p><a href="#top">back to top</a></p>')

analyzefile.close()
