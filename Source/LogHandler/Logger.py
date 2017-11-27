import time
import os
import ntpath
ntpath.basename("a/b/c")


class Logger(object):

    @staticmethod
    def logging(listofFiles, file):
        timestamp = 'ACSM5_' + str(time.strftime('%Y_%m_%d_%H_%M'))
        pathdir = os.path.dirname(os.path.realpath(__file__))
        filedir = os.path.dirname(pathdir)
        try:
            logfilename = filedir + '\\History\\' + timestamp
            logfile = open(filedir + '\\History\\' + timestamp, "w")
        except IOError as e:
            logfile = open((os.path.dirname(filedir)) + '\\History\\' + timestamp, "w")
            logfilename = (os.path.dirname(filedir)) + '\\History\\' + timestamp
            print(e)
            return 'Error creating logfile'
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
    def file_preparing(listofFiles):
        timestamp = 'ACSM5_' + str(time.strftime('%Y_%m_%d_%H_%M'))
        pathdir = os.path.dirname(os.path.realpath(__file__))
        filedir = os.path.dirname(pathdir)
        logfilename = filedir + '\\History\\' + timestamp
        try:
            logfile = open(filedir + '\\History\\' + timestamp, "w")
        except IOError:
            logfile = open((os.path.dirname(filedir)) + '\\History\\' + timestamp, "w")
            logfilename = (os.path.dirname(filedir)) + '\\History\\' + timestamp
        logfile.write(
            'Process Finished files has been added to the requested directory. TAL file Created')
        logfile.write(str(time.strftime('\n' + 'Date: ' '%Y-%m-%d:%H:%M')))
        logfile.write('\n' + '-' * 60 + '\n')
        [logfile.write(i + '\n') for i in listofFiles]
        logfile.close()
        return logfilename

    @staticmethod
    def path_leaf(path):
        '''Extract file name from path '''
        head, tail = ntpath.split(path)
        return tail or ntpath.basename(head)

if __name__ == "__main__":
    pathdir = os.path.dirname(os.path.realpath(__file__))
    filedir = os.path.dirname(pathdir)
    print (os.path.dirname(filedir))
