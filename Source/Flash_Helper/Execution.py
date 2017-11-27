'''
Created on 2017. okt. 24.

@author: SzuroveczD
'''

import shutil
import os


class Execute(object):
    """This class includes everything for preparing Flashing process on BMW
    ACSM5 project: file management and TAL file creation.
    :param source_folder: The path where the SW files are available.
    :param destination_folder: The path of E-Sys/Data folder
    :paramm console: shows action on standard output"""

    INIT_PASS = '[INFO]: ALL FILE IS AVAILABLE FOR FLASHING'
    INIT_FAIL = '[ERROR]: ONE OR MORE FILE IS MISSING FROM THE SOURCE DIRECTORY'
    COPY_PASS = '[INFO]: FILES COPIED TO THE REQUESTED FOLDER'
    TAL_PASS = '[INFO]: TAL FILE CREATION SUCESS'
    DIR_EXIST = '[INFO]: DIRECTORY EXIST FOR THE CURRENT SW'

    def __init__(self, source_folder, destination_folder, console=True):
        self.source_folder = source_folder
        self.destination_folder = destination_folder
        self.console = console
        self.sw_ver = None
        self.btld_ver = None
        self.tal_file = None
        self.tal_sample = 'tal_sample.xml'
        self.tal_source = os.path.dirname(
            os.path.realpath(__file__)) + r'\Files\tal_sample.xml'
        self.cafs = {
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

    def set_sw_ver(self, value):
        """Set SW version."""
        self.sw_ver = value

    def set_btld_ver(self, value):
        """Set Boot Loader version."""
        self.btld_ver = value

    def set_tal_file(self):
        """Set TAL file name."""
        self.tal_file = 'TAL_ACSM05_SWFL_' + self.sw_ver + '_Original_CAFs.xml'

    @staticmethod
    def get_version(file):
        """Extract SW version from file name."""
        return '_'.join(os.path.splitext(file)[0].split('_')[-3:])

    def verification(self):
        """Return True if all required file found."""
        return any([True for elem in self.cafs if self.cafs[elem]])

    def message_handler(self, message):
        """Print Status if True else store it in a variable."""
        if self.console:
            print(message)
        else:
            self.strbuilder += '\n' + str(message)

    def get_message_buffer(self):
        """Return all stored status data."""
        return self.strbuilder.split('\n')

    def get_cafs(self):
        """Return all CAF file names."""
        return self.cafs.values()

    def create_folders(self):
        """Create folders with same name as SW version in the specified folders."""
        for folder in self.directories:
            os.chdir(self.destination_folder + folder)
            try:
                os.mkdir(self.sw_ver)
            except WindowsError:
                self.message_handler(Execute.DIR_EXIST)
        self.steps()

    def init_files(self):
        """Get the SW and Boot Loader version, map the files and check that all file
        is available for flashing."""
        self.cafs = (
            {elem: file for elem in self.cafs for file in os.listdir(
                self.source_folder)if str(elem.lower())[3:] in file})
        if self.verification():
            self.message_handler(Execute.INIT_PASS)
            self.sw_ver = self.get_version(self.cafs['CAF1B2F'])
            self.btld_ver = self.get_version(self.cafs['CAF1B2E'])
            return True
        else:
            self.message_handler(Execute.INIT_FAIL)
            return False

    def tal_creator(self):
        '''Copies the TAL file sample to the specific directory.'''
        working_directory = self.destination_folder + '/TAL/' + self.sw_ver
        self.copy_to(self.tal_source, working_directory)
        os.chdir(working_directory)
        self.set_tal_file()
        try:
            os.rename(self.tal_sample, self.tal_file)
        except Exception as error:
            self.message_handler(error)

    def steps(self):
        """Create Folders,copy the files to the requested directory and moving the
        TAL sample file to the requested location."""
        for file_name in os.listdir(self.source_folder):
            try:
                if 'cafd' in file_name:
                    self.copy_to(self.source_folder + '\\' + file_name, self.destination_folder +
                                 '\\CAF' + '\\' + self.sw_ver)
                elif 'swfl' or 'btld' in file_name:
                    self.copy_to(self.source_folder + '\\' + file_name, self.destination_folder +
                                 '\\SWE' + '\\' + self.sw_ver)
            except Exception as error:
                self.message_handler(error)
        self.tal_creator()
        self.parser()

    def copy_to(self, source_file, destination_folder):
        """Copy the source file to the destination folder"""
        try:
            shutil.copy(source_file, destination_folder)
        except Exception as error:
            self.message_handler(Exception(error))

    def parser(self):
        """Parse the TAL file modify parameter and SW version number"""
        tal_file_loc = self.destination_folder + '\\TAL\\' + self.sw_ver + '\\' + self.tal_file
        from lxml import etree
        input_xml = etree.parse(tal_file_loc)
        input_xml_root = input_xml.getroot()
        # -- Define Required Element indexes
        CAF1B2F = input_xml_root[1][1][0][0]  # SWFL
        CAF1B2A = input_xml_root[2][1][1][0]
        CAF1B29 = input_xml_root[2][1][0][0]
        CAF1B2B = input_xml_root[2][1][2][0]
        CAF1B2C = input_xml_root[2][1][3][0]
        CAF1B2D = input_xml_root[2][1][4][0]
        CAF2ABF = input_xml_root[2][1][5][0]
        CAF1B2E = input_xml_root[3][0][0][0]  # BTLD
        version = [2, 3, 4]
        #--Iterate Through Elements in the XML Fiel
        for element in [CAF1B2F, CAF1B2A, CAF1B29, CAF1B2B, CAF1B2C, CAF1B2D, CAF2ABF, CAF1B2E]:
            # Change the XML element example: 00001B29 to CAF1B29
            component_id = ('CAF' + str(element[1].text)[-4:])
            # Create list from the version number of CAF file name
            caf_id = self.get_version(self.cafs[component_id]).split('_')
            if component_id in self.cafs:
                for file_index, element_index in enumerate(version):
                    current_file_ver = caf_id[file_index]
                    element[element_index].text = current_file_ver
        input_xml.write(self.tal_file)

if __name__ == "__main__":
    SOURCE_FILE = r'd:\temp\006_005_001'
    DESTINATION_FILE = r'c:\Data'
    run = Execute(SOURCE_FILE, DESTINATION_FILE)
    if run.init_files():
        run.create_folders()
