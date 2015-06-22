# pls
Python utility to search Google from the Linux command line

### Installation:

##### Use ant:

`sudo ant install`

##### Removal:

`sudo ant clean`

##### Usage:
`pls [options] [search terms]`

##### Options:
`-c: open using Chrome`  
`-f: open using Firefox`  
`-l: I'm Feeling Lucky`  
`-s: search using Google Scholar`  
`-d: debug flag - prints the URL that pls will open`  
`-h, --help: display usage information and exit`

##### Notes:
- search terms do not need to be enclosed in quotes.
- if building with `ant` fails, try using `sudo`.
- Any special characters (`*`, `"`, `$`, etc...) will be consumed by the shell before the script can even get its hands on them. To use these literal characters in a search query, escape them with `\`.

#### To-do list:
- `-i` flag to search Google Images
- Option TBD: flag to search Let Me Google That For You, for when you're feeling extra sassy (http://lmgtfy.com/)
- (?) switch window focus to newly created browser session

#### Notes for collaborators:
`git fetch`  
`git checkout -b <your develop branch name>`  
`git branch --set-upstream-to=origin/develop <your develop branch name>`  
`git pull`  
- read up on this branching model: http://nvie.com/posts/a-successful-git-branching-model/
- most importantly, develop features on branches checked out from `develop`, and merge them back in when they're stable
- once `develop` is stable, it gets merged with `master` as a new version
- the idea is that `master` will always represent a production-ready state
