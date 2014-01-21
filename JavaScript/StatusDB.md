To use this function as a CouchDB view, create a <code>map.json</code> file containing:
```json
        {"map":"function(doc) { ... }"}
```
Remove all newline characters and make sure to use correct quoting.
The StatusDB view can then be queried by running:
```bash
        curl -s -H "Content-Type: application/json" --data "@map.json" \
        http://USER:PASS@tools-dev.scilifelab.se:5984/flowcells/_temp_view
```
Where <code>USER</code> and <code>PASS</code> should be replaced with the actual login details.
