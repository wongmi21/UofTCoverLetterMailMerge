# -*- coding: utf-8 -*-
"""
Created on Thu Jul 25 02:21:06 2013

@author: mike
"""

from bs4 import BeautifulSoup 
import requests
import csv
from titlecase import titlecase

url = raw_input("Enter a website to extract the URL's from: ")

while url != 'done':
    jobid = url.index('JOB_ID=') + 7
    endjobid = url.index('&abPage=')
    tr = url.index('tr=') + 3
    endtr = url.index('&K1=')
    printurl = 'http://www.careers.utoronto.ca/st/jobview.aspx?print=Y&JOB_ID=' + url[jobid:endjobid] + '&tr=' + url[tr:endtr]
    print printurl
     
    r  = requests.get(url) 
    data = r.text 
    soup = BeautifulSoup(data)
    
    try:
        email = soup.find('span', {'id' :'ctl00_MainContent_ctl03_lbl_apply'})    
        email = unicode(email)[unicode(email).index(u'<strong>Email:</strong>\u00a0') + len(u'<strong>Email:</strong>\u00a0'):]
        email = email[:email.index('<br')]
        print email
    except:
        email = 'email'
        print 'no email'
    try:
        employer = soup.find('span', {'id' :'ctl00_MainContent_ctl03_lbl_contact'}).text
        print employer
    except:
        employer = 'Hiring Manager'
        print 'no employer'
    try:
        company = titlecase(soup.find('span', {'id' :'ctl00_MainContent_ctl03_lbl_org'}).text)
        print company
    except:
        company = ''
        print 'no company'
    try:
        companyaddress = soup.find('span', {'id' :'ctl00_MainContent_ctl03_lbl_address'})
        companyaddress = unicode(companyaddress)
        companyaddress = companyaddress[companyaddress.index('ctl03_lbl_address">') + len('ctl03_lbl_address">'):companyaddress.index('<br/></span>')]
        companyaddress = companyaddress.replace('<br/>', r'\\')
        print companyaddress
    except:
        companyaddress = ''
        print 'no companyaddress'
    try:
        position = soup.find('span', {'id' :'ctl00_MainContent_ctl03_lbl_position_title'}).text
        print position
    except:
        position = ''
        print 'no position'
        
    try:
        actuarial = soup.find('span', {'id' :'ctl00_MainContent_ctl03_lbl_discipline'}).text
        actuarial = actuarial[actuarial.index('Actuarial Science'):]
        actuarial = '1'
        print actuarial
    except:
        actuarial = '0'
        print 'no actuarial'
    try:  
        industry = soup.find('span', {'id' :'ctl00_MainContent_ctl03_lbl_industry'}).text
        print industry
    except:
        industry = 'Finance/Insurance and Big Data'
        print 'industry'
    source = "University of Toronto's career website"
            
    resultFile = open("jobs.csv",'a')
    index = sum(1 for row in csv.reader(open("jobs.csv",'r')))
    newrow = [str(index),employer,company,companyaddress,position,industry,source,actuarial,url,email]
    newentry = ','.join('"' + item.replace(unichr(160), " ").strip() + '"' for item in newrow) + '\n'
    resultFile.write(newentry)
    resultFile.close
    
    url = raw_input("Enter a website to extract the URL's from: ")