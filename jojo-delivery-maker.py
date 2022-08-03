from fpdf import FPDF 
from PIL import Image
from datetime import datetime
from sys import argv

from utils.get_all_files import get_all_files
from utils.zip_files import zip_files

argumentList = argv[1:]
FOLDER_TO_SEARCH_CODE = argumentList[0]
SIGNATURE_PATH = argumentList[1]

STUDENT_NAME = "Renato Cesar Ferreira Barcellos"
LIST_NAME = "Entrega 2"
HEADER_NAME = f"Linguagem de Programação II - {LIST_NAME} - {STUDENT_NAME}"
HEIGHT = 7
WIDTH = 40
ALIGN = "P"


class PdfMaker(FPDF):
    def open_image(self, path: str):
        return Image.open(path)
    
    def add_image(self, path: str, resize_factor: float = 1):
        img = self.open_image(path)
        self.new_line()
        self.image(path, 
                   w=img.width * resize_factor, 
                   h=img.height * resize_factor,
                   type = 'PNG', link = '')
        
    def create_footer(self):
        self.set_font('Arial', 'B', 13)
        e = datetime.now()
        date = "%s / %s / %s" % (e.day, e.month, e.year)
        self.cell(40,20, f"Dourados, {date}")
        self.add_image(SIGNATURE_PATH, 0.1)
        
    def create_header(self, text):
        self.set_font('Arial', 'B', 14)
        self.ln(3)
        self.set_fill_color(255, 255, 255)
        self.cell(0, 10, text, 0, 1, 'C', 1)
        self.ln(7)
        
    def new_line(self):
        self.cell(WIDTH, HEIGHT, f"", align=ALIGN, ln=True)

class SaidaPDF(PdfMaker):
    def add_print(self, path):
        img = self.open_image(path)
        self.image(f"./{path}", w=img.width/10, h=img.height/10)
        self.new_line()
        
    @staticmethod
    def build():
        saida = SaidaPDF(orientation=ALIGN, unit='mm', format='A4')
        saida.alias_nb_pages()
        saida.add_page()
        saida.create_header(HEADER_NAME)
        saida.new_line()  

        for file in get_all_files('./prints', ['png']):
            print(file)
            saida.add_print(file)
            
        saida.new_line()
        saida.create_footer()
        saida.output("./saida.pdf")

class FontesPDF(PdfMaker):
    def create_file_block(self, file_path: str):
        title = file_path.split('/')[-1]
        self.create_title(title)
        self.add_lines_from_file(file_path)
               
    def create_title(self, label):
        self.set_font('Arial', 'B', 15)
        self.ln(5)
        self.set_fill_color(255, 255, 255)
        self.cell(0, 10, label, 0, 1, 'L', 1)
        self.ln(3)
       
    def add_lines_from_file(self, file_path):
        file = open(file_path, 'r')
        self.set_font('Arial', '', 12)
        lines = file.readlines()
        distance_btw_lines = 6.5
        for line in lines:
            pdf_line = line.strip('\n')
            self.cell(0, distance_btw_lines, pdf_line, 0, 0.5)
 
    @staticmethod
    def build(file_name: str, file_type: str = 'java'):               
        fontes = FontesPDF(orientation=ALIGN, unit='mm', format='A4')
        fontes.alias_nb_pages()
        fontes.add_page()
        fontes.create_header(HEADER_NAME)

        directory = FOLDER_TO_SEARCH_CODE
        file_types = [file_type]

        paths = get_all_files(directory, file_types)
        for file in paths:
            print(file)
            fontes.create_file_block(str(file))
            
        fontes.create_footer()
        fontes.output(file_name, 'F')

SaidaPDF.build()
FontesPDF.build('./src.pdf', 'java')
FontesPDF.build('./sql.pdf', 'sql')

files = ['./src.pdf',
        './sql.pdf',
        './saida.pdf',
        './src']

zip_files(f"LPII - {LIST_NAME} - {STUDENT_NAME}.zip", files)
