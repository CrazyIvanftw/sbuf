import requests
import urllib
import httplib2
import json

repository = 'sbuf'
url = 'http://localhost:8080/rdf4j-server/repositories/%s' % (repository)

query = ''' PREFIX sbuf: <http://sbuf.org/grasshopper#>
            PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
            PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
            SELECT ?property ?item ?val
            WHERE {
              sbuf:Default ?property [?item ?val].
              sbuf:Default ?property [sbuf:GroupTag "Setup"].
            }'''

print('POSTing SPARQL query to %s' % (url))

params = { 'query' : query }
headers = { 'content-type' : 'application/x-www-form-urlencoded',
            'accept' : 'application/sparql-results+json' }

(response, content) = httplib2.Http().request(url, 'POST', urllib.parse.urlencode(params), headers=headers)

print('Response %s' % (response.status))
results = json.loads(content)
print( '\n'.join((result['property']['value'] + ' --- ' + result['item']['value'] + ' --- ' + result['val']['value']) for result in results['results']['bindings']))
