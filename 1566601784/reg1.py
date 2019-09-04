# coding=utf8
# the above tag defines encoding for this document and is for Python 2.x compatibility

import re

regex = r"((?:\w|\.|\:|\')*)\=((?:\w|\.|\:|\')*)" # all *=* vals
regex1 = r"((?:[a-fA-F0-9]{2}:)+[a-fA-F0-9]{2})" # mac addr only, no ip match
regex2 = r"((?<=\<)\w*)" # get < items
regex3 = r"((?:\w|\.|\:|\'|\s)*)\=((?:\w|\.|\:|\')*)" #get < items best

test_str = (
	"\"<Ether dst=00:00:CC:01:00:01 src=00:00:BB:01:00:01 type=0x800 |<IP src=1.1.1.11 dst=1.1.1.21 |<Padding |<Raw load='00000000000000000000000000PGIDTI10' |>>>>\""
    )


matches = re.finditer(regex3, test_str)

for matchNum, match in enumerate(matches, start=1):
    
    print ("Match {matchNum} was found at {start}-{end}: {match}".format(matchNum = matchNum, start = match.start(), end = match.end(), match = match.group()))
    
    for groupNum in range(0, len(match.groups())):
        # num of groups = len(match.groups()
        # group1 = key
        # group2 = vals
        groupNum = groupNum + 1
        
        print ("Group {groupNum} found at {start}-{end}: {group}".format(groupNum = groupNum, start = match.start(groupNum), end = match.end(groupNum), group = match.group(groupNum)))


# Note: for Python 2.7 compatibility, use ur"" to prefix the regex and u"" to prefix the test string and substitution.
