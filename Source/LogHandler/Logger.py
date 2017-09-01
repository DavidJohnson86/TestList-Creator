import time
import os
import ntpath
ntpath.basename("a/b/c")


class Logger(object):

    @staticmethod
    def logging(listofFiles, file):
        timestamp = 'ACSM5_' + str(time.strftime('%Y_%m_%d_%H_%M'))
        pathdir = os.getcwd()
        logfilename = pathdir + '\\History\\' + timestamp
        logfile = open(pathdir + '\\History\\' + timestamp, "w")
        logfile.write('Process Finished ' +
                      str(len(listofFiles)) +
                      ' test cases has been added to the testlist. ')
        logfile.write(str(time.strftime('\n' + 'Date: ' '%Y-%m-%d:%H:%M')) + '\n')
        logfile.write(str(Logger.path_leaf(str(file))))
        logfile.write('\n' + '-' * 60 + '\n')
        [logfile.write(i + '\n') for i in listofFiles]
        logfile.close()
        return logfilename

    @staticmethod
    def path_leaf(path):
        '''Extract file name from path '''
        head, tail = ntpath.split(path)
        return tail or ntpath.basename(head)
