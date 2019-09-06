# set var
start=1

for i in `grep $oldString $searchFiles |cut -d: -f1|uniq`; do
  sed -i 's/${oldString}/${newString}/g' interface_uls.yml;
  start=$(($start+1))
  # remove by line num
  # sed -i '' $1'd' /Users/lindach/.ssh/known_hosts
done
echo  "replace num Done.\n"


# ag -o '(?<=-id\s)[0-9]*' interface_uls.yml

#
#while read p; do
#  echo "$p"
#done < interface_uls.yml
