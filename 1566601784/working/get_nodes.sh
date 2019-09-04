# TRAFFIC PROFILE USED

# check tb.yml

sed -n '/profile_l2_sanity/,/profile/p' sanity97-testbed.yml > traffic_profile.yml 

# if empty check logical dict
sed -n '/profile_l2_sanity/,/profile/p' logical_dict.yml > traffic_profile.yml 

# else node info unavailable, exit


# cut out last line of profile
sed -e '$ d' traffic_profile.yml > traffic_profile_2.yml


# parse nodedict from sanity97-testbed.yml 



# get tor name per traffic_run "sanity97-tor1" "sanity97-node03" "sanity97-tor2"


# get line number per match 
# search prev tor starting there

# regex to get last tor# found
https://regex101.com/r/oO85cN/3
(?:sanity97-tor[0-9].*)(?:[\w\W\s]*)(sanity97-tor[0-9])([\w\W\s\S]*)




