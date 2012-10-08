#!/bin/sh

me=$0
link=$(readlink "$me")
[ ! -z "$link" ] && me=$link

cd "$(dirname "$me")"

[ -z "$1" ] && "$0" '.*' && exit

adb logcat | ./proclogcat "$@" | ./coloredlogcat.py
