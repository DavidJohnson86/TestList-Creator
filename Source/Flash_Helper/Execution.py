'''
Created on 2017. okt. 24.

@author: SzuroveczD
'''

import shutil
import os


class Execute(object):

    INIT_PASS = '[INFO]: ALL FILE IS AVAILABLE FOR FLASHING'
    INIT_FAIL = '[ERROR]: ONE OR MORE FILE IS MISSING FROM THE SOURCE DIRECTORY'
    COPY_PASS = '[INFO]: FILES COPIED TO THE REQUESTED FOLDER'
    TAL_PASS = '[INFO]: TAL FILE CREATION SUCESS'
    DIR_EXIST = '[INFO]: DIRECTORY EXIST FOR THE CURRENT SW'

    def __init__(self, source_folder, destination_folder, console=True):
        self.console = console
        self.source_folder = source_folder
        self.destination_folder = destination_folder
        self.SW_VER = None
        self.BTLD_VER = None
        self.TAL_SAMPLE = 'TAL_SAMPLE.xml'
        self.TAL_FILE = None
        self.TAL_SOURCE = os.path.dirname(
            os.path.realpath(__file__)) + '\Files\TAL_SAMPLE.xml'
        self.CAFs = {
            'CAF1B2F': None,
            'CAF1B2A': None,
            'CAF1B29': None,
            'CAF1B2B': None,
            'CAF1B2C': None,
            'CAF1B2D': None,
            'CAF2ABF': None,
            'CAF1B2E': None}
        self.directories = ['/CAF', '/SWE', '/TAL']
        self.strbuilder = ''

    def set_SW_VER(self, value):
        self.SW_VER = value

    def set_BTLD_VER(self, value):
        self.BTLD_VER = value

    def set_TAL_file(self):
        self.TAL_FILE = 'TAL_ACSM05_SWFL_' + self.SW_VER + '_Original_CAFs.xml'

    def get_version(self, file):
        return ('_'.join(os.path.splitext(file)[0].split('_')[-3:]))

    def verification(self):
        return (any([True for elem in self.CAFs if self.CAFs[elem]]))

    def message_handler(self, message):
        if self.console:
            print(message)
        else:
            self.strbuilder += '\n' + str(message)

    def get_message_buffer(self):
        return self.strbuilder.split('\n')

    def get_CAFs(self):
        return self.CAFs.values()

    def create_folders(self):
        for folder in self.directories:
            os.chdir(self.destination_folder + folder)
            try:
                os.mkdir(self.SW_VER)
            except WindowsError:
                self.message_handler(Execute.DIR_EXIST)

    def init_files(self):
        self.CAFs = (
            {elem: file for elem in self.CAFs for file in os.listdir(
                self.source_folder)if str(elem.lower())[3:] in file})
        self.SW_VER = self.get_version(self.CAFs['CAF1B2F'])
        self.BTLD_VER = self.get_version(self.CAFs['CAF1B2E'])
        if self.verification():
            self.message_handler(Execute.INIT_PASS)
            self.steps()
        else:
            self.message_handler(Execute.INIT_FAIL)

    def tal_creator(self):
        '''Creates the TAL file to the specific directory'''
        working_directory = self.destination_folder + '/TAL/' + self.SW_VER
        self.copy_to(self.TAL_SOURCE, working_directory)
        os.chdir(working_directory)
        self.set_TAL_file()
        try:
            os.rename(self.TAL_SAMPLE, self.TAL_FILE)
        except Exception as e:
            self.message_handler(e)

    def steps(self):
        # -- Create SW_VER Folder to the corresponding Directory
        self.create_folders()
        for file_name in os.listdir(self.source_folder):
            try:
                if 'cafd' in file_name:
                    self.copy_to(self.source_folder + '\\' + file_name, self.destination_folder +
                                 '\\CAF' + '\\' + self.SW_VER)
                elif 'swfl' or 'btld' in file_name:
                    self.copy_to(self.source_folder + '\\' + file_name, self.destination_folder +
                                 '\\SWE' + '\\' + self.SW_VER)
            except Exception as e:
                self.message_handler(e)
        self.tal_creator()
        self.parser()

    def copy_to(self, source_file, destination_folder):
        try:
            shutil.copy(source_file, destination_folder)
        except Exception as e:
            self.message_handler(Exception(e))

    def parser(self):
        self.TAL_FILE_LOC = self.destination_folder + '\\TAL\\' + self.SW_VER + '\\' + self.TAL_FILE
        from lxml import etree
        self.input_xml = etree.parse(self.TAL_FILE_LOC)
        self.input_xml_root = self.input_xml.getroot()
        # -- Define Required Element indexes
        CAF1B2F = self.input_xml_root[1][1][0][0]  # SWFL
        CAF1B2A = self.input_xml_root[2][1][1][0]
        CAF1B29 = self.input_xml_root[2][1][0][0]
        CAF1B2B = self.input_xml_root[2][1][2][0]
        CAF1B2C = self.input_xml_root[2][1][3][0]
        CAF1B2D = self.input_xml_root[2][1][4][0]
        CAF2ABF = self.input_xml_root[2][1][5][0]
        CAF1B2E = self.input_xml_root[3][0][0][0]  # BTLD
        version = [2, 3, 4]
        #--Iterate Through Elements in the XML Fiel
        for element in [CAF1B2F, CAF1B2A, CAF1B29, CAF1B2B, CAF1B2C, CAF1B2D, CAF2ABF, CAF1B2E]:
            # Change the XML element example: 00001B29 to CAF1B29
            component_id = ('CAF' + str(element[1].text)[-4:])
            # Create list from the version number of CAF file name
            caf_id = self.get_version(self.CAFs[component_id]).split('_')
            if component_id in self.CAFs:
                for file_index, element_index in enumerate(version):
                    current_file_ver = caf_id[file_index]
                    element[element_index].text = current_file_ver
        self.input_xml.write(self.TAL_FILE)

if __name__ == "__main__":
    source = r'd:\temp\006_005_001'
    dest = r'c:\Data'
    obj = Execute(source, dest)
    obj.init_files()
