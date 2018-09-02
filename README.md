What is this?
-------------

This is a set of scripts to enhance your development time with adb.

* LOGCAT:

`./super-logcat.sh <interesting-process-name-regex-or-tag>`

So, if your process name is `com.example.myapp`, then running `./super-logcat.sh com.example` will show all messages related to your application.

Running the `super-logcat.sh` script with no arguments will display the logcat output from every process, piped through the same formatting and coloring algorithm.


* DEVICES:

`./pickdevice.pl`

This will help you easily select the device to run the commands on. This is usefull when using multiple devices/emulators at the same time.


* METHOD_ANALYSING

`./dexdumpmethods.sh <apk or dx'd jar file>`

You will see all methods in this package. It is usefull to pipe it into `wc -l` to see an overall number of functions.
