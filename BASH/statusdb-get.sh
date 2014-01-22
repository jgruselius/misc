url="tools-dev.scilifelab.se:5984/flowcells/_temp_view"
file=$1
func=$(cat $file | tr "\n" " " | tr -d "\t")
json="{\"map\":\"$func\"}"
read -p "Username for server: " user
read -s -p "Password for $user: " pass
curl -s -H "Content-Type: application/json" --data "$json" http://$user:$pass@$url
unset user
unset pass
