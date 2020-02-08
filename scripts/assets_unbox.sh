#!/bin/bash


#DS_Store
find . -name "*DS_Store" -print0 | xargs -0 rm {};

#unzip
find . -name "*.zip" -execdir unzip -u {} \; -exec rm {} \;

#decrypt
find . -name "*.dat" -exec ./scripts/decrypt_xxtea.py {} \;

./masters.sh ~/Downloads/*.zip

#unpack
find . -name "*.png" -print0 | cut -d '.png' -f1 | xargs -0 ./scripts/unpack_texture.py {};
