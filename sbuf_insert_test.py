import requests
import urllib
import httplib2
import json
from datetime import datetime

# This script simply inserts a string with a with the timestamp when this
# script was run into the databse. After the inser, it will then send a
# follow-up query to the databse requesting all timestamps in the databse.
# the script will display the results of the timestamp query for testing.
# Every time this script is run, it should add a new timestamp without
# overwriting any old ones. 


# Create a timestamp when this script runs
now = datetime.now()
timestamp = datetime.timestamp(now)
test_string = 'This is only a test at: %s.' % datetime.fromtimestamp(timestamp)

# The url of the database as well as the repository id
# IMPORTANT: Queries and Updates do not go to the same url!
repository = 'sbuf'
url = 'http://localhost:8080/rdf4j-server/repositories/%s' % (repository)
update_url = 'http://localhost:8080/rdf4j-server/repositories/%s/statements' % (repository)

# The SPARQL command to update the database
update = '''PREFIX sbuf: <http://sbuf.org/grasshopper#>
            PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
            PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
            INSERT DATA {
                sbuf:Test sbuf:InsertTest [rdf:value "%s"^^xsd:string].
            } ''' % (test_string)

# Print the url before sending for debugging purposes
print('POSTing SPARQL update to %s' % (update_url))

# construct the HTTP POST request with the SPARQL update inbedded in it.
params1 = { 'update' : update }
headers = { 'content-type' : 'application/x-www-form-urlencoded',
            'accept' : 'application/sparql-results+json' }

# Send and wait for http response from the database
(response1, content1) = httplib2.Http().request(update_url, 'POST', urllib.parse.urlencode(params1), headers=headers)

#Print out the response code (204 means the SPARQL statement ran without issues)
print('Update Status %s' % (response1.status))

# New SPARQL Query: We want to see if the update actually worked or if there
# were no syntax errors in the SPARQL update. That is, it's possible that the
# SPARQL update ran, but it did not actually do what we want.
query = ''' PREFIX sbuf: <http://sbuf.org/grasshopper#>
            PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
            PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
            SELECT ?val
            WHERE {
              sbuf:Test sbuf:InsertTest [rdf:value ?val].
            }'''


# When the script get's this far, it will print out the ure it will send the query to.
# IMPORTANT: Quiries and Updates do not go to the same url.
print('POSTing SPARQL query to %s' % (url))

# Consrtuct the HTTP POST request with the query imbedded in it
params2 = { 'query' : query }

# Send HTTP POST query request to the database and wait for response.
(response2, content2) = httplib2.Http().request(url, 'POST', urllib.parse.urlencode(params2), headers=headers)

# Print out the status code for the response from the database (200 means that there is data returned with the response)
print('Query Status %s' % (response2.status))

# Parse the content of the response as JSON and print the extracted info
results2 = json.loads(content2)
print( '\n'.join(result['val']['value'] for result in results2['results']['bindings']))
