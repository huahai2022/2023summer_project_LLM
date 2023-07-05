#####################
import sys
sys.path.append("C:\\Users\\LENOVO\\AppData\\Local\\Packages\\PythonSoftwareFoundation.Python.3.11_qbz5n2kfra8p0\\LocalCache\\local-packages\\Python311\\site-packages")
#系统环境变量，需修改或删除!
#####################

from flask import Flask, request, jsonify
import re
from flask_cors import CORS
import os

#####################
#需要本地安装flask
#####################

#Flask实现本地服务器部署
app = Flask(__name__)
CORS(app)

# 定义读取Markdown文件的函数
def read_markdown_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read()
    # 使用正则表达式提取图片链接
    image_pattern = r'!\[.*?\]\((.*?)\)'
    image_sentences = re.findall(image_pattern, text)
    return text,image_sentences

#路由挂载
@app.route('/receive.py', methods=['GET','POST'])
def process_text():
    data = request.json
    input_text = data['text']

    #此处实现前后端连接，完成input_text的使用和response_text的获得

    #####################
    response_text = '你好！请问有什么可以帮助你的？'
    #记得改变response_text变量！
    #####################

    # 读取Markdown文件内容
    #####################
    markdown_file_path_array = [
        'C:\\Users\\LENOVO\\Desktop\\Project\\Chapter9_1_1.md',
        'C:\\Users\\LENOVO\\Desktop\\Project\\Chapter9_1_3.md',
    ]
    #记得改变.md路径！
    #####################  
    
    #封装数据并送往前端
    markdown_contents = []
    for markdown_file_path in markdown_file_path_array:
        file_name = os.path.basename(markdown_file_path)
        markdown_text, markdown_images = read_markdown_file(markdown_file_path)
        markdown_content = {'file_name': file_name, 'markdown_text': markdown_text, 'markdown_images': markdown_images}
        markdown_contents.append(markdown_content)

    markdown_response = {'text': response_text, 'markdown_contents': markdown_contents}

    return jsonify(markdown_response)

#服务器（浏览器）占位用URL
@app.route('/', methods=['GET'])
def index(): 
    return "Waiting"

#定义一致端口运行
if __name__ == '__main__':
    #####################
    app.run(host='127.0.0.1', port=5000)
    #确保该端口不被占用！
    #####################