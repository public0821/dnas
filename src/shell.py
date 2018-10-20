import logging
import os
import subprocess
import shlex
import shutil
from exceptions import Error

class CallError(Error):
    pass

def system(cmd):
    return subprocess.call(cmd, shell=True)
    
#run batch commands, raise exception if any commands failed.
def run_commands(commands, shell=False):
    for command in commands:
        run_command(command, shell=shell)

def run_command(cmd, cwd=None, shell=False):
    output = getoutput(cmd, shell=shell, cwd=cwd)
    if output:
        logging.debug(_("output of command '{}': {}").format(cmd, output))

#run a command and return the output of the command
#raise exception if command exit with error code
def getoutput(command, shell=False, check=True, cwd=None):
    args = command if shell else shlex.split(command)
    try:
        output = subprocess.check_output(args, stderr=subprocess.STDOUT, cwd=cwd, shell=shell)
        return output.decode().strip()
    except subprocess.CalledProcessError as e:
        output = e.output.decode().strip()
        if check:
            raise CallError(_("run '{}' failed: {}").format(command, output))
        else:
            logging.warning(e) 
            return output

def check_command(command, shell=False, cwd=None):
    args = command if shell else shlex.split(command)
    try:
        subprocess.check_output(args, stderr=subprocess.STDOUT, cwd=cwd, shell=shell)
        return True
    except subprocess.CalledProcessError as e:
        logging.debug(e) 
        return False
