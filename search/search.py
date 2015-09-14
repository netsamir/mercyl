#!/usr/bin/env python
# encoding: utf-8


"""Module to extract new machine from website"""


import urllib2
from bs4 import BeautifulSoup
import smtplib
import shelve
import logging
import logging.handlers
import time


# checking if there is new machine

class Search(object):
    def search(self):
        LOG_FILENAME = 'search.log'
        # Set up a specific logger with our desired output level
        my_logger = logging.getLogger('mylogger')
        my_logger.setLevel(logging.DEBUG)

        # Add the log message handler to the logger
        handler = logging.handlers.RotatingFileHandler(LOG_FILENAME,
                                                    maxBytes=100000,
                                                    backupCount=1)
        my_logger.addHandler(handler)

        while True:
            url = "http://www.machineryzone.eu/annonces.asp?trich=localisation&triordre=DESC&page=1&ianneemini=1996&distancemax=2500&iprixmini=&paysloca=loca21&action=rech&boxannee=Max%2E+year++%3A+2002&iprixmax=&aff=&ltypeann=&sprop9=580sle&numrub=313&typerech=a&typerechloca=1&valeurdefautmodele=Model&iprop3=&codepostal=1357&ianneemax=2002&lprop1=3391&boxprixht=Price+excl%2E+VAT&erreursaisierech=0&type="
            response = urllib2.urlopen(url)
            my_logger.debug('lookup url %s' % url)
            html = response.read()
            soup = BeautifulSoup(html)
            stock = soup.find_all('div', attrs={"data-id": True})
            my_logger.debug('Parsing html for ids')

            ids = []
            for annonce in stock:
                ids.append(annonce.a.attrs['data-id'])

            tracto_db = shelve.open('machines_ids.db')
            my_logger.debug('Opening DB')

            try:
                pids = tracto_db['machines_ids.db']
                my_logger.debug('Old ids %s' % pids)
                tracto_db['machines_ids.db'] = ids
                my_logger.debug('New ids %s' % ids)
            except KeyError:
                # First run
                my_logger.debug('First occurcene - creating db')
                pids = []
                tracto_db['machines_ids.db'] = pids
            finally:
                tracto_db.close()

            my_logger.debug('IDS %s' % ids)
            my_logger.debug('PIDS %s' % pids)
            diff = set(ids) - set(pids)
            my_logger.debug('Checking difference %s' % diff)
            if diff != set():
                # sending an email when we found something new
                my_logger.debug('Sending email')
                sender = "samir.sadek@mercyl.com"
                recv1 = "netsamir@gmail.com"
                recv2 = "rami@mercyl.com"
                msg = "Salut Rami, \n J'ai trouvé des nouvelles machines. \n Voici le lien vers les Case 580 SLE: \n" + url
                eman = "ssadek"
                drow = "15novY2K08"

                server = smtplib.SMTP('smtp.webfaction.com:587')
                server.starttls()
                server.login(eman, drow)
                server.sendmail(sender, recv1, msg)
                server.sendmail(sender, recv2, msg)
                server.quit()
                my_logger.debug('Email sent')

            time.sleep(600)


if __name__ == '__main__':
        s = Search()
        s.search()
