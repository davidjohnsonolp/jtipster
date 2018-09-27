#!/usr/bin/python
import urllib, urllib2

secret_key = '6LfIvgQTAAAAALXc-Ht55vRoSTI8Mwgny7UQn4Nh'
server_name = 'https://www.google.com/recaptcha/api/siteverify'


def check(response):
    params = urllib.urlencode(dict(secret=secret_key, response=response))
    data = None
    try:
        f = urllib2.urlopen(server_name, params)
        data = f.read()
        f.close()
    except urllib2.HTTPError:
        pass
    except urllib2.URLError:
        pass
    return data


def confirm(response):
    result = False
    reply = check(response)
    if reply:
        if reply.lower().find('"success": true') >= 0:
            result = True
    return result