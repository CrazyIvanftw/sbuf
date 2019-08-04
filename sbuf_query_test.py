import requests
import urllib
import httplib2
import json


# This script will send a SPARQL query to the databse that requests all of
# the data for the default grasshopper configuration (I.e. the numbers that were
# in grasshopper on the day that I wen't in to hard code them in the databse).
# The script will print the values it receives to the terminal.


# The url of the database as well as the repository id
repository = 'sbuf'
url = 'http://localhost:8080/rdf4j-server/repositories/%s' % (repository)

# The SPARQL Command that will query the database
query = ''' PREFIX sbuf: <http://sbuf.org/grasshopper#>
            PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
            PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
            SELECT ?property ?item ?val
            WHERE {
              sbuf:Default ?property [?item ?val].
              sbuf:Default ?property [sbuf:GroupTag "Setup"].
            }'''


# When the script get's this far, it will print out the url for debugging
print('POSTing SPARQL query to %s' % (url))

# Construct the HTTP POST request to be sent to the databse
# In the header 'application/sparql-results+json' means that you're
# requesting that the results be returned in the json format. You can
# also request xml if that is preferable.
params = { 'query' : query }
headers = { 'content-type' : 'application/x-www-form-urlencoded',
            'accept' : 'application/sparql-results+json' }

# Send HTTP request, wait for response
(response, content) = httplib2.Http().request(url, 'POST', urllib.parse.urlencode(params), headers=headers)

# Prind the response code of the HTTP request  (200 means that there is data returned with the response)
print('Response %s' % (response.status))

# Parse the content of the response as JSON and print the extracted info
results = json.loads(content)
print( '\n'.join((result['property']['value'] + ' --- ' + result['item']['value'] + ' --- ' + result['val']['value']) for result in results['results']['bindings']))
