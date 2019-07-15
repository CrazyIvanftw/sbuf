Work Update:
1) rdf4j server installed on personal computer
2) most grasshopper parameters are hardcoded in rdf4j database (see sbuf_sparql_init_2.rq)
3) suggestions for standard queries to DB have been written (see std_queries.rq) and are awaiting your thoughts
4) basic 'Create' and 'Read' functionality with REST api working (see sbuf_query_test.py and sbuf_insert_test.py)

Current Issues:
1) server not installed on lab machine
  - Anders Nilsson and I have not been in the lab at the same time yet so I haven't had a chance to figure out why I can't login to the lab machine.

2) There are some grasshopper parameters that have not been hardcoded
  - problem : there are several parameters that are an ordered series of BREP (boundary representation) files. This type of file is difficult to handle in rdf.
    * solution?: there is an rdf onthology called 'OntoBREP' for working with BREP files, but I have not gotten it working yet.
    * solution?: serialize and de-serialize the BREP files locally and save them in the DB as a byte-stream
  - problem: I can't figure out how to access the data from two parameters (a 4x4 matrix called 'M' and a curve called 'TCP').
    * solution?: Get Henrik to help me figure out how to get at the numbers at some point?

3) 'Update' and 'Delete' functionality not implemented for DB yet via REST api
  - I just haven't gotten around to it yet, that's next on my to-do list

4) Have not mounted sensors into the robot yet.
  - I just haven't gotten around to it yet, that's next on my to-do list

Considerations:
1) My understanding was that you planned for about a week's worth of work to be done on this. As of today, I went over 40 hours of working on this in total. I don't want to do too much more before I get your approval.
2) I think it would be worth figuring out how to serialize and de-serialize BREP files for DB storage. The reason is that method would probably also be useful for storing RAPID files and sensor data.
Time estimates:
1) install server and DB onto lab machine (2h once Anders and I figure out how to get me logged in)
2) finish 'Update' and 'Delete' functionality (4h)
3) save BREP files to DB (8h)
4) save matrix and curve parameters to DB (2h once I have access to the grasshopper data)
5) mount sensors (8h)

Explanation of current DB structure:
The basic idea right now is that the graph of grasshopper parameters looks like this:

sbuf:SaveFile -> sbuf:parameter ->  blank_node
                                    blank_node -> rdf:value -> data
                                    ...
                                    blank_node -> sbuf:GroupTag -> "some tag"

That is to say, I've made the graph two nodes deep from a root node that is the 'file name'.
Unfortunately, rdf doesn't like it when its 'subject' in the 'subject' -> 'predicate' -> 'object' structure is a string literal.
That means that we're gonna have to save the files as something like sbuf:SaveFile3 or something. It shouldn't be an issue, but I wanted to say it.  
