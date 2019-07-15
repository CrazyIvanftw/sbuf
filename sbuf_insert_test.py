import requests
import urllib
import httplib2
import json
from datetime import datetime



# current date and time
now = datetime.now()
timestamp = datetime.timestamp(now)
test_string = 'This is only a test at: %s.' % datetime.fromtimestamp(timestamp)

repository = 'sbuf'
url = 'http://localhost:8080/rdf4j-server/repositories/%s' % (repository)
update_url = 'http://localhost:8080/rdf4j-server/repositories/%s/statements' % (repository)

update = '''PREFIX sbuf: <http://sbuf.org/grasshopper#>
            PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
            PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
            INSERT DATA {
                sbuf:Test sbuf:InsertTest [rdf:value "%s"^^xsd:string].
            } ''' % (test_string)
print('POSTing SPARQL update to %s' % (update_url))

#params = { 'query' : query }
params1 = { 'update' : update }
headers = { 'content-type' : 'application/x-www-form-urlencoded',
            'accept' : 'application/sparql-results+json' }

(response1, content1) = httplib2.Http().request(update_url, 'POST', urllib.parse.urlencode(params1), headers=headers)

print('Update Status %s' % (response1.status))
#print('Content:\n %s' % (content))


query = ''' PREFIX sbuf: <http://sbuf.org/grasshopper#>
            PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
            PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
            SELECT ?val
            WHERE {
              sbuf:Test sbuf:InsertTest [rdf:value ?val].
            }'''

print('POSTing SPARQL query to %s' % (url))
params2 = { 'query' : query }
(response2, content2) = httplib2.Http().request(url, 'POST', urllib.parse.urlencode(params2), headers=headers)
print('Query Status %s' % (response2.status))
results2 = json.loads(content2)
print( '\n'.join(result['val']['value'] for result in results2['results']['bindings']))

#print( '\n')
#print(content)

#r = requests.get(url)

#print(r.headers)
#print(r.text)
#print(r.content)
#print(r)
#with open('comic.png', 'wb') as f:
#    f.write(r.content)
