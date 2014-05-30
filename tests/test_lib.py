from pdf2img import Pdf2Img
from unittest import main
from unittest import TestCase
import hashlib
import os
import shutil


PDF_PATH = './tests/handbuch.pdf'


class TestPdf2img(TestCase):

    def setUp(self):
        self.converter = Pdf2Img()

    def tearDown(self):
        if os.path.exists(os.path.abspath(self.converter.path)):
            shutil.rmtree(self.converter.path)

    def test_count_pages(self):
        result = self.converter.count_pages(
            os.path.abspath(PDF_PATH))
        self.assertEquals(61, result, 'Expect 11 pages')

    def test_get_destination_folder(self):
        filehandler = open(PDF_PATH, 'rb')
        exists, result = self.converter.destination_folder(filehandler)

        self.assertFalse(exists)
        self.assertEquals(hashlib.sha256(filehandler.read()).hexdigest(),
                          result)

        filehandler.close()

    def test_get_destination_folder_exists(self):
        self.converter.convert(
            os.path.abspath(PDF_PATH))

        filehandler = open(PDF_PATH, 'rb')
        exists = self.converter.destination_folder(filehandler)[0]

        self.assertTrue(exists)
        filehandler.close()

    def test_get_resources(self):
        filehandler = open(PDF_PATH, 'rb')
        expected = self.converter.convert(
            os.path.abspath(PDF_PATH))
        hash_ = self.converter.destination_folder(filehandler)[1]

        result = self.converter.get_resources(hash_)
        self.assertEquals(expected, result)

    def test_converter(self):
        result = self.converter.convert(
            os.path.abspath(PDF_PATH))

        self.assertEquals(5, len(result), 'Expect five images')


if __name__ == "__main__":
    main()
