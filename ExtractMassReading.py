##
# This script is for extracting the reading at mass for the day.
##

from datetime import date

import requests
from lxml import html

# The url of the reading
urlUniversalisStr = 'https://www.universalis.com/800/mass.htm'
# The tags expected to have some text to be extrated
neededTag = ['td', 'div', 'i']
# Feast Name
feastName = ''
# Section title
sectionLists = ['First reading', 'Responsorial Psalm', 'Second reading', 'Gospel Acclamation', 'Gospel']

tmpFile = 'tempFile.tmp'


def get_filename_datetime(feastName):
    # Use current date to get a text file name.
    return feastName + " - " + str(date.today()) + ".txt"


def keep_text(text, thefile):
    # For new section, add a blank line
    if text in sectionLists:
        thefile.write('\n\n')
    thefile.write('\n' + text)


def keep_reading_text(tagName, text, thefile):
    thefile.write('\n' + text)


# Extracting the text
def getMassReadingPage():
    page = requests.get(urlUniversalisStr)
    tree = html.fromstring(page.content)

    # feast name
    feastName = tree.xpath('//*[@id="feastname"]/strong/text()')
    # date name
    dateName = tree.xpath('//*[@id="datename"]/tt/text()')

    fileName = get_filename_datetime(feastName[0])
    thefile = open(fileName, 'a')

    keep_text(feastName[0], thefile)
    keep_text(dateName[0], thefile)

    for tag in tree.iter():
        if tag.tag == 'tr':
            thtags = tag.xpath('th')
            for thtag in thtags:
                keep_text(thtag.text, thefile)

        if not len(tag):
            if tag.tag in neededTag:
                if tag.text:
                    txt = tag.text.rstrip()
                    keep_reading_text(tag.tag, txt, thefile)

    thefile.close()


# The main text
def main():
    getMassReadingPage()


# Main process
if __name__ == "__main__":
    main()
