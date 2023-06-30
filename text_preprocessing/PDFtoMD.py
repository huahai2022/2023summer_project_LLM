import fitz
import os
import re
import base64

# 创建保存图片的目录
if not os.path.exists('images'):
    os.makedirs('images')

# 遍历每个 PDF 文件，提取文本和图片
text_list = []
for pdf_file in os.listdir('D:\learn\project\llm\\Data'):
    if not pdf_file.endswith('.pdf'):
        continue

    # 打开 PDF 文件，获取文档对象
    doc = fitz.open(os.path.join('D:\learn\project\llm\\Data', 'MTDS.pdf'))

    # 遍历每一页，获取页面对象
    for i in range(doc.page_count):
        page = doc.load_page(i)

        # 获取页面中的图片对象，并保存为 PNG 文件
        for img in page.get_images():
            pix = fitz.Pixmap(doc, img[0])
            if pix.n < 5:
                pix._writeIMG(f'images/{pdf_file}_page{i+1}_image{img[1]}.png',format=3)

        # 获取页面中的文本内容，并保存到列表中
        text = page.get_text("text")
        text_list.append(text)

# 将提取出的文本和图片转换为 Markdown 格式
with open('output.md', 'w', encoding='utf-8') as f:
    for i, text in enumerate(text_list):
        # 将文本内容转换为 Markdown 格式
        markdown_text = ''
        for line in text.split('\n'):
            # 处理标题
            if re.match(r'^\s*[A-Z]+\s*$', line):
                markdown_text += f'# {line.strip()}\n'
            # 处理段落
            elif line.strip():
                markdown_text += f'{line.strip()}\n'
            # 处理空行
            else:
                markdown_text += '\n'

        # 将页面中的图片插入到 Markdown 文本中
        for img_file in os.listdir('images'):
            if img_file.startswith(f'{pdf_file}_page{i+1}_image'):
                markdown_text += f'![{img_file}](./images/{img_file})\n'

        f.write(markdown_text)