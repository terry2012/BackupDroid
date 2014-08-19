#!/usr/bin/env python

import os

def main():
    os.system('dd if=backup.ab bs=1 skip=24 | openssl zlib -d > backup.tar')
    os.system('tar xvf backup.tar')

if __name__ == '__main__':
    main()