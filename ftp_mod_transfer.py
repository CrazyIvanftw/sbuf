from ftplib import FTP
import os
import fileinput
import sys

# This script will transfer a file to the mod_transfers folder of the LTH2400
# controller. The command line arguments are the user, password, and filename.
# The desired file is expected to be in the same directory as the script, so
# if it is not, use an absolute path name an argument. 

#filename = 'ftpTargets.mod'

def ftp_transfer(user, password, file_name):
    ftp = FTP()
    ftp.set_debuglevel(2)
    ftp.connect('192.168.66.167', 21)
    ftp.login(user, password)
    ftp.cwd('/hd0a/LTH2400_RW608/HOME/mod_transfers')
    ftp.storbinary('STOR '+file_name, open(file_name, 'rb'))
    ftp.quit()

if __name__ == '__main__':
    user = sys.argv[1]
    password = sys.argv[2]
    filename = sys.argv[3]
    ftp_transfer(user, password, filename)
