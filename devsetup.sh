#!/usr/bin/env bash
# Checking whether there's a docker installation somewhere
# on PATH
hash docker >/dev/null 2>&1
if [ "$?" != "0" ] ; then 
    echo "It looks like \`docker\` is not available on this system."
    echo "Please update your \$PATH variable with the parent directory of your \`docker\` installation."
    exit 1
fi

