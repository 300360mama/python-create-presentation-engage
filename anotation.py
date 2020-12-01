
import PyPDF2
PDFFile = open("C:\\python_scripts\\test_py\\Imraldi_iPad_11526v4_pt.pdf",'rb')

pdf = PyPDF2.PdfFileReader(PDFFile)


# fields = pdf.getFields()
#
# print(fields)


# print(a['/Annots'][1].getObject())


numPages = pdf.getNumPages()
i = 1
while i < 2:
    page = pdf.getPage(i)
    a = page.getObject()
    print(a['/Contents'])
    b = a['/Annots'][1].getObject()
    print(b['/A'])
    i = i + 1



# for page in range(pages):
#     # print("Current Page: {}".format(page))
#     pageSliced = PDF.getPage(page)
#     pageObject = pageSliced.getObject()
#     if key in pageObject.keys():
#         ann = pageObject[key]
#         for a in ann:
#             u = a.getObject()
#             print(u['/Rect'])
#             if uri in u[ank].keys():
#                 print(u[ank].keys())
#                 print(u[ank][uri])