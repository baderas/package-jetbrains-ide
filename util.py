__author__ = 'Andreas Bader'
__version__ = "0.01"

import os
import shutil
import subprocess

def check_file_readable(filename):
    if check_file_exists(filename) and os.access(filename, os.R_OK):
        return True
    return False

def check_file_exists(filename):
    if os.path.isfile(filename):
        return True
    return False

# Check if folder exists
def check_folder(path,logger,reverseLogic=False, noError=False):
    if not(os.path.isdir(path) and os.path.exists(path)):
        if not reverseLogic:
            if not noError:
                logger.error("%s does not exist." %(path))
            return False
        else:
            return True
    if not reverseLogic:
        return True
    else:
        if not noError:
            logger.error("%s does exist." %(path))
        return False

def delete_folder(path,logger,no_error=False):
    if check_folder(path,logger):
        try:
            shutil.rmtree(path)
        except Exception:
            logger.warning('Failed to delete %s.' %(path), exc_info=True)
            return False
        return True
    else:
        if no_error:
            return True
        return False

def delete_file(path,logger,no_error=False):
    if os.path.isfile(path):
        try:
            os.remove(path)
        except Exception:
            logger.error('Failed to remove file', exc_info=True)
            return False
        return True
    else:
        if no_error:
            return True
        return False


def copy_folder(path1,path2,logger):
    try:
        shutil.copytree(path1, path2, symlinks=False, ignore=None)
    except Exception:
        logger.error('Failed to copy %s to %s.' %(path1,path2), exc_info=True)
        return False
    return True

def copy_file(path1,path2,logger):
    try:
        shutil.copyfile(path1,path2)
    except Exception:
        logger.error('Failed to copy %s to %s.' %(path1,path2), exc_info=True)
        return False
    return True

def clean_space(line):
    str = line
    while str[0] == ' ':
        str = str[1:]
    while str[-1] == ' ':
        str = str[:-1]
    return str

def clean_quote(line):
    str = line
    while str[0] == '\'':
        str = str[1:]
    while str[-1] == '\'':
        str = str[:-1]
    while str[0] == '\"':
        str = str[1:]
    while str[-1] == '\"':
        str = str[:-1]
    return str

def clean_newline(line):
    str = line
    while str[0] == '\n':
        str = str[1:]
    while str[-1] == '\n':
        str = str[:-1]
    return str

def clean_newline_space(line):
    str = line
    while str[0] == '\n' or str[0] == ' ':
        str = str[1:]
    while str[-1] == '\n' or str[-1] == ' ':
        str = str[:-1]
    return str

def clean_quote_space(line):
    str = line
    while str[0] == '\'' or str[0] == ' ':
        str = str[1:]
    while str[-1] == '\'' or str[-1] == ' ':
        str = str[:-1]
    return str

def create_folder(folder):
    try:
        os.makedirs(folder)
    except:
        return False
    return True

def get_script_path():
    return os.path.dirname(os.path.realpath(__file__))

def cmd_exists(cmd):
    return subprocess.call("type " + cmd, shell=True,
        stdout=subprocess.PIPE, stderr=subprocess.PIPE) == 0

def run_cmd(cmd, logger, returnOutput = False):
    process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, err = process.communicate()
    if process.returncode != 0:
        logger.error("Command '%s' returned %s with the following output: '%s' and the following error output: '%s'"
                     %(cmd, process.returncode, output, err))
    if not returnOutput:
        return process.returncode == 0
    else:
        if process.returncode == 0:
            return output
        else:
            return None