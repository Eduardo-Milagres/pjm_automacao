import os
from docx import Document

class docManager:
    def merger(self, path):
        merged = Document()

        docs_list = []

        docs = os.listdir(path)
        for doc in docs:
            docs_list.append(os.path.join(path, doc))

        for doc in docs_list:  
            doc_file = Document(doc)

            for element in doc_file.element.body:
                merged.element.body.append(element)

        merged.save(f'{path}/Merged_doc.docx')
