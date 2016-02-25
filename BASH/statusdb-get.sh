url="tools-dev.scilifelab.se:5984/flowcells/_temp_view"
file=$1
if [ -z "$file" ] || [ ! -f "$file" ] ; then
	echo -e "\nUsage:\n\t$0 <mapfunc.js>\n" >&2
	exit
fi
# Remove newlines and tabs:
func=$(tr "\n" " " < "$file" | tr -d "\t")
# Remove comments:
func=$(echo "$func" | perl -pe "s/(\/\*)[^\*]+\*\///")
json="{\"map\":\"$func\"}"
echo "Using server URL: http://$url" >&2
read -rp "Username for server: " user
read -rs -p "Password for $user: " pass
curl -s -H "Content-Type: application/json" --data "$json" http://"$user":"$pass"@"$url"
unset user
unset pass
