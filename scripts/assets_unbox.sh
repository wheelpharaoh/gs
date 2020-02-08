#!/bin/bash


#DS_Store
find . -name "*DS_Store" -print0 | xargs -0 rm {};

#unzip
find . -name "*.zip" -execdir unzip -u {} \; -exec rm {} \;

#decrypt
find . -name "*.dat" -exec /Users/jo/dev/gs/scripts/decrypt_xxtea.py {} \;
/Users/jo/dev/gs/scripts/masters.sh ~/Downloads/*.zip