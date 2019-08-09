#!/bin/bash
#Please specify full pathname of both input and output
#prePro.py deskews and rotates images somewhat
#ocrmypdf turns it pack into readable pdfs, and further fixes rotations
#and deskews as well
INNAME=$1
OUTNAME=$2
python prePro.py $INNAME bigData/edited.pdf
ocrmypdf --rotate-pages --deskew bigData/edited.pdf OUTNAME

