import os
import shutil
import subprocess

__author__ = 'Andreas Bader'
__version__ = "0.01"


def check_file_readable(filename):
    if check_file_exists(filename) and os.access(filename, os.R_OK):
        return True
    return False


def check_file_exists(filename):
    if os.path.isfile(filename):
        return True
    return False


# Check if folder exists
def check_folder(path, logger, reverse_logic=False, no_error=False):
    if not(os.path.isdir(path) and os.path.exists(path)):
        if not reverse_logic:
            if not no_error:
                logger.error("%s does not exist." % path)
            return False
        else:
            return True
    if not reverse_logic:
        return True
    else:
        if not no_error:
            logger.error("%s does exist." % path)
        return False


def delete_folder(path, logger, no_error=False):
    if check_folder(path, logger):
        try:
            shutil.rmtree(path)
        except OSError:
            logger.warning('Failed to delete %s.' % path, exc_info=True)
            return False
        return True
    else:
        if no_error:
            return True
        return False


def delete_file(path, logger, no_error=False):
    if os.path.isfile(path):
        try:
            os.remove(path)
        except OSError:
            logger.error('Failed to remove file', exc_info=True)
            return False
        return True
    else:
        if no_error:
            return True
        return False


def copy_folder(path1, path2, logger):
    try:
        shutil.copytree(path1, path2, symlinks=False, ignore=None)
    except OSError:
        logger.error('Failed to copy %s to %s.' % (path1, path2), exc_info=True)
        return False
    return True


def copy_file(path1, path2, logger):
    try:
        shutil.copyfile(path1, path2)
    except OSError:
        logger.error('Failed to copy %s to %s.' % (path1, path2), exc_info=True)
        return False
    return True


def clean_space(line):
    string = line
    while string[0] == ' ':
        string = string[1:]
    while string[-1] == ' ':
        string = string[:-1]
    return string


def clean_quote(line):
    string = line
    while string[0] == '\'':
        string = string[1:]
    while string[-1] == '\'':
        string = string[:-1]
    while string[0] == '\"':
        string = string[1:]
    while string[-1] == '\"':
        string = string[:-1]
    return string


def clean_newline(line):
    string = line
    while string[0] == '\n':
        string = string[1:]
    while string[-1] == '\n':
        string = string[:-1]
    return string


def clean_newline_space(line):
    string = line
    while string[0] == '\n' or string[0] == ' ':
        string = string[1:]
    while string[-1] == '\n' or string[-1] == ' ':
        string = string[:-1]
    return string


def clean_quote_space(line):
    string = line
    while string[0] == '\'' or string[0] == ' ':
        string = string[1:]
    while string[-1] == '\'' or string[-1] == ' ':
        string = string[:-1]
    return string


def create_folder(folder):
    try:
        os.makedirs(folder)
    except OSError:
        return False
    return True


def get_script_path():
    return os.path.dirname(os.path.realpath(__file__))


def cmd_exists(cmd):
    return subprocess.call("type " + cmd, shell=True,
                           stdout=subprocess.PIPE, stderr=subprocess.PIPE) == 0


def run_cmd(cmd, logger, return_output=False, no_error=False):
    process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, err = process.communicate()
    if not no_error and process.returncode != 0:
        logger.error("Command '%s' returned %s with the following output: '%s' and the following error output: '%s'"
                     % (cmd, process.returncode, output, err))
    if not return_output:
        return process.returncode == 0
    else:
        if process.returncode == 0:
            return output
        else:
            return None
