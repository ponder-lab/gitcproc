import sys
import ghProc
import getGitLog
import subprocess
import getpass
import os
import argparse
sys.path.append("../util")

import Util
from Util import ConfigInfo
from Config import Config
'''
Gitcproc.py is the master script, it invokes:
1) The downloads from GitHub
2) Writes the commit logs out
3) Parses and writes the parse to the choosen output format
'''

parser = argparse.ArgumentParser()
parser.add_argument("config_file", help = "This is the path to your configuration file.")
parser.add_argument("-d","--download", action="store_true", help = "Flag that indicates you want to run the step to download the projects.")
parser.add_argument("-wl","--write_log", action="store_true", help = "Flag that indicates you want to run the step to write the logs.")
parser.add_argument("-pl","--parse_log", action="store_true", help = "Flag that indicates you want to run the step to parse the logs.")
parser.add_argument("-p","--password", type = str, default = None, help = "If you are outputting to the database, you must enter your password.")

args = parser.parse_args()

config_file = args.config_file
config_info = ConfigInfo(config_file)

if(config_info.DATABASE and args.parse_log): #If we have database output selected and are performing the parse-log step.
    if args.password is not None:
        password = args.password
    else:
        password = getpass.getpass(prompt="Database option selected, enter your password:")
else:
    password = ""

repo_config = config_info.cfg.ConfigSectionMap("Repos")

if(args.download):
    count = sum(1 for line in open(repo_config['repo_url_file'])) #Default is to read all of them in.

    #Check that the repo list file exists
    if(not os.path.isfile(repo_config['repo_url_file'])):
        print(repo_config['repo_url_file'] + ", the file containing the list of projects to download,")
        print("cannot be found.  Make sure your path and name are correct.")

    #Create the output directory if it doesn't exist yet.
    if(not os.path.isdir(repo_config['repo_locations'])):
        subprocess.call(["mkdir", "-p", repo_config['repo_locations']])

    #Invoke the Java Downloads
    subprocess.call(["java", "-jar", "../../bin/callclone.jar", repo_config['repo_url_file'], repo_config['repo_locations'], "0", str(count), config_info.SEP])

if(args.write_log):
    #Also should include logging for time...
    subprocess.call(["python", "getGitLog.py", repo_config['repo_locations'], config_file])

if(args.parse_log):
    project_set = set()
    if(not os.path.isfile(repo_config['repo_url_file'])):
        print(repo_config['repo_url_file'] + ", the file containing the list of projects to download,")
        print("cannot be found.  Make sure your path and name are correct.")
    else:
        try:
            with open(repo_config['repo_url_file'], 'r') as f:
                for line in f:
                    project_set.add(line.strip().replace("/", config_info.SEP))
        except:
            if(config_info.DEBUG or config_info.DEBUGLITE):
                print("Can't read in repo file, parsing all projects in the directory.")

    #Run ghProc
    dirs_and_names = [(os.path.join(repo_config['repo_locations'], name), name) for name in os.listdir(repo_config['repo_locations']) if os.path.isdir(os.path.join(repo_config['repo_locations'], name))]
    for next_project, name in dirs_and_names:
        if(len(project_set) != 0 and name not in project_set):
            continue
        #subprocess.call(["python", "ghProc.py", next_project, config_file, password])
        subprocess.call(["nohup", "sh", "run.sh", next_project, name, config_file, password])


#Parellel Version:
#p = subprocess.Popen([sys.executable, '/path/to/script.py'],
#                                    stdout=subprocess.PIPE,
#                                    stderr=subprocess.STDOUT)
