url="tools-dev.scilifelab.se:5984/flowcells/_temp_view"
file=$1
if [ -z "$file" ] || [ ! -f $file ] ; then 
	echo "\nUsage:\n\t$0 <mapfunc.js>\n"
	exit
fi
func=$(cat $file | tr "\n" " " | tr -d "\t")
json="{\"map\":\"$func\"}"
read -p "Username for server: " user
read -s -p "Password for $user: " pass
curl -s -H "Content-Type: application/json" --data "$json" http://$user:$pass@$url
unset user
unset pass
