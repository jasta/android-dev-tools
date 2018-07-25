#!/usr/bin/env bash

if [ ! "$*" ]; then
	"$0" ".+"
	exit $?
fi

dir=`dirname "$0"`

if [ "`readlink $0`" ]; then
	dir=`dirname "$(readlink $0)"`
fi

adb logcat | "$dir/proclogcat" "$@" | "$dir/coloredlogcat.py"
