# evergreen
![alt text](assets/github-meme-you-vs-the-guy-she-tells-you-not-to-worry-about.jpg?raw=true "Before you installed evergreen vs. after you installed evergreen")

##what's in the box
* A launch daemon that initializes a Poisson counting process
* A system subprocess that writes the repository's current commit count to [a tracked file](/.evergreen-data/state.txt)
* A user agent that pushes the updated state to the Git repository about every 90 minutes
* A abstract complaint syntax for generating new issues
* A command-line interface to Github API

##requirements
Tested on Mac OSX/Sierra, theoretically should work with all POSIX-based operating systems. You'll need python3 and git command-line tools on your path.

##installation

###Github Issues API
`brew install ghi`
or
`gem install ghi`

(detailed instructions forthcoming)
