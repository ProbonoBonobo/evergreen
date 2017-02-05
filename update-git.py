#!/usr/local/bin/python3
import os
import signal
import subprocess
import sys
import re
from datetime import datetime, time, timedelta
import math
import random
import json
import io
from generate import make_issue


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
        self.home = "/Users/kz/Projects/Evergreen4/"
        self.count = 0
        self.has_sudo = False
        self.download_q = []
        self.issues = {'open' : [], 'closed': []}
        self.dependencies = {'ghi'      : 'not available',
                             'git'      : 'not available',
                             'hub'      : 'not available',
                             'crontab'  : 'not available',
                             'launchctl': 'not available',
                             'chmod'    : 'not available',
                             'mkdir'    : 'not available',
                             'rm'       : 'not available'}
        self.on_quit = {'filepaths' : ['/Users/kz/Projects/Evergreen4/.evergreen_data']}
        self.log = []
        self.boot()


    # def then(self, msg):
    #     response = exec_cmd(msg)
    #     assert(response['success'])
    #     return 'ok'
    def boot(self):
        self.goto("/Users/kz/Projects/Evergreen4")
        for required_executable in list(self.dependencies.keys()):
            executable_path = self.which(required_executable)
            print("Dependency " + str(required_executable.upper()) + " path is " + str(executable_path))
            self.dependencies[required_executable] = executable_path
        self.goto("/Users/kz/Projects/Evergreen4")
        if self.issues['open']:
            self.close_all_open_issues()
        self.create_issue()


        self.echo("pwd")
        self.goto(".evergreen_data")
        self.echo("pwd")
        self.touch("state.txt")
        self.touch("logfile.log")
        self.echo("git add .")
        self.update_static_state()
        self.commit()
        self.push()
        self.write_log()


    def update_static_state(self):
        ctr = self.count_commits()
        cmd = cat(ctr, " > ", "state.txt")
        self.echo(cmd)

    def commit(self):
        commit_number = self.count_commits()
        self.exec_cmd("git add .")
        self.exec_cmd("git commit . -m \"State update\"")

    def issues_labeled(self,label="all"):
        if label != "all":
            context = self.exec_cmd("/usr/local/bin/ghi list --label=" + str(label))
        else:
            context = self.exec_cmd("/usr/local/bin/ghi list --global")
        output = context['stdout']
        patt = re.compile(r"(?:\s*)(\d+)(?:\W\s)")
        matches = re.findall(patt,output)
        return matches

    def create_issue(self):
        issue_title = make_issue()
        context = self.exec_cmd("".join(["\"$(/usr/local/bin/ghi open -m  \'", issue_title, "\n(automatically generated)\' )\""]))
        print(context['stdout'])

    def open_issues(self):
        context = self.exec_cmd("/usr/local/bin/ghi list")
        output = context['stdout']
        patt = re.compile(r"(?:\s*)(\d+)(?:\W\s)")
        issue_numbers = re.findall(patt,output)
        self.issues['open'] = issue_numbers
        return self.issues['open']

    def closed_issues(self):
        context = self.exec_cmd("/usr/local/bin/ghi list --closed")
        output = context['stdout']
        patt = re.compile(r"(?:\s*)(\d+)(?:\W\s)")
        closed_issues = re.findall(patt,output)
        self.issues['closed'] = closed_issues
        return self.issues

    def close_all_open_issues(self):
        open_issues = self.open_issues()
        if open_issues:
            for issue_id in open_issues:
                print("Closing issue " + str(issue_id) + "...")
                self.exec_cmd("/usr/local/bin/ghi close " + issue_id)
        print("Open issues:")
        print(self.open_issues())


    def reopen_issue(self, issue_id="random"):
        closed_issues = self.closed_issues()
        if issue_id == "random":
            issue_id = random.choice(closed_issues)
        if issue_id in closed_issues:
            print("Reopening issue " + str(issue_id) + "...")
            self.exec_cmd("/usr/local/bin/ghi reopen " + issue_id)
            print("Open issues:")
            print(self.open_issues())

    def close_issue(self, issue_id="random"):
        open_issues = self.open_issues()
        if issue_id == "random":
            issue_id = random.choice(open_issues)
        if issue_id in open_issues:
            print("Closing issue " + str(issue_id) + "...")
            self.exec_cmd("/usr/local/bin/ghi close " + issue_id)
            print("Open issues:")
            print(self.open_issues())




    def push(self):
        self.exec_cmd("git push origin master")


    def get_remote_name(self):
        remote_name =  shextract("git rev-parse --abbrev-ref --symbolic-full-name @{u}")
        if isinstance(remote_name, bytes):
            remote_name = remote_name.decode(sys.getdefaultencoding())
        return remote_name.strip()

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
        return cat(shextract("ls" + flags), print_output=True)


    def count_commits(self):
        ctr = self.exec_cmd("git rev-list --all --count")
        if hasattr(ctr, 'stdout') and isinstance(ctr['stdout'], bytes):
            ctr['stdout'] = ctr['stdout'].decode(sys.getdefaultencoding())
        return ctr['stdout']

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
            wrapped = {'cmd' : cmd, 'success' : "False", 'exit_code':  str(p.returncode), 'stdout': 'Error!', 'error': stderr}
        else:
            output = self.get_output(cmd)
            wrapped = {'cmd' : cmd, 'success' : "True", 'exit_code':  str(p.returncode), 'stdout': output, 'error': ''}

        for key, val in wrapped.items():
            if isinstance(val, bytes):
                wrapped[key] = val.decode("utf-8").rstrip()
        self.log.append(wrapped.items())
        return wrapped
    def last(self):
        return self.log

    def read_log(self):
        for line in self.log:
            for tup in line:
                print(tup[0], "=", tup[1])
            print("\n")

    def write_log(self):
        with open("logfile.txt", "w") as f:
            for line in self.log:
                msg = ["{"]
                for tup in line:
                    val = "".join(["'", tup[1], "'"])
                    msg.append("".join([tup[0], " : ", val ]))
                msg.append("}")
                f.write(", ".join(msg))
                f.write(", \n")



    def echo(self, msg):
        self.exec("echo " + msg)

    def exec(self, cmd):
        response = self.exec_cmd(cmd)
        out = response['stdout']
        if out and isinstance(out, bytes):
            out = out.decode(sys.getdefaultencoding())
        for f in out.split("\n"):
            print(f)
        return out

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
    if output is bytes:
        return shedcode(output)
    return output
    # if split_delimiter:
    #     if split_delimiter == "whitespace":
    #         decoded = decoded.split()
    #     else:
    #         decoded = decododed.split(split_delimiter)

def cat(*strings, sep='', print_output=False):
    catenated = sep.join([str(num) for num in strings])
    if print_output is False:
        return catenated
    print(catenated)

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

# class CronDaemon():
#     from crontab import CronTab
#     def __init__(self):
#         self.cron = CronTab(user=True)
#     def print(self):
#         for job in self.cron:
#             print(job)
#     def add(self,cmd="/usr/local/bin/python3 /Users/kz/Projects/Evergreen4/utils.py"):
#         job = self.cron.new(command=cmd, comment='evergreen')
#         job.setall("* * * * *")
#         job.enable()
#         assert(True==job.is_valid())
#         self.cron.write_to_user( user=True )
#         self.cron.write()
#     def cancel_all(self):
#         self.cron.remove_all(comment='evergreen')
#         self.cron.write_to_user( user=True )

if __name__ == "__main__":
    sh = Shell()
    sh.update_static_state()
    # sh.commit()
    # sh.push()
    sh.read_log()
    sh.write_log()

# shellshok("git rev-list --all --count")
# shextract("git rev-list --all --count", split_delimiter=False)
