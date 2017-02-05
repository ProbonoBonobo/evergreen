#/usr/local/bin/python3
import os
import re
import subprocess
import shutil
import sys
valid = 1
unknown = 0
invalid = -1

def get_parent():
    return os.path.dirname(os.path.abspath(__file__))

def is_valid_plist_file(fp,value_if_true, value_if_false, value_if_nil):
    if shutil.which("plutil"):
        result =  subprocess.check_output(['plutil', fp]).decode("utf-8")
        if 'OK' in result:
            return value_if_true
        else:
            return value_if_false
    return value_if_nil

    subprocess.check_output(["plutil", "/Library/LaunchAgents/com.kevinzeidler.evergreen.plist"])
def state(cmd_line_arg):
    if cmd_line_arg == 'y' or cmd_line_arg == 'n':
        return 'valid'
    else:
        return 'invalid'

env = dict({r'\$PATH\_TO\_PYTHON3\$' : '/usr/local/bin/python3',
            r'\$PATH\_TO\_SCRIPT\$'    : ''.join([get_parent(),"/",'event-loop.py']),
            r'\$USER\$'    : os.environ['USER']})

template = "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n<!DOCTYPE plist PUBLIC \"-//Apple Computer//DTD PLIST 1.0//EN\" \"http://www.apple.com/DTDs/PropertyList-1.0.dtd\">\n<plist version=\"1.0\">\n<dict>\n    <key>Label</key>\n    <string>com.kevinzeidler.evergreen</string>\n\n    <key>OnDemand</key>\n    <false/>\n\n    <key>UserName</key>\n    <string>$USER$</string>\n\n    <key>ProgramArguments</key>\n    <array>\n            <string>$PATH_TO_PYTHON3$</string>\n            <string>$PATH_TO_SCRIPT$</string>\n    </array>\n</dict>\n</plist>"

if __name__ == '__main__':

    try:
        file = open("/Library/LaunchAgents/com.kevinzeidler.evergreen.plist", 'r')


    except IOError:
        assert(os.exists("/Library/LaunchAgents"))
        for env_var in list(env.keys()):
            print(env_var)
            template = re.sub(env_var, env[env_var], template)
        plist_file = template
        with open("com.kevinzeidler.evergreen.plist", 'w') as f:
            f.write(plist_file)
        assert(is_valid_plist_file(get_parent() + "com.kevinzeidler.evergreen.plist", valid, invalid, unknown) == valid)
        user_confirmation = ""
        while state(user_confirmation) == 'invalid':
            user_confirmation = input("This script will create a new startup daemon in /Library/LaunchAgents that initializes the git update process on startup. Continue? (y/n)")
            print("Please enter 'y' to confirm, or 'n' to quit.")
        if user_confirmation == 'y':
            os.symlink(get_parent() + "/com.kevinzeidler.evergreen.plist", "/Library/LaunchAgents/com.kevinzeidler.evergreen.plist")
        else:
            print("Installation aborted. To complete the installation, move or link the plist file at " + get_parent() + "com.kevinzeidler.evergreen.plist to your /Library/LaunchAgents directory.")
    finally:
        plist_status = is_valid_plist_file("/Library/LaunchAgents/com.kevinzeidler.evergreen.plist", valid, invalid, unknown)
        if plist_status is valid:
            print("\n\nDaemon successfully loaded. Exiting with status code 0...\n\n")
            sys.exit(0)

        if plist_status is invalid:
            sys.exit("Error validating the launch daemon at \"/Library/LaunchAgents/com.kevinzeidler.evergreen.plist\".")
