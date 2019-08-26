import os
import fileinput
import sys
import requests
import errno
import time
from ftplib import FTP
from bs4 import BeautifulSoup

irb240_url = "192.168.66.167"
username = "greg"
passwd = "gregspassword"
auth = requests.auth.HTTPDigestAuth(username, passwd)
session = requests.Session()

class ABBException(Exception):
    def __init__(self, message, code):
        super(ABBException, self).__init__(message)
        self.code=code

def ftp_transfer(filename, user=username, password=passwd):
    ftp = FTP()
    ftp.set_debuglevel(2)
    ftp.connect(irb240_url, 21)
    ftp.login(user, password)
    ftp.cwd('/hd0a/LTH2400_RW608/HOME/mod_transfers')
    ftp.storbinary('STOR '+filename, open(filename, 'rb'))
    ftp.quit()

def ftp_retrieve(filename, local_filename, user=username, password=passwd):
    ftp = FTP()
    ftp.set_debuglevel(2)
    ftp.connect(irb240_url, 21)
    ftp.login(user, password)
    ftp.cwd('/hd0a/LTH2400_RW608/HOME/mod_finished')
    with open(local_filename, 'wb') as f:
        ftp.retrbinary('RETR %s' % filename, f.write)
    ftp.delete(filename)
    ftp.quit()

def rapid_bool(string_bool):
    return string_bool.upper() == "TRUE"

def _process_response(response):
    soup=BeautifulSoup(response.text, features="lxml")

    if (response.status_code == 500):
        raise Exception("Robot returning 500 Internal Server Error")

    if (response.status_code == 200 or response.status_code == 201  \
        or response.status_code==202 or response.status_code==204):

        return soup.body

    if soup.body is None:
        raise Exception("Robot returning HTTP error " + str(response.status_code))

    error_code=int(soup.find('span', attrs={'class':'code'}).text)
    error_message1=soup.find('span', attrs={'class': 'msg'})
    if (error_message1 is not None):
        error_message=error_message1.text
    else:
        error_message="Received error from ABB robot: " + str(error_code)

    raise ABBException(error_message, error_code)

def _do_get(relative_url):
    url="/".join(["http://"+irb240_url, relative_url])
    res=session.get(url, auth=auth)
    try:
        return _process_response(res)
    finally:
        res.close()

#THIS DOESN'T WORK. LOGIN ISSUE
def _do_post(relative_url, payload):
    url="/".join(["http://"+irb240_url, relative_url])
    params = {"action": "set"}
    res=session.post(url, params=params, data=payload, auth=auth)
    try:
        return _process_response(res)
    finally:
        res.close()

def get_rapid_variable(var):
    soup = _do_get("rw/rapid/symbol/data/RAPID/T_ROB1/" + var)
    state = soup.find('span', attrs={'class': 'value'}).text
    return state

#THIS DOESN'T WORK AT THE MOMENT. THERE IS A LOGIN ISSUE
def set_rapid_variable(var, value):
    payload={'value': value}
    _do_post("rw/rapid/symbol/data/RAPID/T_ROB1/" + var, payload)


#PERS string module_to_find := "new.mod";
#PERS string module_to_load := "next.mod";
#PERS string module_proc_to_run := "main";
#PERS string last_module_run := "none";
#PERS bool bool_variable := TRUE;



if __name__ == '__main__':
    module_name = get_rapid_variable("module_to_find").strip('"')
    #print("sending: " + module_name)
    ftp_transfer(module_name)
    retrieved = False
    #print("Waiting for file to retrieve...")
    while not retrieved:
        get_module_name = get_rapid_variable("last_module_run").strip('"')
        if get_module_name == "none":
            #print("\t ...still waiting...")
            # Wait for 200 milliseconds
            time.sleep(.200)
        else:
            #print("retrieving: " + get_module_name)
            ftp_retrieve(get_module_name, get_module_name)
            retrieved = True
    #print("done")
