#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os, sys, re, json
import urllib.request

try:
    from termcolor import colored
except ImportError:
    print('termcolor is not installed. Please pip install termcolor')
    sys.exit(1)

def getAuthFromFile(file):
    if os.path.isfile(file):
        with open(file) as f:
            return str(f.readline().replace('\n', ''))
    else:
        print('ERROR! '+ file + ' doesn\'t exist!')
        sys.exit(1)

def getJSON(url, auth):
    req = urllib.request.Request(url)
    req.add_header('Authorization', auth)
    return json.loads(urllib.request.urlopen(req).read().decode('utf-8'))

def pYellow(txt):
    print(colored(txt, 'yellow', attrs=['bold']))

def pGreen(txt):
    print(colored(txt, 'green'))

def pBlue(txt):
    print(colored(txt, 'blue'))

def checkInput(var):
    if(len(var) != 2):
        print('<word> is missing: ./ludwig.sh <word>')
        sys.exit(1)

def main():
    checkInput(sys.argv)

    word     = sys.argv[1]
    search   = 'https://api.ludwig.guru/ludwig-authentication-manager/rest/v1.0/search?q=' + str(word)
    suggest  = 'https://api.ludwig.guru/ludwig-authentication-manager/rest/v1.0/suggest?q=' + str(word)
    authfile = os.path.dirname(__file__) + '/auth.conf'
    auth     = getAuthFromFile(authfile)
    rawjson  = getJSON(search, auth)

    if 'Dictionary' not in rawjson.keys():
        suggestjson = getJSON(suggest, auth)
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
    main()
