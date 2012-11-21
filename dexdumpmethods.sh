#!/bin/sh
###############################################################################
##
## Dump a list of methods from an apk or dx'd jar file.  This script was
## originally constructed to explore the general platform size of various
## framework jar files, but may be useful to others in light of the discovered
## Dalvik limit on total number of permitted methods as discussed here:
##
##   http://code.google.com/p/android/issues/detail?id=20814
##
## Usage:
##
##   dexdumpmethods.sh foo.apk
##
## I typically pipe the output to 'wc -l' to get a rough sense of size.
##
###############################################################################

filename=$1

# Dumps the method information to XML through the standard dexdump tool then
# processes it with XPath.  Basically, this selects all method tags, prints the
# class name then the method, and then iterates through all child parameters and
# formats them appropriately.  Most of the complexity is just getting the
# formatting looking right :)
dexdump -l xml "$filename" | \
        xmlstarlet sel -t \
                -m '//class/method' -v '../@name' -o '#' -v '@name' -o '(' \
                -m 'parameter' -o '' -v '@type' \
                        -i 'not(position()=last())' -o ', ' \
                -b -b -o ')' -i 'not(position()=last())' -n -b
