import argparse
from pdf2img import Pdf2Img


def main():
    parser = argparse.ArgumentParser(
        description='Converts pdf pages to images with ghostscript')

    parser.add_argument('pdf_file', help='The pdf file')
    parser.add_argument('-o',
                        '--output',
                        default='./var',
                        help='Output directiry, default is "./var".')

    parser.add_argument('-p',
                        '--pages',
                        type=int,
                        default=5,
                        help='Amoint of pages to be converted. -1 means all')

    args = parser.parse_args()

    output = args.output
    pdf_file = args.pdf_file
    pages = args.pages

    print "Converting {0} pages of the pdf file <{1}> to {2}".format(
        pages,
        pdf_file,
        output
        )

    converter = Pdf2Img(output, limit=pages)
    converter.convert(pdf_file)


if __name__ == '__main__':
    main()
