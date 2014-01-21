To use this function as a CouchDB view, create a map.json file containing:
```json
        {"map":"function(doc) { ... }"}
```
Remove all newline characters and make sure to use correct quoting.
The StatusDB view can then be queried by running:
```bash
        curl -s -H "Content-Type: application/json" --data "@map.json" \
        http://USER:PASS@tools-dev.scilifelab.se:5984/flowcells/_temp_view
```
Where USER and PASS should be replaced with the actual login details.
