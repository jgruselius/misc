This brief help describes how to query a CouchDB database from a terminal emulator using scripts in this repository. A "map function" is defined in JavaScript which specifies how to generate the JSON data from the database. See CouchDB documentation for how to construct this function. This repo provides an example map function [statusdb-index-read-view.js](https://github.com/jgruselius/misc/blob/master/JavaScript/statusdb-index-read-view.js) which gets data yield per index, lane and flowcell from SciLifeLab's StatusDB.

For the simplest method, see *3*.

#### 1. In the terminal: ####
Create a <code>map.json</code> file containing:
```json
{"map":"function(doc) { ... }"}
```
Remove all newline characters and make sure to use correct quoting.
The StatusDB view can then be queried by running:
```bash
curl -s -H "Content-Type: application/json" --data "@map.json" \
"http://USER:PASS@tools-dev.scilifelab.se:5984/flowcells/_temp_view"
```
Where <code>USER</code> and <code>PASS</code> should be replaced with the actual login details to the database server.

#### 2. Using the shell script: ####

To use the map function defining a CouchDB view defined in the file <code>mapfunc.js</code>, use the shell script [<code>statusdb-get.sh</code>](https://github.com/jgruselius/misc/blob/master/BASH/statusdb-get.sh):

```bash
sh statusdb-get.sh <mapfunc.js>
```

The script will prompt for server login details.

#### 3. Using the Python script: ####

The above can now be done using the [statusdb-get.py](https://github.com/jgruselius/misc/blob/master/Python/statusdb-get.py) script, which also offers the option to convert database response to comma-separated values.

##### Example: #####
```bash
python "Python/statusdb-get.py" --out "data.csv" \
--url "http://tools-dev.scilifelab.se:5984/flowcells/_temp_view" --csv \
"JavaScript/statusdb-index-read-view.js"
```

The script will prompt for database login details.

**Note:**
The <code>--csv</code> option requires a defined JSON format and therefore only works with the [example map function](https://github.com/jgruselius/misc/blob/master/JavaScript/statusdb-index-read-view.js).

Print usage help by running:
```bash
python statusdb-get.py --help
```

```
usage: statusdb-get.py [-h] [--out OUT] [--url URL] [--csv] jsfile

Query a CouchDB database

positional arguments:
  jsfile      File containing JavaScript map function

optional arguments:
  -h, --help  show this help message and exit
  --out OUT   File to write response to. If omitted write to stdout
  --url URL   Database URL. If omitted use http://tools-
              dev.scilifelab.se:5984/flowcells/_temp_view
  --csv       Convert response to CSV
```
