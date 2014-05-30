import hashlib
import os
import subprocess


COMMAND_COUNT_PDF_PAGES = ('gs -q -dNOSISPLAY -c "({path}) '
                           ' (r) file runpdfbegin pdfpagecount = quit"')


COMMAND_CONVERT_PDF_PAGE = ['gs',
                            '-q',
                            '-dSAFER',
                            '-dBATCH',
                            '-dNOPAUSE',
                            '-sDEVICE=png16m',
                            '-dGraphicsAlphaBits=4',
                            '-dTextAlphaBits=4',
                            '-r150x150',
                            '-']


class Pdf2Img(object):

    def __init__(self, output='./var'):
        self.path = output
        self.create_structure()

    def create_structure(self):
        if not os.path.exists(self.path):
            print "Create missing storage directory: {0}".format(
                os.path.abspath(self.path))
            os.makedirs(self.path, mode=0700)

    def count_pages(self, path):
        process = subprocess.Popen(
            COMMAND_COUNT_PDF_PAGES.format(**{'path': path}),
            bufsize=-1,
            shell=True,
            stdout=subprocess.PIPE)
        result = process.communicate()[0]
        return_code = process.returncode

        if return_code == 0:
            print "Ghostscript counted amount of pages in {0}".format(path)
        else:
            print "Ghostscript process did not exit cleanly! "
            print "Error Code: {0}".format(return_code)

        return int(result)

    def destination_folder(self, filehandler):
        filehandler.seek(0)
        hash_ = hashlib.sha256(filehandler.read()).hexdigest()
        destination = '{0}/{1}'.format(self.path, hash_)
        exists = True

        if not os.path.exists(destination):
            os.makedirs(destination)
            exists = False

        filehandler.seek(0)
        return exists, hash_

    def get_resources(self, folder):
        resources = []
        for file_ in os.listdir('{0}/{1}'.format(self.path, folder)):
            resources.append('{0}/{1}'.format(folder, file_))
        return resources

    def convert(self, path, limit=5):
        """Converts a pdf to images using ghostscript"""
        pdf = open(path, 'r')
        pages = self.count_pages(path)
        exists, folder = self.destination_folder(pdf)
        resoruces = []

        if exists:
            return self.get_resources(folder)

        if limit == -1:
            limit = pages

        for page in range(1, pages + 1)[:limit]:

            output = './var/{0}/{1}_image.png'.format(folder, page)

            command = COMMAND_CONVERT_PDF_PAGE[:]
            command.insert(-1, '-dFirstPage={0:d}'.format(page))
            command.insert(-1, '-dLastPage={0:d}'.format(page))
            command.insert(-1, '-sOutputFile={0}'.format(output))

            process = subprocess.Popen(command,
                                       bufsize=-1,
                                       stdout=subprocess.PIPE,
                                       stdin=subprocess.PIPE)
            pdf.seek(0)
            process.stdin.write(pdf.read())
            process.communicate()[0]
            process.stdin.close()
            return_code = process.returncode
            if return_code == 0:
                print "Ghostscript processed one page of a pdf file."
                resoruces.append('{0}/{1}_image.png'.format(folder, page))
            else:
                print "Ghostscript process did not exit cleanly! "
                print "Error Code: {0}".format(return_code)

        return resoruces
