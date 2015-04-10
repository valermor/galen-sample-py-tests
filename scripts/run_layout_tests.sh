#!/bin/bash

currdir=$(basename "$PWD")

if [ "$currdir" == "scripts" ]; then
        cd ..
fi

echo "rm -rf ./target"
rm -rf ./target

echo "nose2 --plugin nose2.plugins.junitxml --plugin nose2.plugins.mp -c nose2.cfg -N 2 -A group=LAYOUT --log-level debug"
nose2 --plugin nose2.plugins.junitxml --plugin nose2.plugins.mp -c nose2.cfg -N 2 -A group=LAYOUT --log-level debug

python test/reports.py
