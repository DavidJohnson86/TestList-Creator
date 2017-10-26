'''
==============================================================================
Main modules for parsing and modifying Xml Files for BMW ACSM5 Project
==============================================================================
                            OBJECT SPECIFICATION
==============================================================================
$ProjectName: BMW ACSM5
$Source: Parser.py
$Revision: 1.1 $
$Author: David Szurovecz $
$Date: 2017/07/14 16:05:32CEST $

============================================================================
'''

from lxml import etree


class XmlParser(object):

    XML_ATTRS = {}
    XML_FAILED = []

    def __init__(self, source):
        INFILE = source
        self.INFILE_ROOT = INFILE.getroot()
        self.get_allfailedobject()

    def get_testnames(self):
        try:
            XmlParser.XML_ATTRS['name'] = [element.attrib['val'] for element in self.INFILE_ROOT.xpath(
                "//COMPA-REPORT//SEQ[@TestVariationIndex]//ATTR[@id='TestVariation']")]
        except IndexError:
            XmlParser.XML_ATTRS['name'] = ''

    def get_allfailedobject(self):
        ''' Parsing all the nodes with all data where FailedMeasurements > 0'''
        try:
            XmlParser.XML_FAILED = [element for element in self.INFILE_ROOT.xpath(
                "//COMPA-REPORT//SEQ[@TestVariationIndex]") if element[13].attrib['id'] == "FailedMeasurements" and int(element[13].attrib['val']) > 0]
        except IndexError:
            XmlParser.XML_FAILED = []

    def get_failedtestnames(self):
        try:
            XmlParser.XML_ATTRS['failed'] = [element[7].attrib['val']
                                             for element in XmlParser.XML_FAILED]
        except IndexError:
            XmlParser.XML_ATTRS['failed'] = ''


class ListCreator(object):

    @staticmethod
    def testlist_creator(listofFailed, output, inlist):
        row_counter, set_counter = 0, 0
        inlist_root = inlist.getroot()
        for test_sets in range(1, len(inlist_root[0]), 2):
            try:
                elem = inlist_root[0][test_sets][0]
            except IndexError:
                print('error')
                return False
            for test_cases in range(0, len(elem)):
                if elem[test_cases].tag == 'ENABLED':
                    row_counter = 0
                    numof_testcases = 1 + len(elem[test_cases].text) / 2
                    test_states = numof_testcases * [0]
                    test_status = elem[test_cases]
                row_counter += 1
                set_counter += 1
                if elem[test_cases].text in listofFailed:
                    test_states[row_counter - 2] = 1
                    test_status.text = str(test_states)[1:-1:]
        try:
            inlist.write(str(output))
        except IOError:
            return False
        return True
