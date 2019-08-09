
def sparql_target(name, x, y, z, q1, q2, q3, q4, cf1, cf4, cf6, cfx, eax_a, eax_b, eax_c, eax_d, eax_e, eax_f):
    '''Given the parameters of a robtarget, this function returns a sparql statement for storing that target in an rdf4j database.'''
    line1 = "\n\t \t sbuf:QiruiTargets   abb:robtarget  [ \n"
    line2 = "\t \t \t \t abb:name  [ \n \t \t \t \t \t \t abb:string \"{}\"^^xsd:string ] ;\n".format(name)
    line3 = "\t \t \t \t abb:pos [ \n \t \t \t \t \t \t abb:trans_x \"{}\"^^xsd:double ; \n \t \t \t \t \t \t abb:trans_y \"{}\"^^xsd:double ; \n \t \t \t \t \t \t abb:trans_z \"{}\"^^xsd:double  ] ;\n".format(x, y, z)
    line4 = "\t \t \t \t abb:orient [ \n \t \t \t \t \t \t abb:rot_q1 \"{}\"^^xsd:double ; \n \t \t \t \t \t \t abb:rot_q2 \"{}\"^^xsd:double ; \n \t \t \t \t \t \t abb:rot_q3 \"{}\"^^xsd:double ; \n \t \t \t \t \t \t abb:rot_q4 \"{}\"^^xsd:double  ] ;\n".format(q1, q2, q3, q4)
    line5 = "\t \t \t \t abb:confdata [ \n \t \t \t \t \t \t abb:robconf_cf1 \"{}\"^^xsd:double ; \n \t \t \t \t \t \t abb:robconf_cf4 \"{}\"^^xsd:double ; \n \t \t \t \t \t \t abb:robconf_cf6 \"{}\"^^xsd:double ; \n \t \t \t \t \t \t abb:robconf_cfx \"{}\"^^xsd:double  ] ;\n".format(cf1, cf4, cf6, cfx)
    line6 = "\t \t \t \t abb:extjoint [ \n \t \t \t \t \t \t abb:extax_eax_a \"{}\"^^xsd:string ; \n \t \t \t \t \t \t abb:extax_eax_b \"{}\"^^xsd:string ; \n \t \t \t \t \t \t abb:extax_eax_c \"{}\"^^xsd:string ; \n \t \t \t \t \t \t abb:extax_eax_d \"{}\"^^xsd:string ; \n \t \t \t \t \t \t abb:extax_eax_e \"{}\"^^xsd:string ; \n \t \t \t \t \t \t abb:extax_eax_f \"{}\"^^xsd:string  ] \n".format(eax_a, eax_b, eax_c, eax_d, eax_e, eax_f)
    line7 = "\t \t ]"
    target = line1 + line2 + line3 + line4 + line5 + line6 + line7
    #print("Target {} constructed".format(name))
    return target

def sparql_target_no_external_joints(name, x, y, z, q1, q2, q3, q4, cf1, cf4, cf6, cfx):
    '''Given the parameters of a robtarget, this function returns a sparql statement for storing that target in an rdf4j database.
        Note: This function assumes no external joints for the target.'''
    line1 = "\n\t \t sbuf:QiruiTargets   abb:robtarget  [ \n"
    line2 = "\t \t \t \t abb:name  [ \n \t \t \t \t \t \t abb:string \"{}\"^^xsd:string ] ;\n".format(name)
    line3 = "\t \t \t \t abb:pos [ \n \t \t \t \t \t \t abb:trans_x \"{}\"^^xsd:double ; \n \t \t \t \t \t \t abb:trans_y \"{}\"^^xsd:double ; \n \t \t \t \t \t \t abb:trans_z \"{}\"^^xsd:double  ] ;\n".format(x, y, z)
    line4 = "\t \t \t \t abb:orient [ \n \t \t \t \t \t \t abb:rot_q1 \"{}\"^^xsd:double ; \n \t \t \t \t \t \t abb:rot_q2 \"{}\"^^xsd:double ; \n \t \t \t \t \t \t abb:rot_q3 \"{}\"^^xsd:double ; \n \t \t \t \t \t \t abb:rot_q4 \"{}\"^^xsd:double  ] ;\n".format(q1, q2, q3, q4)
    line5 = "\t \t \t \t abb:confdata [ \n \t \t \t \t \t \t abb:robconf_cf1 \"{}\"^^xsd:double ; \n \t \t \t \t \t \t abb:robconf_cf4 \"{}\"^^xsd:double ; \n \t \t \t \t \t \t abb:robconf_cf6 \"{}\"^^xsd:double ; \n \t \t \t \t \t \t abb:robconf_cfx \"{}\"^^xsd:double  ] ;\n".format(cf1, cf4, cf6, cfx)
    line6 = "\t \t \t \t abb:extjoint [ \n \t \t \t \t \t \t abb:extax_eax_a \"{}\"^^xsd:string ; \n \t \t \t \t \t \t abb:extax_eax_b \"{}\"^^xsd:string ; \n \t \t \t \t \t \t abb:extax_eax_c \"{}\"^^xsd:string ; \n \t \t \t \t \t \t abb:extax_eax_d \"{}\"^^xsd:string ; \n \t \t \t \t \t \t abb:extax_eax_e \"{}\"^^xsd:string ; \n \t \t \t \t \t \t abb:extax_eax_f \"{}\"^^xsd:string  ] \n".format("9E+09", "9E+09", "9E+09", "9E+09", "9E+09", "9E+09")
    line7 = "\t \t ]"
    target = line1 + line2 + line3 + line4 + line5 + line6 + line7
    #print("Target {} constructed".format(name))
    return target

def sparql_insert_seperate_params(*data):
    '''given some number of sparql statements corresponding to data that nees to be inserted, this will wrap every data string
        in an INSERT statement and return one string that can be used via the rdf4j REST API'''
    prefix = '''PREFIX sbuf: <http://sbuf.org/grasshopper#>\nPREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>\nPREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>\nPREFIX xsd: <http://www.w3.org/2001/XMLSchema#>\nPREFIX abb: <http://FakePlaceholderABB.com/RAPID#>
    \nINSERT DATA {
    \n\t GRAPH <sbuf:GripperTargets>{
    '''
    last = "\n\t} \n}"
    statement = prefix
    counter = 1
    for target in data:
        if counter == len(data):
            statement = statement + target + " .\n"
        else:
            statement = statement + target + " ;\n"
        counter = counter + 1
    statement = statement + last
    return statement

def sparql_insert_list_params(data):
    '''given some number of sparql statements corresponding to data that nees to be inserted, this will wrap every data string
        in an INSERT statement and return one string that can be used via the rdf4j REST API'''
    prefix = '''PREFIX sbuf: <http://sbuf.org/grasshopper#>\nPREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>\nPREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>\nPREFIX xsd: <http://www.w3.org/2001/XMLSchema#>\nPREFIX abb: <http://FakePlaceholderABB.com/RAPID#>
    \nINSERT DATA {
    \n\t GRAPH <sbuf:GripperTargets>{
    '''
    last = "\n\t} \n}"
    statement = prefix
    #counter = 1
    for target in data:
        statement = statement + target + " .\n"
        #if counter == len(data):
        #    statement = statement + target + " .\n"
        #else:
        #    statement = statement + target + " ;\n"
        #counter = counter + 1
    statement = statement + last
    return statement

def parse_rapid_file(file_name):
    '''given a rapid file, will return a dictionary containing the params of every robtarget object mapped by the param name.
        Note: At the moment, the expected input format is very touchey. Should make more robust in the future, but no time now.'''
    rapid = open(file_name, "r+")
    lines = rapid.readlines()
    targets = []
    for line in lines:
        robtarget_start = line.find("robtarget")
        if robtarget_start != -1 :
            name_end = line.find(":=")
            name = line[robtarget_start+10:name_end]
            data = line[name_end+4:len(line)-4].split("],[")
            trans = data[0].split(",")
            rot = data[1].split(",")
            robconf = data[2].split(",")
            extax = data[3].split(",")
            t = {
                "name" : name,
                "x" : trans[0], "y" : trans[1], "z" : trans[2],
                "q1" : rot[0], "q2" : rot[1], "q3" : rot[2], "q4" : rot[3],
                "cf1" : robconf[0], "cf4" : robconf[1], "cf6" : robconf[2], "cfx" : robconf[3],
                "eax_a" : extax[0], "eax_b" : extax[1], "eax_c" : extax[2], "eax_d" : extax[3], "eax_e" : extax[4], "eax_f" : extax[5]
            }
            targets.append(t)
    rapid.close()
    return targets

if __name__ == '__main__':
    targets = parse_rapid_file("HardcodedTargets.mod")
    sparql_targets = []
    for target in targets:
        sparql_target = sparql_target_no_external_joints(target["name"], target["x"], target["y"], target["z"], target["q1"], target["q2"], target["q3"], target["q4"], target["cf1"], target["cf4"], target["cf6"], target["cfx"])
        sparql_targets.append(sparql_target)

    sparql_insert_statement = sparql_insert_list_params(sparql_targets)
    print(sparql_insert_statement)
