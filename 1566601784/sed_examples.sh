txt='Mon Jan 22 12:12:12 2012 foo=blah   foo2=blah2  foo3=Some longer sentence that can contain spaces and numbers   somethingelse=blarg   foo5=abcdefg
Mon Jan 22 12:13:12 2012 foo=blah   foo2=blah3  foo3=another long sentence that could be the same or different that the prior log entry   somethingelse=blarg   foo5=112345abcdefg
Mon Jan 22 12:14:12 2012 foo=blah   foo2=blah2  foo3=Foo923847923874Some longer sentence that can contain spaces and numbers   somethingelse=blarg   foo5=abcdefg
Mon Jan 22 12:15:12 2012 foo=blah   foo2=blah2  foo3=Fooo02394802398402384Some longer sentence that can contain spaces and numbers   somethingelse=blarg   foo5=abcdefg'


# take the first 8 words out of each line of input:
echo $txt|sed -rn 's/^(\S+\s){8}(.*)/\2/p' 

####################################################################################

echo $txt| sed 's/[^ ]\{1,\}=/\n&/g' | grep '^foo3=' #BEST, match all foo3 vals


echo $txt|sed -n '/foo3=/{s/.*foo3=//;s/\S*=.*//;p}' 
echo $txt|sed -n 's/.*foo3=\([^=]*\)\s\+\S*=.*/\1/p' 

echo $txt| sed '/\n/s/ [^ ]*=.*//p;/\n/!s/foo3=/\n\n&/;D' | grep . 

####################################################################################