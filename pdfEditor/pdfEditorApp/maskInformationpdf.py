# imports
import datetime

import PyPDF2
import fitz
import re


class Redactor:
    @staticmethod
    def get_sensitive_data(lines):

        """ Function to get all the lines """

        # email regex
        EMAIL_REG = r"([\w\.\d]+\@[\w\d]+\.[\w\d]+)"
        for line in lines:

            # matching the regex to each line
            if re.search(EMAIL_REG, line, re.IGNORECASE):
                search = re.search(EMAIL_REG, line, re.IGNORECASE)
                yield search.group(1)

    # constructor
    def __init__(self, path):
        self.path = path

    def email_redaction(self):

        """ main redactor code """
        print("heloo ")

        # opening the pdf
        doc = fitz.open(self.path)

        for page in doc:

            page.wrap_contents()

            sensitive = self.get_sensitive_data(page.get_text("text")
                                                .split('\n'))
            for data in sensitive:
                areas = page.search_for(data)

                # drawing outline over sensitive datas
                [page.add_redact_annot(area, fill=(0, 0, 0)) for area in areas]

            # applying the redaction
            page.apply_redactions()
        current_datetime = datetime.datetime.now()
        myFile = f"Fileredacted_{current_datetime.strftime('%Y-%m-%d_%H%M%S')}.pdf"
        doc.save(myFile)
        print("Successfully redacted")
        return myFile

    def redact_pdf(self, output_path, redaction_areas):
        pdf = fitz.open(self.path)

        # Iterate through each page of the PDF
        for page_num in range(pdf.page_count):
            page = pdf[page_num]
            for area in redaction_areas:
                x, y, width, height = area
                redaction_rect = fitz.Rect(x, y, x + width, y + height)
                page.add_redact_annot(redaction_rect, fill=(1, 1, 1))
            page.apply_redactions()
        pdf.save(output_path)
        pdf.close()


# if __name__ == "__main__":
#     # replace it with name of the pdf file
#     path = '../PDF_pool/mail_example.pdf'
#     redactor = Redactor(path)
#     redactor.email_redaction()
#     path = '../PDF_pool/chapitre2.pdf'
#     out = '../PDF_pool/pdf_Redacted.pdf'
#     redaction_areas = [(100, 200, 50, 50)]
#     redactor = Redactor(path)
#     redactor.redact_pdf(out, redaction_areas)