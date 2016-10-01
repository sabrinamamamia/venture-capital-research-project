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

files = open("master_list.txt", "r")
files = files.readlines()
files = map(lambda s: s.strip(), files)
#print files

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

    def scrape(value):
        reorganization = soup.findAll(text=re.compile("Reorganization"))
        if len(reorganization) != size: 
            print "None - list index out of range"
        else:
            reorganization_1 = reorganization[value].parent.nextSibling.text
            reorganization_1 = str(reorganization_1)
            reorganization_1 = reorganization_1.replace(": ", "")
            dict_instance1["Reorganization"] = reorganization_1
            #print reorganization
            #print reorganization_1

        dividends = soup.findAll(text="Cumulative Dividends")
        if len(dividends) != size: 
            print "None - list index out of range"
        else:
            dividends_1 = dividends[value].parent.nextSibling.text
            dividends_1 = str(dividends_1)
            dividends_1 = dividends_1.replace(": ", "")
            dict_instance1["Cum_Dividends"] = dividends_1
            #print dividends
            #print dividends_1

        redemption = soup.findAll(text="Redemption")
        if len(redemption) != size: 
            print "None - list index out of range"
        else:
            redemption_1 = redemption[value].parent.nextSibling.text
            redemption_1 = str(redemption_1)
            redemption_1 = redemption_1.replace(": ", "")
            dict_instance1["Redemption"] = redemption_1
            #print redemption
            #print redemption_1

        dilution = soup.findAll(text="Anti-Dilution")
        if len(dilution) != size: 
            print "None - list index out of range"
        else:
            dilution_1 = dilution[value].parent.nextSibling.text
            dilution_1 = str(dilution_1)
            dilution_1 = dilution_1.replace(": ", "")
            dict_instance1["Anti_Dilution"] = dilution_1
            #print dilution
            #print dilution_1

        stocktype = soup.findAll(text="Stock Type")
        if len(stocktype) != size: 
            print "None - list index out of range"
        else:
            stocktype_1 = stocktype[value].parent.nextSibling.text
            stocktype_1 = str(stocktype_1)
            stocktype_1 = stocktype_1.replace(": ", "")
            dict_instance1["Type"] = stocktype_1
            #print stocktype
            #print stocktype_1

        liqmult = soup.findAll(text="Liq. Multiple")
        if len(liqmult) != size: 
            print "None - list index out of range"
        else:
            liqmult_1 = liqmult[value].parent.nextSibling.text
            liqmult_1 = str(liqmult_1)
            liqmult_1 = liqmult_1.replace(": ", "")
            dict_instance1["Liq_Multiple"] = liqmult_1

        liqpref = soup.findAll(text="Liquidation Pref.")
        if len(liqpref) != size: 
            print "None - list index out of range"
        else:
            liqpref_1 = liqpref[value].parent.nextSibling.text
            liqpref_1 = str(liqpref_1)
            liqpref_1 = liqpref_1.replace(": ", "")
            dict_instance1["Liquidation_Pref"] = liqpref_1

        direction = soup.findAll(text="Direction")
        if len(direction) != size: 
            print "None - list index out of range"
        else:
            direction_1 = direction[value].parent.nextSibling.text
            direction_1 = str(direction_1)
            direction_1 = direction_1.replace(": ", "")
            dict_instance1["Direction"] = direction_1

        round_x = soup.findAll(text="Round")
        if len(round_x) != size: 
            print "None - list index out of range"
        else:
            round_x = round_x[value].parent
            round_1 = round_x.nextSibling.text
            round_1 = str(round_1)
            round_1 = round_1.replace(": ", "")
            dict_instance1["Round"] = round_1

        a = round_x.parent.previousSibling
        #print "ROUND:"
        #print a.text
        a1 = a.text
        if a1.count('-') == 2:
            dict_instance1["Date"] = a1
        if a1.count('.') == 1 and a1.count('$') == 0 and a1.count('a') == 0:
            dict_instance1["Amount"] = a1
        if a1.count('$') == 1 and a1.count('.') == 0:
            dict_instance1["Valuation"] = a1
        if a1.count(',') > 0 and a1.count('$') == 0 and a1.count('%') == 0: 
            dict_instance1["Shares"] = a1
        if a1.count('$') == 1 and a1.count('.') == 1:
            dict_instance1["Price"] = a1
        else:
            dict_instance1["???"] = a1

        a2 = a.previousSibling.text
        if a2.count('%') > 0:
            print "Finished scraping round data."
        else:
            if a2.count('-') == 2:
                dict_instance1["Date"] = a2
            if a2.count('.') == 1 and a2.count('$') == 0 and a2.count('a') == 0:
                dict_instance1["Amount"] = a2
            if a2.count('$') == 1 and a2.count('.') == 0:
                dict_instance1["Valuation"] = a2
            if a2.count(',') > 0 and a2.count('$') == 0 and a2.count('%') == 0:
                dict_instance1["Shares"] = a2 
            if a2.count('$') == 1 and a2.count('.') == 1:
                dict_instance1["Price"] = a2
            else:
                dict_instance1["???"] = a2

            a3 = a.previousSibling.previousSibling.text
            if a3.count('%') > 0:
                print "Finished scraping round data."
            else:
                if a3.count('-') == 2:
                    dict_instance1["Date"] = a3
                if a3.count('.') == 1 and a3.count('$') == 0 and a3.count('a') == 0:
                    dict_instance1["Amount"] = a3
                if a3.count('$') == 1 and a3.count('.') == 0:
                    dict_instance1["Valuation"] = a3
                if a3.count(',') > 0 and a3.count('$') == 0 and a3.count('%') == 0:
                    dict_instance1["Shares"] = a3
                if a3.count('$') == 1 and a3.count('.') == 1:
                    dict_instance1["Price"] = a3
                else:
                    dict_instance1["???"] = a3

                a4 = a.previousSibling.previousSibling.previousSibling.text
                if a4.count('%') > 0:
                    print "Finished scraping round data."
                else:
                    if a4.count('-') == 2:
                        dict_instance1["Date"] = a4
                    if a4.count('.') == 1 and a4.count('$') == 0 and a4.count('a') == 0:
                        dict_instance1["Amount"] = a4
                    if a4.count('$') == 1 and a4.count('.') == 0:
                        dict_instance1["Valuation"] = a4
                    if a4.count(',') > 0 and a4.count('$') == 0 and a4.count('%') == 0:
                        dict_instance1["Shares"] = a4
                    if a4.count('$') == 1 and a4.count('.') == 1:
                        dict_instance1["Price"] = a4
                    else:
                        dict_instance1["???"] = a4

                    a5 = a.previousSibling.previousSibling.previousSibling.previousSibling.text
                    if a5.count('%') > 0:
                        print "Finished scraping round data."
                    else:
                        if a5.count('-') == 2:
                            dict_instance1["Date"] = a5
                        if a5.count('.') == 1 and a5.count('$') == 0 and a5.count('a') == 0:
                            dict_instance1["Amount"] = a5
                        if a5.count('$') == 1 and a5.count('.') == 0:
                            dict_instance1["Valuation"] = row
                        if a5.count(',') > 0 and a5.count('$') == 0 and a5.count('%') == 0:
                            dict_instance1["Shares"] = a5
                        if a5.count('$') == 1 and a5.count('.') == 1 and a5.count('$') == 0:
                            dict_instance1["Price"] = a5
                        else:
                            dict_instance1["???"] = a5

        print dict_instance1

        outfile = open("./Rounds_TEST.csv", "a")
        writer = csv.writer(outfile)
        writer.writerow([dict_instance1["???"],dict_instance1["Company"],dict_instance1["Date"],dict_instance1["Amount"],dict_instance1["Valuation"],dict_instance1["Shares"],dict_instance1["Price"],dict_instance1["Round"],dict_instance1["Direction"],
                        dict_instance1["Liquidation_Pref"],dict_instance1["Liq_Multiple"],dict_instance1["Anti_Dilution"],dict_instance1["Redemption"],dict_instance1["Cum_Dividends"],dict_instance1["Reorganization"]])

        
    #pdf = "/Users/sabrinama/RetailMeNot Inc.pdf"
    html = convert_pdf_to_txt(a)
    soup = BeautifulSoup(html)
    #print soup

    company_name = str(pdf)
    company_name = company_name.replace('.pdf', '').replace('/Users/sabrinama/', '')

    #company_name = str(html)
    #company_name = company_name.replace('.pdf', '')
    #if company_name.count('-') > 0:
    #    company_name = company_name.replace('-', '')
    #print company_name

    dict = {"Company": None, "Date": None, "Amount": None, "Valuation": None, "Shares": None, "Price": None, 
            "Round": None, "Direction": None, "Liquidation_Pref": None, "Liq_Multiple": None,
            "Type": None, "Anti_Dilution": None, "Redemption": None, "Cum_Dividends": None, 
            "Reorganization": None, "???": None
            }

    dict_instance1 = dict;
    dict_instance1["Company"] = company_name

    number_of_rounds = soup.findAll(text=re.compile("Round"))
    size = len(number_of_rounds)

    if size == 1:
        scrape(0)

    if size == 2:
        scrape(0)
        scrape(1)

    if size == 3:
        scrape(0)
        scrape(1)
        scrape(2)

    if size == 4:
        scrape(0)
        scrape(1)
        scrape(2)
        scrape(3)

    if size == 5:
        scrape(0)
        scrape(1)
        scrape(2)
        scrape(3)
        scrape(4)

    if size == 6:
        scrape(0)
        scrape(1)
        scrape(2)
        scrape(3)
        scrape(4)
        scrape(5)

    if size == 7:
        scrape(0)
        scrape(1)
        scrape(2)
        scrape(3)
        scrape(4)
        scrape(5)
        scrape(6)

    if size == (8):
        scrape(0)
        scrape(1)
        scrape(2)
        scrape(3)
        scrape(4)
        scrape(5)
        scrape(6)
        scrape(7)

    if size == (9):
        scrape(0)
        scrape(1)
        scrape(2)
        scrape(3)
        scrape(4)
        scrape(5)
        scrape(6)
        scrape(7)
        scrape(8)
