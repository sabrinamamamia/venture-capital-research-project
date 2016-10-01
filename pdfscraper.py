from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import HTMLConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from cStringIO import StringIO

from BeautifulSoup import BeautifulSoup
import csv
import re
import sys
import json

files = open("PDFfileslist.txt", "r")
files = files.readlines()
files = map(lambda s: s.strip(), files)
print files

for a in files:
    def convert_pdf_to_txt(path):
        rsrcmgr = PDFResourceManager()
        retstr = StringIO()
        codec = 'utf-8'
        laparams = LAParams()
        device = HTMLConverter(rsrcmgr, retstr, codec=codec, laparams=laparams)
        fp = file(path, 'rb')
        interpreter = PDFPageInterpreter(rsrcmgr, device)
        password = ""
        maxpages = 0
        caching = True
        pagenos=set()
        for page in PDFPage.get_pages(fp, pagenos, maxpages=maxpages, password=password,caching=caching, check_extractable=True):
            interpreter.process_page(page)
        fp.close()
        device.close()
        str = retstr.getvalue()
        retstr.close()
        return str

    html = convert_pdf_to_txt(a)
    soup = BeautifulSoup(html)
    #print soup

    company_name = str(a)
    company_name = company_name.replace('.pdf', '')
    if company_name.count('-') > 0:
        company_name = company_name.replace('-', '')
    #print company_name

    #COMPANY TAB------------------------------------------------
    a_string = soup.find(text="Geographic Region:").parent.parent
    #print a_string
    list = a_string.findAll("span")

    name = ""

    dict = {"Company:": None, "Address:": None, "Geographic Region:": None, "Industry:": None, "SIC Codes:": None, "NAICS Codes:": None, "Legal Counsel:": None, "Company Website:": None,
    "Executive": None, "Position": None}

    dict_instance1 = dict;

    for idx, val in enumerate(list):
        if idx % 2 == 0:
            #continue #print "key:", val.text
            name = val.text #name = key. val.text e.g. "Geogrpahic Location"
            dict_instance1["Company:"] = company_name
        else:
            dict_instance1[name] = val.text #dict[Geographic Location] = val.text
            dict_instance1["Company:"] = company_name

    #company = dict_instance1

    outfile = open("./Company_TEST_V1.csv", "a")
    writer = csv.writer(outfile)
    writer.writerow([dict_instance1["Company:"],dict_instance1["Address:"],dict_instance1["Geographic Region:"],dict_instance1["Industry:"],dict_instance1["SIC Codes:"],dict_instance1["NAICS Codes:"],dict_instance1["Legal Counsel:"],dict_instance1["Company Website:"]])
    #Access a dictionary value with its key name in the same syntax that you assign a value to a key name - see line 45

    #KEY MANAGEMENT TAB------------------------------------------
    if soup.findAll(text="Key Management\n") == None:
        pass
    else:
        draft1_management = soup.findAll(text="Key Management\n")
        draft1_management = draft1_management[1].parent.parent
        draft1_management = draft1_management.nextSibling.contents
        draft1_management = str(draft1_management)
        draft1_management = draft1_management.replace('\n', '').replace('<br /></span>]', '').replace('&amp;','&').split('<br />')
       
        if draft1_management[0] == "Investors (current and":
            pass
        elif draft1_management[0] == "Investment Data - Preferred":
            pass
        
    for a in draft1_management:
        if a.count("Investors (current and") > 0:
            pass
        elif a.count('Investment Data - Preferred') > 0:
            pass
        elif a.count(',') == 0:
            index = draft1_management.index(a)
            index_before = index - 1 
            x = draft1_management[index]
            y = draft1_management[index_before]
            z = y + ' ' + x
            new = ''. join(z)
            draft1_management[index] = new
            del draft1_management[index_before] 
        elif a.count('<')>=1:
            split_a = a.split('>')
            index = draft1_management.index(a)
            draft1_management[index] = split_a[-1]
    #print draft1_management

    name = ""
    outfile = open("./Management_TEST_V1.csv", "a")
    fieldnames = ["Company", "Executive", "Position"]
    writer = csv.DictWriter(outfile, fieldnames = fieldnames)
    #writer.writeheader()

    management = []
    for a in draft1_management:
        a_1 = str(a).split(',')
        name = a_1.pop(0) 
        b = ','.join(a_1)
        a = [name, ','.join(a_1)] 
        
        dict_instance1["Company"] = company_name
        dict_instance1["Executive"] = name
        dict_instance1["Position"] = b

        management.append(
        {
            "Company" : company_name,
            "Executive" : name,
            "Position" : b
        }
        );

        writer.writerow({
            "Company" : company_name,
            "Executive" : name,
            "Position" : b
        })

    print management
    #print dict_instance1

    #INVESTOR TAB------------------------------------------------
    if soup.find(text="Investors (current and\n") == None:
        pass

    else:
        investor = soup.find(text="Investors (current and\n").parent.parent.nextSibling.contents
        investor_alt = soup.find(text="Investors (current and\n").parent.parent.nextSibling.nextSibling.contents
        
        test = investor[0].text
        if test == "Comparable PrivateCompanies":
            investor = investor_alt

        investor = str(investor)
        investor = investor.replace('\n', '').replace('<br /></span>]', '').replace('&amp;','&').replace('. ','.').split('<br />')
        investor[0] = str(investor[0]).split('>')
        investor[0] = investor[0][1]

        name = ""
        outfile = open("./Investor_TEST_V1.csv", "a")
        fieldnames = ["Company", "Investor"]
        writer = csv.DictWriter(outfile, fieldnames = fieldnames)
        #writer.writeheader()

        for a in investor:

            dict_instance1["Company"] = company_name
            dict_instance1["Executive"] = a

            if a.count('<') >= 1:
                split_a = a.split('>')
                print split_a
                print split_a[-1]
               
                index = investor.index(a)
                investor[index] = split_a[-1]

            writer.writerow({
                    "Company" : company_name,
                    "Investor" : a
                })
    print investor

    #COMPARABLES TAB------------------------------------------------
    if soup.find('div', text = re.compile('Comparable Private\n')) == None:
        pass
    else:
        investor = soup.find(text="Investors (current and\n").parent.parent.nextSibling.contents
        comparables = soup.find('div', text = re.compile('Comparable Private\n')).parent.parent.nextSibling.contents
        comparables_alt = soup.find('div', text = re.compile('Comparable Private\n')).parent.parent.nextSibling.nextSibling.contents

        test = investor[0].text
        if test == "Comparable PrivateCompanies":
            comparables = comparables_alt

        comparables = str(comparables)
        comparables = comparables.replace('\n', '').replace('<br /></span>]', '').replace('&amp;','&').replace('. ','.').split('<br />')
        comparables[0] = str(comparables[0]).split('>')
        comparables[0] = comparables[0][1]

        name = ""
        outfile = open("./Comparables_TEST_V1.csv", "a")
        fieldnames = ["Company", "Comparable_PrivCo"]
        writer = csv.DictWriter(outfile, fieldnames = fieldnames)   
        #writer.writeheader()

        for a in comparables:
            dict_instance1["Company"] = company_name
            dict_instance1["Comparable_PrivCo"] = a

            writer.writerow({
                    "Company" : company_name,
                    "Comparable_PrivCo" : a
                    })

        print comparables
