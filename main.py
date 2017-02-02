#!/usr/local/bin/python3
import io
import os
import subprocess
import sys
import time
from subprocess import call, check_output
import functools
from typing import Iterable
import math
import random

parentDirectory = "/Users/kz/Projects/Evergreen3"
sys.path.append("/Users/kz/Projects/Evergreen3")
from utils import exists, isDirectory, isFile, isUrl, response_code, shexec, touch, pwd, cat, shextract, shedcode,shencode, shedcode, cd, ls, pwd, mapreduce


class SM:
    corral = {}

    def register(self, name, obj):
        self.corral['name'] = obj
        return self.corral['name']

    def checkout(self, name):
        if hasattr(self.corral, name):
            return eelf.corral[name]
        return False

    def start(self, verbose=False):

        if verbose:
            print("Start state: " + str(self.startState))
        self.state = self.startState

    def step(self, inp, verbose=False,  sleep_interval=1):
        (s, o) = self.getNextValues(self.getState(), self.getInput())
        self.state = s
        time.sleep(1)
        turnstileNavigator.giveToken(self.getInput())
        if verbose:
            msg = " ".join(
                (str(i) for i in ["In:", s, " Out:", o, " Next State: ", self.state]))
            print(msg)
        return o

    def transduce(self, inputs, verbose=False, sleep_interval=1):
        self.start(verbose)
        return [self.step(self.getInput(), verbose) for inp in inputs]

    def run(self, n=10, verbose=None, sleep_interval=1):
        if verbose is None and hasattr(self, 'verbose'):
            verbose = self.verbose
        return self.transduce([None] * n, verbose)

    def makeCounter(init, step):
        return sm.Feedback(sm.Cascade(Increment(step), sm.Delay(init)))

    def create_repository(visibility='private'):
        is_private = lambda x: x == 'private'
        api_call = "".join(
            ["curl -u 'USER:myInsecureGithubPassword' https://api.github.com/user/repos -d '{\"name\":\"REPO\", \"private\":\"", is_private(visibility), "\"}'"])
        exec_all(api_call)

    def path_to(target):
        return app_state['path_to'][target]

    def validate_paths(filepaths):
        return all(map(lambda target: os.path.exists(path_to(target)), filepaths))


class Turnstile(SM):
    startState = 0

    def __init__(self, startingState=startState):
        self.prevState = None
        self.state = startingState

    def getState(self):
        return 'Green' if self.state is 1 else 'Red'

    def insertToken(self, pathwalker, token, verbose=True):
        # print(str(token))
        self.prevState = self.state
        self.state = 1 if token.callback(pathwalker) is True else 0
        if verbose:
            print("Start: " + str(self.prevState) + " Input: " +
                  str(token) + " Output: " + str(self.state))
        return (self.prevState, self.state)


class TurnstileNavigator(SM):
    startState = 0

    def __init__(self, startingState=startState):
        self.prevState = None

        self.state = startingState
        self.token = []
        self.turnstile = Turnstile
        self.verbose = True

    def kill(self):
        print("Turnstile Navigator instance got stuck at " + str(date.time()))

    def getState(self):
        if self.prevState is 0 and self.state is 0:  # blocked?
            self.kill()
        elif self.state is 1:
            return 'Departing'
        else:
            return 'Arrived'

    def getInput(self, philter=None):
        if len(self.token) > 0:
            t = self.token[len(self.token)]
            return t

    def nextTime(rateParameter):
        return -math.log(1.0 - random.random()) / rateParameter

    def dispatch(self, msg):
        # inputs: "setup git repository", "load last_update", "update
        # countdown", "update schedule", "update_daemon"
        dispatchingOn = ["pass", "setup git repository"]
        if msg not in dispatchingOn:
            return False
        opcode = dispatchingOn.index(msg)
        if opcode is 0:
            pass
        elif opcode is 1:
            create_repository()
        elif opcode is 2:
            if hasattr(app_state, 'arrivals'):
                app_state['arrivals'].append(nextTime(1/90))







    def giveToken(self, token):
        self.token.append(token)
        self.leave(self.state, self.token.pop())

    def leave(self, state, token):

        transition = turnstile.insertToken(self, token)
        self.prevState = transition[0]
        self.state = transition[1]


class Config(SM):

    def __init__(self, deserialized):
        self.data = deserialized

    def get(self, k):
        return self.data[k]

    def extend(self, k, v):
        self.data[k] = v
        return 'ok'

    def update(self, kv):
        self.data.update(kv)
        return 'ok'


class PathConstructor(Config):
    startState = 'loading'
    statusVec = ['creating', 'loading', 'updating']

    def __init__(self, env, startState=startState, verbose=True):
        self.pos = 0
        self.env = env
        self.state = startState
        self.verbose = verbose

    def toggle(flag):
        if "-v" in flag:
            self.verbose = not self.verbose

    def getPos(self):
        return self.pos

    def getInput(self, philter=None):
        curr = self.env.get('path_seq')[self.getPos()]
        if philter in range(0, len(curr)):
            return curr[philter]
        return curr

    def getPath(self):
        return self.getInput(2)
    #
    # @staticmethod
    # def isFile(inp: tuple):
    #     return inp.resource_type == 'file'
    #
    # @staticmethod
    # def isDirectory(inp: tuple):
    #     return inp.resource_type == 'directory'
    #
    # @staticmethod
    # def touch(inp: tuple):
    #     """
    #     Emulates the 'touch' command by creating the file at *path* if it does not
    #     exist.  If the file exist its modification time will be updated.
    #     """
    #     path = inp[2]
    #     with io.open(path, 'ab'):
    #         os.utime(path, None)

    # @staticmethod
    # def mkdir(inp: tuple):
    #     """
    #     Emulates the 'touch' command by creating the file at *path* if it does not
    #     exist.  If the file exist its modification time will be updated.
    #     """
    #     path = inp[2]
    #     os.mkdir(path)

    def initialize(self, waypoint):
        if isFile(waypoint.filepath):
            touch(waypoint.filepath)
        elif isDirectory(waypoint.filepath):
            mkdir(waypoint.filepath)

    @staticmethod
    def statusCode(msg):
        encoded = statusVec.index(msg)
        if self.verbose:
            print(encoded)
        return encoded

    @staticmethod
    def statusMsg(code, verbose=False):
        msg = statusVec[code]
        if verbose:
            print(msg)
        return msg

    def load(self, waypoint: tuple):
        fp = waypoint.filepath
        if isFile(fp):
            with open(fp) as f:
                contents = f.read()
                self.env.extend(waypoint.node, waypoint.filepath)
        elif isDirectory(fp):
            os.chdir(fp)

    def getState(self, verbose=False):
        if verbose:
            print("Self.state: " + self.state)
        return self.state

    def handleCallbacks(self, inp):
        pass

    def getNextState(self, inp):
        state = self.getState()
        if self.verbose:
            cat("\nCurrent state: ",str(state),inp.node, sep = " ", print_output=True)
        path_to_ref = inp[2]
        if state == 'updating':
            self.handleCallbacks(inp)
            self.pos += 1

        if os.path.exists(path_to_ref):
            if state == 'loading':
                self.load(inp)
                return 'updating'
            return 'loading'
        else:
            self.initialize(inp)
            return 'creating'

    def getNextValues(self, state, inp):
        return (self.getNextState(inp), inp[2])


class Accumulator(SM):
    startState = 0

    def getNextValues(self, state, inp):
        return (state + inp, state + inp)


def exec_all(args):
    return subprocess.call(args.split())


def makeCounter(init, step):
    return sm.Feedback(sm.Cascade(Increment(step), sm.Delay(init)))

def preserve_cwd(function):
    @functools.wraps(function)
    def decorator(*args, **kwargs):
        cwd = os.getcwd()
        try:
            os.chdir(args[0][0])
            return function(*args, **kwargs)
        finally:
            os.chdir(cwd)
    return decorator


#get_remote_url("/Users/kz/Projects/scotchbox/public/kevinzeidler.com")
#=> 'https://github.com/ProbonoBonobo/kevinzeidler.com.git'

def has_remote_target(fp=os.getcwd()):
    remote_url = get_remote_url()
    return remote_url and "github.com" in remote_url

@preserve_cwd
def total_number_of_commits(fp=os.getcwd()):
    os.chdir(fp)
    return shextract("git rev-list --all --count")


def create_repository(is_private=True, user='ProbonoBonobo', pw='myInsecureGithubPassword', repo_name='evergreen_data'):
    if has_remote_target():
        return
    else:
        shexec("git init")
        time.sleep(0.25)
        shexec("touch README.md")
        time.sleep(0.25)
        shexec("git add ")
        time.sleep(0.25)
        shexec("git commit -m \"initial commit \"")
        time.sleep(0.25)
        shexec("curl -u", user, ":", pw, " \"https://api.github.com/user/repos\", -d '{\"name\":\", repo_name, \", \"private:\", is_private,}\"")



def path_to(target):
    return app_state['path_to'][target]


def validate_paths(filepaths: Iterable[str]) -> bool:
    return all(map(lambda target: os.path.exists(path_to(target)), filepaths))


def get_state():
    return {'downloaded': ['conf', 'run', 'working_directory'],
            'initialized': ['staging_directory', 'file_to_update']}

def initializeCwd():
    abspath = os.path.abspath(__file__)
    dname = os.path.dirname(abspath)
    os.chdir(dname)
    print("Daemon initiialized. Current working directory is: " + cwd())
    return

@preserve_cwd
def is_vcs_root(fp=os.getcwd()):
        return os.path.exists('.git') and bool(shexec("git rev-parse --is-inside-work-tree"))
@preserve_cwd
def is_git_common_dir(fp=os.getcwd()):
    return shextract("git rev-parse --git-common-dir")
@preserve_cwd
def get_remote_url(fp=os.getcwd()):
    return shextract("git config --get remote.origin.url")

def load_config_file(config_file) -> dict:
    """
    Loads a configuration mapping object with contents
    of a given file.
    :param config_file: File-like object that can be read.
    :returns: mapping with configuration parameter values
    """
    code = compile(config_file.read(), config_file.name, 'exec')
    locals = {}
    exec(code, {'__builtins__': __builtins__}, locals)
    return locals


def run(conf):
    state = app_state.update(conf)
    print(path_to('working_directory'))
#
if __name__ == '__main__':

    abspath = os.path.abspath(__file__)
    dname = os.path.dirname(abspath)
    os.chdir(dname)
    print("Daemon initiialized. Current working directory is: " + pwd())
    sys.path.append(parentDirectory)
    f = open('config.txt')
    app_state = Config(load_config_file(f))
    turnstile = app_state.register('Turnstile', Turnstile())
    turnstileNavigator = app_state.register(
                                'TurnstileNavigator', TurnstileNavigator())
    pathConstructor = app_state.register(
        'PathConstructor', PathConstructor(app_state))


    is_git_common_dir("/Users/kz/Projects/scotchbox/public/kevinzeidler.com")
    is_vcs_root("/Users/kz/Projects/scotchbox/public/kevinzeidler.com")

# constructor.transduce(app_state['path_to'].values(), verbose=True)
