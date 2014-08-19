#!/usr/bin/env python

from xml.dom import minidom
import base64
import subprocess


def decrypt_andftp(text):
    cmd = 'java AndFtpDecryptor %s' % text
    proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    ret = proc.communicate()[0][:-1]
    return ret


def main():
    andftp = 'apps/lysesoft.andftp/sp/andftp.xml'
    doc = minidom.parse(andftp)
    root = doc.documentElement
    nodes = root.getElementsByTagName('string')
    
    url = ''
    username = ''
    password = ''
    
    for node in nodes:
        attr = node.getAttribute('name')
        if attr.startswith('ftp.url['):
            url = node.childNodes[0].data.replace('\r', '').replace('\n', '')
        if attr.startswith('ftp.username['):
            username = node.childNodes[0].data.replace('\r', '').replace('\n', '')
        if attr.startswith('ftp.password['):
            password = node.childNodes[0].data.replace('\r', '').replace('\n', '')
    
    print '\tEncoded Account'
    print '=' * 32
    print 'URL: %s' % url
    print 'Username: %s' % username
    print 'Password: %s' % password
    print ''
    
    url = base64.b64decode(url)
    username = base64.b64decode(username)
    password = base64.b64decode(password)
    
    print '\tDecoded Account'
    print '=' * 32
    print 'URL: %s' % url
    print 'Username: %s' % username
    print 'Password: %s' % password
    print ''
    
    username = decrypt_andftp(username)
    password = decrypt_andftp(password)
    
    print '\tDecrypted Account'
    print '=' * 32
    print 'URL: %s' % url
    print 'Username: %s' % username
    print 'Password: %s' % password
    print ''
    
    
if __name__ == '__main__':
    main()
