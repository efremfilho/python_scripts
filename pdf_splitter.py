!pip install PyPDF2==2.12.1

import os
from PyPDF2 import PdfReader, PdfWriter

def split_file(filename, num_parts=10): #number of parts
  """Divide um PDF em várias partes, cada uma sendo um PDF válido.

  Args:
    filename: O nome do arquivo PDF a ser dividido.
    num_parts: O número de partes para dividir o arquivo.
  """
  # Get extension of the file
  base_filename = os.path.splitext(filename)[0]  
  
  # Oepn original PDF
  with open(filename, 'rb') as f:
    reader = PdfReader(f)
    total_pages = len(reader.pages)
    pages_per_part = total_pages // num_parts

    for i in range(num_parts):
      # new pdf for each part
      writer = PdfWriter()
      
      # add pages to the parts
      start_page = i * pages_per_part
      end_page = min((i + 1) * pages_per_part, total_pages) 
      for page_num in range(start_page, end_page):
        writer.add_page(reader.pages[page_num])

      # save the part as a pdf
      chunk_filename = f'{base_filename}.part{i+1}.pdf'
      with open(chunk_filename, 'wb') as chunk_f:
        writer.write(chunk_f)

split_file('/content/FILENAME.pdf')
