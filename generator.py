from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Image
import os
from PIL import Image as PILImage
from io import BytesIO

def convert_image(file_path, max_width=400):
    img = PILImage.open(file_path)
    img = img.convert("RGB")

    width_percent = (max_width / float(img.size[0]))
    new_height = int((float(img.size[1]) * float(width_percent)))
    img = img.resize((max_width, new_height), PILImage.LANCZOS)

    img_stream = BytesIO()
    img.save(img_stream, format='JPEG')
    img_stream.seek(0)
    return img_stream, new_height


def generate_pdf_from_image(file_name, output_pdf):
    doc = SimpleDocTemplate(output_pdf, pagesize=letter)
    elements = []

    img_stream, img_height = convert_image(file_name)
    img = Image(img_stream)

    max_page_width, max_page_height = letter
    img_width, img_height = img.wrap(max_page_width, max_page_height)

    img.width = img_width
    img.height = img_height

    elements.append(img)
    doc.build(elements)


def generate_pdf(input_file, output_pdf):
    _, ext = os.path.splitext(input_file)
    ext = ext.lower()

    # if ext == '.txt':
    #     generate_pdf_from_text(input_file, output_pdf)
    # elif ext == '.csv':
    #     generate_pdf_from_csv(input_file, output_pdf)
    # elif ext in ['.xlsx', '.xls']:
    #     generate_pdf_from_excel(input_file, output_pdf)
    # elif ext == '.html':
    #     generate_pdf_from_html(input_file, output_pdf)
    if ext in ['.jpg', '.jpeg', '.png']:
        generate_pdf_from_image(input_file, output_pdf)
    else:
        raise ValueError("Unsupported file type")


if __name__ == '__main__':
    generate_pdf('./docs/To-do list - To do.csv',
                 './pdfs/To-do fron csv list.pdf')
