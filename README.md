# evergreen
![alt text](assets/github-meme-you-vs-the-guy-she-tells-you-not-to-worry-about.jpg?raw=true "Before you installed evergreen vs. after you installed evergreen")

##what's in the box
* A launch daemon that initializes a Poisson counting process
* A system subprocess that writes the repository's current commit count to [a tracked file](/.evergreen_data/state.txt)
* A user agent that pushes the updated state to the Git repository about every 90 minutes
* A abstract complaint syntax for generating new issues
* A command-line interface to Github API

##what's the deal with the 'issues' section
yeah I guess simply updating [the commit counter](/.evergreen_data/state.txt) is insufficient to trigger a github "activity" event, so I made a generator function that yields [category-theoretic complaints](https://github.com/ProbonoBonobo/evergreen/issues?utf8=%E2%9C%93&q=is%3Aissue)  

##requirements
Tested on Mac OSX/Sierra, theoretically should work with all POSIX-based operating systems. You'll need python3 and git command-line tools on your path.

##installation
The install.sh script is untested and *not* recommended. Install manually for now:

###Github Issues API
`brew install ghi`
or
`gem install ghi`

To store your github credentials in an auth token, type

`ghi config --auth <MyUsername>`

and follow the prompt's instructions.

###initializing the launch daemon

`Nobodys-MacBook-Pro:Evergreen4 kz$ python3 installer.py`

`Daemon successfully loaded. Exiting with status code 0...`

Restart to activate the daemon.

##help wanted
Do these instructions work for you? Do they not work? I haven't found any good way to package a Python command line utility with its environment dependencies. I'm writing the `installer.sh` shell script to configure those dependencies on a clean Ubuntu VM in the hopes of being able to run tests against the deployed version. I don't really know what I'm doing. Pull requests welcome!
