#!/usr/bin/env python

import sys, subprocess, os, re, urllib2, argparse, random
# Global variables - _g suffix indicates global status

url_g = 'https://www.google.com/search?q=' # default to standard google search
browser_g = 'xdg-open' # use system default as default browser
parser_g = argparse.ArgumentParser(epilog='Special characters (*, ", $, etc.) must be escaped using \, and search terms do not need to be enclosed in quotes.') # global argument parser

# utility functions
def trueCount(boolList):
    count = 0 # number of true items in the list
    for current in boolList:
        if current == True:
            count += 1
    return count

def debugPrint(string):
    if parser_g.parse_args().debug == True: # check arguments for -d flag
        print string

# register arguments with the parser
def initParser():
    '''
    Initializes the parser to accept all defined arguments. Future options should be registered here.
    '''
    browserArgGroup = parser_g.add_mutually_exclusive_group()
    flagArgGroup = parser_g.add_mutually_exclusive_group()

    parser_g.add_argument(
            'terms',
            help='Search terms to be passed to Google',
            nargs='*')
    parser_g.add_argument(
            '-d',
            '--debug',
            help='Debug flag - print the URL that pls will open',
            action='store_true')
    browserArgGroup.add_argument(
            '-c',
            '--chrome',
            help='Open using Chrome',
            action='store_true')
    browserArgGroup.add_argument(
            '-f',
            '--firefox',
            help='Open using Firefox',
            action='store_true')
    flagArgGroup.add_argument(
            '-l',
            '--lucky',
            help='I\'m Feeling Lucky',
            action='store_true')
    flagArgGroup.add_argument(
            '-i',
            '--images',
            help='Search using Google Images',
            action='store_true')
    flagArgGroup.add_argument(
            '-s',
            '--scholar',
            help='Search using Google Scholar',
            action='store_true')
    flagArgGroup.add_argument(
            '-n',
            '--news',
            help='Search using Google News',
            action='store_true')
    flagArgGroup.add_argument(
            '-v',
            '--video',
            help='Search using Google Video',
            action='store_true')
    flagArgGroup.add_argument(
            '-y',
            '--youtube',
            help='Search using YouTube',
            action='store_true')
    flagArgGroup.add_argument(
            '-m',
            '--sass',
            help='Increase sass - search using Let Me Google That For You',
            action='store_true')
    flagArgGroup.add_argument(
            '-r',
            '--simpsons',
            help='Open a randomly selected Simpsons episode',
            action='store_true')
    flagArgGroup.add_argument(
            '-x',
            '--xkcd',
            help='Open a randomly selected xkcd comic',
            action='store_true')

def which(program): # thanks: http://stackoverflow.com/questions/377017/test-if-executable-exists-in-python
    def is_exe(fpath):
        return os.path.isfile(fpath) and os.access(fpath, os.X_OK)

    fpath, fname = os.path.split(program)
    if fpath:
        if is_exe(program):
            return program
    else:
        for path in os.environ["PATH"].split(os.pathsep):
            path = path.strip('"')
            exe_file = os.path.join(path, program)
            if is_exe(exe_file):
                return exe_file

    return None

def determineBrowser(argList):
    '''
    Sets global browser variable; the default value (xdg-open) is initialized with the global variable, so it is not specified here.
    '''
    global browser_g
    if argList.chrome == True:
        if not which('google-chrome'):
            print 'Google Chrome is not installed.'
            exit(1)
        else:
            browser_g = 'google-chrome'

    elif argList.firefox == True:
        if not which('firefox'):
            print 'Firefox is not installed.'
            exit(1)
        else:
            browser_g = 'firefox'

def getQuery():
    '''
    Gets the query string that will be appended to the appropriate URL.
    '''
    query = ''
    terms = parser_g.parse_args().terms # don't need to declare global parser_g because we're not editing the variable here - just reading from it
    for term in terms:
        query += term
        query += '+'
    query = query[:-1] # remove final '+' added by for loop
    return query

def internetOn(): # thanks: http://stackoverflow.com/questions/3764291/checking-network-connection
    try:
        response = urllib2.urlopen('http://google.com/', timeout = 1)
        return True
    except urllib2.URLError as err: pass
    return False

def exitIfNoInternet():
    if not internetOn():
        print 'Problem connecting to the internet.'
        exit(64) # exit code 64 means machine is not on the network

def getSource(url):
    req = urllib2.Request(url, headers={'User-Agent' : "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/534.30 (KHTML, like Gecko) Ubuntu/11.04 Chromium/12.0.742.112 Chrome/12.0.742.112 Safari/534.30"})
    source = urllib2.urlopen(req).read() # get html source
    return source

def determineURL(argList):
    '''
    Sets global URL (e.g. to search Images, Scholar, LMGTFY, etc.) given the corresponding flag.
    '''
    global url_g

    exitIfNoInternet()

    query = getQuery() # query to be appended to URL in some cases

    url_g += query # default to standard Google search

    if argList.scholar == True:
        url_g = 'https://scholar.google.com/scholar?q=' + query
        # append query here to show Google results page with given query

    elif argList.lucky == True:
        source = getSource(url_g)
        searchObj = re.search( r'<h3 class="r"><a href="(.*?)"', source) # get first occurrence of a result and capture its URL

        if not searchObj:
            print 'Warning: no search terms detected. Defaulting to Google homepage.'
            url_g = 'https://www.google.com/'

        else:
            url_g = searchObj.group(1)
        # do not append query here; the purpose of -l is to access first link of results

    elif argList.images == True:
        baseURL = 'https://www.google.com'
        source = getSource(url_g)
        searchObj = re.search( r'<a class="q qs" href="([^"]*)">Images</a>', source)

        if not searchObj:
            print 'Warning: no search terms detected. Defaulting to Google Images homepage.'
            url_g = 'https://images.google.com/'

        else:
            imgHash = searchObj.group(1)
            imgHash = imgHash.replace('&amp;', '&')
            url_g = baseURL + imgHash
        # do not append query here; Google Images has a more complex URL, which is handled by the above logic

    elif argList.sass == True:
        url_g = 'http://www.lmgtfy.com/?q=' + query
        # append query here to pass search terms to LMGTFY

    elif argList.simpsons == True:
        seasonSelect = 'http://projectfreetv.so/free/the-simpsons/'
        source = getSource(seasonSelect)
        searchObj = re.findall( r'<a href="(http://projectfreetv.so/free/the-simpsons/the-simpsons-season-\d+/)" ?>', source)
        seasonURL = random.choice(searchObj)

        episodeSelect = seasonURL
        source = getSource(episodeSelect)
        searchObj = re.findall( r'<a href="(http://projectfreetv.so/the-simpsons-season-\d+-episode-\d+/)">', source)
        episodeURL = random.choice(searchObj)

        url_g = episodeURL

    elif argList.xkcd == True:
        # url_g = 'https://xkcd.com/4/' # guaranteed to be random
        url_g = 'http://c.xkcd.com/random/comic/'

    elif argList.youtube == True:
        url_g = 'https://www.youtube.com/results?search_query=' + query
        # append query here to display youtube results with given query

    elif argList.news == True:
        url_g = 'https://www.google.com/search?tbm=nws&q=' + query
        # append query here to display news results with given query

    elif argList.video == True:
        url_g = 'https://www.google.com/#tbm=vid&q=' + query

    # additional options here

def main():
    '''
    Driver function for pls
    '''
    DEVNULL = open(os.devnull, 'w')

    initParser()
    determineBrowser(parser_g.parse_args())
    determineURL(parser_g.parse_args())
    debugPrint(url_g)

    subprocess.call([browser_g, url_g], stdout=DEVNULL, stderr=subprocess.STDOUT) # shhhh - redirect browser output to /dev/null
    # thanks: http://stackoverflow.com/questions/11269575/how-to-hide-output-of-subprocess-in-python-2-7

if __name__ == '__main__':
    main()
