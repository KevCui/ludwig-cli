#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os, sys, re, json
import urllib.request
from random import shuffle

def showErrorAndExit(txt):
    print('ERROR! ' + txt)
    sys.exit(1)

def getAuthFromFile(file):
    if os.path.isfile(file):
        list = []
        f = open(file, 'r')
        for line in f:
            list.append(line.replace('\n', ''))
        return list
    else:
        showErrorAndExit(file + ' doesn\'t exist!')

def writeToFile(file, token):
    f = open(file, "w+")
    f.write(token)
    f.close()

def getJSON(url, auth):
    badauth = os.path.dirname(__file__) + '/badauth.conf'

    shuffle(auth)
    n = 0
    while n < len(auth):
        req = urllib.request.Request(url)
        req.add_header('Authorization', auth[n])
        try:
            return json.loads(urllib.request.urlopen(req).read().decode('utf-8'))
        except:
            writeToFile(badauth, auth[n])
            n = n + 1
    showErrorAndExit('No available token!')

def pYellow(txt):
    print(colored(txt, 'yellow', attrs=['bold']))

def pGreen(txt):
    print(colored(txt, 'green'))

def pBlue(txt):
    print(colored(txt, 'blue'))

def main():
    if (len(sys.argv) != 2): showErrorAndExit('<word> is missing: ./ludwig.py <word>')

    word     = sys.argv[1]
    url      = 'https://api.ludwig.guru/ludwig-authentication-manager/rest/v1.0'
    search   = url + '/search?q=' + str(word)
    suggest  = url + '/suggest?q=' + str(word)
    authfile = os.path.dirname(__file__) + '/auth.conf'
    tokens   = getAuthFromFile(authfile)
    rawjson  = getJSON(search, tokens)

    if 'Dictionary' not in rawjson.keys():
        suggestjson = getJSON(suggest, tokens)
        pBlue('Suggestion: ' + ', '.join(suggestjson[0]['values']))
    else:
        for definition in rawjson['Dictionary']['posDefinition']:
            pYellow(definition['posType'])
            for gloss in definition['glosses']:
                pGreen('  - ' + gloss['definition'])
                try:
                    print('      ' + ''.join(gloss['example']))
                except:
                    pass
            try:
                pBlue('  Synonyms: ' + ', '.join(definition['synonyms']))
            except:
                pass
            try:
                pBlue('  Antonyms: ' + ', '.join(definition['antonyms']))
            except:
                pass
            print("\n")

if __name__ == '__main__':
    try:
        from termcolor import colored
    except ImportError:
        showErrorAndExit('termcolor is not installed. Please pip install termcolor')

    main()
