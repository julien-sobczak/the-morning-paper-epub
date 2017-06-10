#!/bin/bash

# ========================================
# Append new tags in Pypub source code
# to include <pre> and <code> elements
# in the generated epub.
# ========================================


LIB_DIR=env/lib/python2.7/site-packages/pypub

# Make a copy of the original files
cp $LIB_DIR/constants.py{,.bak}
cp $LIB_DIR/constants.pyc{,.bak}

# Print array declaration
head -n 3 $LIB_DIR/constants.py >> \
          $LIB_DIR/constants2.py

# Append new tags
echo "    'code': []," >> $LIB_DIR/constants2.py
echo "    'pre': [],"  >> $LIB_DIR/constants2.py

# Print the remaining of the file
tail -n $((`wc -l $LIB_DIR/constants.py |awk '{print $1}'`- 3)) $LIB_DIR/constants.py >> \
          $LIB_DIR/constants2.py

mv $LIB_DIR/constants2.py $LIB_DIR/constants.py
