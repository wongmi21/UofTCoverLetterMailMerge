# -*- coding: utf-8 -*-
"""
Created on Tue Jul 23 22:51:49 2013

@author: mike
"""

import os
import csv
import shutil
import subprocess
import urllib

fid = open("jobs.csv")
jobs = csv.reader(fid)
head = jobs.next()

for row in jobs:
    index = row[0]
    employer = row[1].replace('Dr', '').replace('Mr', '').replace('Mrs', '').replace('Ms', '').replace('Miss', '').replace('. ', '').replace('.', '')
    try:
        employer = employer[:employer.index(',')].strip()
    except:
        employer = employer
    company = row[2]
    companyaddress = row[3]
    position = row[4]
    industry = row[5]
    source = row[6]
    actuarial = row[7]
    printurl = row[8]
    email = row[9]
    
    olddir = index + ". " + position + " - " + company    
    newdir = olddir    
    chars=['\\','/',':','*','?','"','<','>','|']    
    for c in chars:
        newdir = newdir.replace(c, '_')
    if actuarial == "1":
        actuarialstring1 = r"actuarialstring1."
	actuarialstring2 = r"actuarialstring2."
    else:
        actuarialstring1 = ""
	actuarialstring2 = ""
    if not os.path.exists(newdir):
        os.makedirs(newdir)
        shutil.copy("signature.png", newdir)
        try:
            urllib.urlretrieve(printurl, "jobdescription.html")
            shutil.move("jobdescription.html", newdir)
        except:
            pass
        with open(newdir + "/CoverLetter.tex", 'w') as out_f:
            out_f.write(
r"""% Cover letter using letter.cls
\documentclass{letter} % Uses 10pt
%\usepackage{helvetica} % uses helvetica postscript font (download helvetica.sty)
%\usepackage{newcent}   % uses new century schoolbook postscript font 
\usepackage{graphicx}
% the following commands control the margins:
\topmargin=-1in    % Make letterhead start about 1 inch from top of page 
\textheight=10in    % text height can be bigger for a longer letter
\oddsidemargin=0pt   % leftmargin is 1 inch
\textwidth=6.5in     % textwidth of 6.5in leaves 1 inch for right margin
\newcommand{\employer}{"""+employer+r"""}
\newcommand{\company}{"""+company.replace('&','\\&')+r"""}
\newcommand{\companyaddress}{"""+companyaddress+r"""}
\newcommand{\position}{"""+position.replace('&','\\&')+r"""}
\newcommand{\source}{"""+source+r"""}
\newcommand{\actuarial}{"""+actuarial+r"""}
\newcommand{\industry}{"""+industry.replace('&','\\&')+r"""}


\begin{document}


%\signature{MYNAMEHERE}           % name for signature 
\longindentation=0pt                       % needed to get closing flush left
\let\raggedleft\raggedright                % needed to get date flush left
 
 
\begin{letter}{
\employer \\
\company \\
\companyaddress
}

\begin{center}
{\large\bf MYNAMEHERE} 
\end{center}
\medskip\hrule height 1pt
\begin{center}
{MYCONTACTINFOHERE} 
\end{center} \vfill % forces letterhead to top of page
 
 
\opening{Dear \employer:} 
 
\noindent COVER LETTER HERE

\closing{Sincerely yours, \\
\fromsig{\includegraphics[scale=0.25]{signature.png}} \\
\fromname{MYNAMEHERE}
} 
\end{letter}
\end{document}
"""        )
        with open(newdir + "/" + email + ".txt", 'w') as out_g:
            out_g.write(
r"""Dear """+employer+r""",

I am writing to express interest in the """+position+r""" position for """+company+r""".
I recently graduated from the University of Toronto in GRADDATEHERE with a FIELDSHERE. """+actuarialstring1+r"""
I have attached both my resume and a cover letter for your consideration. Thank you very much.

Sincerely,
MYNAMEHERE

-------
MYNAME
MYCONTACTINFO
"""
            )
        subprocess.call(['pdflatex', "-output-directory=" + newdir, newdir + "/MichaelWongCoverLetter.tex"], shell=False)
