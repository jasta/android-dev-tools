#!/usr/bin/python

'''
    Copyright 2009, The Android Open Source Project

    Licensed under the Apache License, Version 2.0 (the "License"); 
    you may not use this file except in compliance with the License. 
    You may obtain a copy of the License at 

        http://www.apache.org/licenses/LICENSE-2.0 

    Unless required by applicable law or agreed to in writing, software 
    distributed under the License is distributed on an "AS IS" BASIS, 
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. 
    See the License for the specific language governing permissions and 
    limitations under the License.
'''

# script to highlight adb logcat output for console
# written by jeff sharkey, http://jsharkey.org/
# piping detection and popen() added by other android team members

# modified by Josh Guilfoyle <jasta@devtcg.org> to simplify formatting back to
# adb logcat original.  I just want colorized logcat output, nothing fancier.

import os, sys, re, StringIO
import fcntl, termios, struct

BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE = range(8)

def format(fg=None, bg=None, bright=False, bold=False, dim=False, reset=False):
    # manually derived from http://en.wikipedia.org/wiki/ANSI_escape_code#Codes
    codes = []
    if reset: codes.append("0")
    else:
        if not fg is None: codes.append("3%d" % (fg))
        if not bg is None:
            if not bright: codes.append("4%d" % (bg))
            else: codes.append("10%d" % (bg))
        if bold: codes.append("1")
        elif dim: codes.append("2")
        else: codes.append("22")
    return "\033[%sm" % (";".join(codes))

def colorToFormat(color):
    return format(fg=color, bold=True)

LAST_USED = map(colorToFormat, [RED,GREEN,YELLOW,BLUE,MAGENTA,CYAN,WHITE])
KNOWN_TAGS = {
    "dalvikvm": format(fg=BLACK, bold=True),
    "AndroidRuntime": format(fg=BLACK, bold=True),
    "Process": format(fg=YELLOW, bold=True),
    "ActivityManager": format(fg=CYAN, bold=True),
    "ActivityThread": format(fg=CYAN, bold=True),
    "System.err": format(bg=BLUE),
    "System.out": format(bg=BLUE),
}

def allocate_color(tag):
    # this will allocate a unique format for the given tag
    # since we dont have very many colors, we always keep track of the LRU
    if not tag in KNOWN_TAGS:
        KNOWN_TAGS[tag] = LAST_USED[0]
    color = KNOWN_TAGS[tag]
    if color in LAST_USED:
        LAST_USED.remove(color)
        LAST_USED.append(color)
    return color


TAGTYPES = {
    "V": "",
    "D": format(fg=BLUE, bold=True),
    "I": "",
    "W": format(fg=YELLOW, bold=True),
    "E": format(fg=RED, bold=True),
}


TAGTYPENAMES = {
    "V": "Verb ",
    "D": "Debug",
    "I": "Info ",
    "W": "WARN ",
    "E": "ERROR"
}

retag = re.compile("^([A-Z])/([^\(]+)\(([^\)]+)\): (.*)$")
newRetag = re.compile("^([0-9-\s:.]+?)\s+(\d+)\s+(\d+)\s+([A-Z])\s+(.*?)\s*: (.*)$")

# to pick up -d or -e
adb_args = ' '.join(sys.argv[1:])

# if someone is piping in to us, use stdin as input.  if not, invoke adb logcat
if os.isatty(sys.stdin.fileno()):
    input = os.popen("adb %s logcat" % adb_args)
else:
    input = sys.stdin

while True:
    try:
        line = input.readline().rstrip()
    except KeyboardInterrupt:
        break

    match = retag.match(line)
    newMatch = newRetag.match(line)
    if not match is None:
        tagtype, tag, owner, message = match.groups()
        linebuf = StringIO.StringIO()

        # write out tagtype colored edge
        if not tagtype in TAGTYPES: break
        linebuf.write("%s%s%s" % (TAGTYPES[tagtype], TAGTYPENAMES[tagtype], format(reset=True)))

        color = allocate_color(tag)
        linebuf.write(" / %s%s%s" % (format(fg=color, bold=True), tag, format(reset=True)))

        linebuf.write(" (%s): " % owner)

        linebuf.write("%s%s%s" % (color, message, format(reset=True)))
        line = linebuf.getvalue()
    elif not newMatch is None:
        time, owner, ppid, tagtype, tag, message = newMatch.groups()
        if not tagtype in TAGTYPES: break

        linebuf = StringIO.StringIO()
        linebuf.write("%s %05s | %05s" % (time, owner, ppid))


        # write out tagtype colored edge
        linebuf.write(" %s%s%s" % (TAGTYPES[tagtype], TAGTYPENAMES[tagtype], format(reset=True)))

        colorfmt = allocate_color(tag)
        linebuf.write(" / %s%s%s: " % (colorfmt, tag, format(reset=True)))

        linebuf.write("%s%s%s" % (colorfmt, message, format(reset=True)))
        line = linebuf.getvalue()
    print line
