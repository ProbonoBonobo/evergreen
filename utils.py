#!/usr/local/bin/python3
import os
import signal
import subprocess
import sys
import re
from typing import Callable, Iterable
from crontab import CronTab
from datetime import datetime, time, timedelta
import sched
import math
import random
import io
class timeout:
    def __init__(self, seconds=1, error_message='Timeout'):
        self.seconds = seconds
        self.error_message = error_message
    def handle_timeout(self, signum, frame):
        raise TimeoutError(self.error_message)
    def __enter__(self):
        signal.signal(signal.SIGALRM, self.handle_timeout)
        signal.alarm(self.seconds)
    def __exit__(self, type, value, traceback):
        signal.alarm(0)
class Shell:
    def __init__(self):
        self.github_access_token = "46f76f6db8e7876b7a17417c28fccbb67fe70090"
        self.home = "/Users/kz/Projects/Evergreen3/"
        self.count = 0
        self.has_sudo = False
        self.download_q = []
        self.dependencies = {'git'      : 'not available',
                             'hub'      : 'not available',
                             'crontab'  : 'not available',
                             'launchctl': 'not available',
                             'chmod'    : 'not available',
                             'mkdir'    : 'not available',
                             'rm'       : 'not available'}
        self.on_quit = {'filepaths' : ['/Users/kz/Projects/Evergreen3/.evergreen_data']}
        self.log = []
        self.boot()


    # def then(self, msg):
    #     response = exec_cmd(msg)
    #     assert(response['success'])
    #     return 'ok'
    def boot(self):
        for required_executable in self.dependencies.keys():
            executable_path = self.which(required_executable)
            print("Dependency " + required_executable.upper() + " path is " + executable_path)
            self.dependencies[required_executable] = executable_path

        self.echo("pwd")
        self.goto(".evergreen_data")
        self.echo("pwd")
        self.touch("state.txt")
        self.echo("git add all")
        self.echo("git commit -m \"Updated at " + datetime.now().strftime("%c"))
        self.echo("git push remote origin")
        print("Booted.")

    def update_static_state(self):
        ctr = self.count_commits()
        cmd = "".join([ctr, " > ", "state.txt"])
        self.echo(cmd)

    def commit(self):
        commit_number = self.count_commits()
        cmd = "".join(["git commit -m \"Commit #", commit_number, " finished at ", datetime.now().strftime("%c"), "\""])
        self.exec(cmd)


    def is_exe(self,fpath):
        return os.path.isfile(fpath) and os.access(fpath, os.X_OK)

    def which(self,program):
        fpath, fname = os.path.split(program)
        if fpath:
            if self.is_exe(program):
                return program
        else:
            for path in os.environ["PATH"].split(os.pathsep):
                path = path.strip('"')
                exe_file = os.path.join(path, program)
                if self.is_exe(exe_file):
                    return exe_file

        return None
    def touch(self, fp):
        """
        Emulates the 'touch' command by creating the file at *path* if it does not
        exist.  If the file exist its modification time will be updated.
        """
        with io.open(fp, 'ab'):
            os.utime(fp, None)

    def cat(*strings, sep='', print_output=False):
        catenated = sep.join([str(num) for num in strings])
        if print_output is False:
            return catenated
        print(catenated)
    def exists(url):
        return True if response_code(url) == "200" else False

    def pwd():
        return os.getcwd()

    def cd(dirnam):
        try:
            os.chdir(dirnam)
            cat(show("ls").split("\n"), print_output=True)
        except:
            return 1
        return 0

    def ls(flags):
        cat(shextract("ls" + flags), print_output=True)

    def count_commits(self):
        return shextract("git rev-list --all --count")

    def mkdir(self,fp):
        """
        Emulates the 'touch' command by creating the file at *path* if it does not
        exist.  If the file exist its modification time will be updated.
        """
        os.mkdir(fp)
    def goto(self, fp):
        if self.can_go(fp) is False:
            self.mkdir(fp)
        exit_code = os.chdir(fp)
        return (exit_code, self.pwd())

    def pwd(self):
        return os.getcwd()

    def can_go(self, fp):
        return os.path.exists(fp) and os.path.isdir(fp)

    def mkdir(self, fp):
        if os.path.exists(fp) is False:
            response = self.exec_cmd(" ".join(["mkdir", fp]))
            abspth = os.path.abspath(fp)
            print("Creating a new directory at " +  abspth)
            return response
        return os.path.exists(fp)


    def get_output(self, cmd):
        try:
            out = subprocess.check_output(cmd.split(" "))
        except:
            out = 'Error'
        return out

    def exec_cmd(self, cmd):
        success = True
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE,shell=True)
        stdout, stderr = p.communicate()
        if p.returncode and stderr:
            success = False
            wrapped = {'cmd' : cmd, 'success' : False, 'exit_code':  p.returncode, 'stdout': b'Error!', 'error': stderr}
        else:
            output = self.get_output(cmd)
            wrapped = {'cmd' : cmd, 'success' : True, 'exit_code':  p.returncode, 'stdout': output, 'error': b''}
        self.log.append(wrapped)
        return wrapped

    def last(self):
        return self.log

    def read_log(self):
        for msg in self.log:
            print(msg)

    def echo(self, msg):
        self.exec("echo " + msg)

    def exec(self, cmd):
        response = self.exec_cmd(cmd)
        out = response['stdout']
        decoded = out.decode("utf-8")
        for f in decoded.split("\n"):
            print(f)
        return response

    def initialized(self):
        print("Checking if " + str(os.getcwd())  + " is initialized...")
        response = self.exec_cmd("git rev-parse")
        if response['success']:
            print("It's already initialized!")
            return True
        else:
            print("Not initialized!")
            return False

    def init_repo(self):
        if self.initialized():
            return
        else:
            print("Initializing a repository at " + self.pwd())
            self.echo("git init")
            self.echo("git touch README.md")

    def del_dir(self, fp):
        if fp is not self.home and os.path.isdir(fp):
            print("DELETING DIRECTORY " + fp)
            os.removedirs(fp)

    def del_file(self, fp):
        if os.path.exists(fp) and os.pardir(fp) is not self.home:
            print("DELETING FILE " + fp)
            os.remove(fp)
            def shexec(cmd, timeout_interval=3,error_message="I just crapped my pants", **kwargs):
                """
                Takes: a command-line argument to the user shell, represented as string
                Returns: bash exit code
                """
                try:
                    with timeout(seconds=timeout_interval):
                        exit_code = subprocess.call(cmd.split(" "))
                        return exit_code
                except TimeoutError:
                    return error_message
                return error_message


    def teardown(self):
        if self.initialized():
            print("Destroying the initialized repository " + self.pwd())
            self.echo("rm -rf .git")
        for p in self.on_quit['filepaths']:
            if os.path.isdir(p):
                self.del_dir(p)
            if os.path.isfile(p):
                self.del_file(p)
            else:
                print(p + " deleted.")

def shedcode(data: bytes, format=sys.getdefaultencoding(), trim_whitespace=True) -> str:
    return data.decode(format).rstrip()

def shencode(data: str, format=sys.getdefaultencoding()) -> bytes:
    return data.encode(format)

def shextract(cmd, split_delimiter=False, timeout=3, **kwargs):
    if shexec(cmd) is 0:
        output = subprocess.check_output(cmd.split(" "))
    else:
        output = b"Void"
    if output is None:
        return shedcode(shellshok(cmd))
    decoded = shedcode(output)
    # if split_delimiter:
    #     if split_delimiter == "whitespace":
    #         decoded = decoded.split()
    #     else:
    #         decoded = decododed.split(split_delimiter)
    return decoded

def shellshok(cmd):
    process = subprocess.Popen(cmd.split(" "), stdout=subprocess.PIPE)
    stdout = process.communicate()[0]
    # print('STDOUT:{}'.format(stdout))
    return stdout

def shexec(cmd, timeout_interval=3,error_message="I just crapped my pants", **kwargs):
    """
    Takes: a command-line argument to the user shell, represented as string
    Returns: bash exit code
    """
    try:
        with timeout(seconds=timeout_interval):
            exit_code = subprocess.call(cmd.split(" "))
            return exit_code
    except TimeoutError:
        return error_message
    return error_message

if __name__ == "__main__":
    sh = Shell()
    sh.update_static_state()
# shellshok("git rev-list --all --count")
# shextract("git rev-list --all --count", split_delimiter=False)
