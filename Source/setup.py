from distutils.core import setup
import py2exe
import Report_Parser
import LogHandler

setup(
    windows=[{'script': r'd:\10_Development\Python\TL_Creater\Application.py'}],
    options={
        'py2exe': 
        {
            'includes': ['lxml.etree', 'lxml._elementpath', 'gzip','Report_Parser.Parser','LogHandler.Logger'],
        }
    }
)