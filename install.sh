#!/bin/sh
$USE_ALIASES = true
declare -A ghiSym
ghiSym=([ghi]=1 [tmp-ghi-util]=2)
declare -A gitSym
gitSym([git]=1 [tmp-git-util]=2)



command_exists () {
    type "$1" &> /dev/null ;
}

echo "Installing command-line dependency 'git' (https://git-scm.com/book/en/v1/Getting-Started-Installing-Git)..."
if command_exists git ; then
    echo "Skipping because git is already installed.\n\n"
elif command_exists brew ; then
    brew install git
    export git
    echo "Installation complete."
elif command_exists yum ; then
    yum install git
    export git
    echo "Installation complete."
elif command_exists apt-get ; then
    apt-get install git
    export git
    echo "Installation complete."
else
    echo "Couldn't find git command-line tools, or a suitable package manager to download the tools. To install them yourself, see the instructions at https://git-scm.com/book/en/v1/Getting-Started-Installing-Git.  Aborting."; exit 1;
fi




echo "Installing command-line dependency 'ghi' (https://github.com/stephencelis/ghi)..."
if command_exists ghi ; then
    echo "Skipping because ghi is already installed.\n\n"
elif command_exists brew ; then
    brew install ghi
    export ghi
    echo "Installation complete."
elif command_exists gem ; then
    gem install ghi
    export ghi
    echo "Installation complete."
else
    echo "Installation of ghi requires either homebrew or gem. Please make sure homebrew or gem is executable and try again.  Aborting."; exit 1;
fi
