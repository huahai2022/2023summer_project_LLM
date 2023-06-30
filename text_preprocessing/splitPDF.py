
#实现对PDF的按照页分割
import PyPDF2

input_file = "D:\learn\project\llm\\text_preprocessing\\13_16.pdf"
output_file = "16.pdf"
start_page = 429

# 打开PDF文件
with open(input_file, "rb") as f:
    pdf_reader = PyPDF2.PdfReader(f)

    # 获取PDF文件总页数
    total_pages = len(pdf_reader.pages)

    # 创建一个新的PDF写入对象
    pdf_writer = PyPDF2.PdfWriter()

    # 将指定页码后面的所有页添加到新的PDF写入对象中
    for page in range(start_page, total_pages):
        current_page = pdf_reader.pages[page]
        pdf_writer.add_page(current_page)

    # 将新的PDF写入对象保存为PDF文件
    with open(output_file, "wb") as f:
        pdf_writer.write(f)