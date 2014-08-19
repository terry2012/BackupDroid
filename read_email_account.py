#!/usr/bin/env python

import sqlite3

def main():
    conn = sqlite3.connect('apps/com.google.android.email/db/EmailProvider.db')
    cur = conn.cursor()

    print 'Protocol\tUsername\t\t\tPassword'
    for row in cur.execute('select protocol, login, password from HostAuth;'):
        print '%s\t\t%s\t\t%s' % (row[0], row[1], row[2])

    cur.close()
    conn.close()

if __name__ == '__main__':
    main()
