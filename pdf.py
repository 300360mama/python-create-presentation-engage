from PyPDF2 import PdfFileReader

path = "C:\\Users\\олександр\\Desktop\\sdfsa\\ICP_DYS_iPad_Folder_DE_interaktiv.pdf"

with open(path, "rb") as filehandle:
    pdf = PdfFileReader(filehandle)
    info = pdf.getFields()
    print(info)


