#!/bin/bash

# تثبيت sherlock
if [ ! -d "sherlock" ]; then
    git clone https://github.com/sherlock-project/sherlock.git
    cd sherlock
    pip install -r requirements.txt
    cd ..
fi

# تثبيت theHarvester
if [ ! -d "theHarvester" ]; then
    git clone https://github.com/laramies/theHarvester.git
    cd theHarvester
    pip install -r requirements/base.txt
    cd ..
fi

# تثبيت PhoneInfoga
if [ ! -d "PhoneInfoga" ]; then
    git clone https://github.com/sundowndev/phoneinfoga.git
    cd phoneinfoga
    pip install -r requirements.txt
    cd ..
fi