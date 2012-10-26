#!/bin/sh

python setup.py sdist

if [ "$?" -ne 0 ]; then
    echo "Build failed."
    exit 1
fi

python setup.py sdist upload

if [ "$?" -ne 0 ]; then
    echo "Upload failed."
    exit 1
fi

