import requests
import urllib
import httplib2
import json
from datetime import datetime

# This updates the value of the default counter (incriment the current value in
# the databse by 1) and then sends a query that requests the value of the counter.
# If run several times, you should see that the value returned by the database
# incriments. 

# The url of the database as well as the repository id
repository = 'sbuf' #this is the repository id
url = 'http://localhost:8080/rdf4j-server/repositories/%s' % (repository) #this is where simple queries go
update_url = 'http://localhost:8080/rdf4j-server/repositories/%s/statements' % (repository) #this is where updates go (anything that alters the state of the database)

# The SPARQL Command that the databse should execute
update = '''PREFIX sbuf: <http://sbuf.org/grasshopper#>
            PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
            PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
            WITH <sbuf:GrasshopperConfigurations>
            DELETE { ?node rdf:value ?val }
            INSERT { ?node rdf:value ?newval }
            WHERE {
                sbuf:Default sbuf:Counter ?node .
                ?node rdf:value ?val .
                Bind( (?val + 1) AS ?newval)
            }  '''

# When the script get's this far, it will print out the url for debugging
print('POSTing SPARQL update to %s' % (update_url))

# Construct the HTTP POST request to be sent to the databse
params1 = { 'update' : update }
headers = { 'content-type' : 'application/x-www-form-urlencoded',
            'accept' : 'application/sparql-results+json' }

# Send HTTP request, wait for response
(response1, content1) = httplib2.Http().request(update_url, 'POST', urllib.parse.urlencode(params1), headers=headers)

# Prind the response code of the HTTP request (204 means the SPARQL statement ran without issues)
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
              sbuf:Default sbuf:Counter ?node .
              ?node rdf:value ?val
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
