url="tools-dev.scilifelab.se:5984/flowcells/_temp_view"
file=$1
if [ -z "$file" ] || [ ! -f $file ] ; then 
	echo "\nUsage:\n\t$0 <mapfunc.js>\n"
	exit
fi
# Remove newlines and tabs:
func=$(cat $file | tr "\n" " " | tr -d "\t")
# Remove comments:
func=$(echo "$func" | perl -pe "s/(\/\*)[^\*]+\*\///")
json="{\"map\":\"$func\"}"
read -p "Username for server: " user
read -s -p "Password for $user: " pass
curl -s -H "Content-Type: application/json" --data "$json" http://$user:$pass@$url
unset user
unset pass

