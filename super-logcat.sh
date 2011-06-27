#!/bin/sh

cd "$(dirname "$0")" # if run from another directory

[ -z "$1" ] && "$0" '.*' && exit

adb logcat | ./proclogcat "$@" | ./coloredlogcat.py
