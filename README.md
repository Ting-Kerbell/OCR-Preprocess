This program is designed to preprocess PDFS for the ABBYY OCR by deskewing and 
rotating files. More specifically this program is designed to correct the 
orientation of pdfs such as the following: 
(https://epancotti.github.io/elizabethpancotti.com/blurred_pdf_samples.pdf)
The content is blurred for confidentiality reasons

USAGE: sh deskewPDF {input file with relative path} {output file name with path}
Ideally, you can put the input pdf into the input folder, and the output file in
the generated_output folder. It would look something like this:
sh deskewPDF input/1998.pdf generated_output/changed1998.pdf

REQUIREMENTS:
Some of the preprocessing is done in Python while the rest is
done on command line through ocrmypdf. For the python code to work, the 
following libraries are needed:
numpy
cv2
pdf2image
FPDF
PIL

User must also install ocrmypdf 
(https://ocrmypdf.readthedocs.io/en/latest/installation.html)
The additional packages required for this is also specified in the link.
