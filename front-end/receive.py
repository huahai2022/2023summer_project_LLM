import sys
sys.path.append("C:\\Users\\LENOVO\\AppData\\Local\\Packages\\PythonSoftwareFoundation.Python.3.11_qbz5n2kfra8p0\\LocalCache\\local-packages\\Python311\\site-packages")
from flask import Flask, request, jsonify
from flask_cors import CORS
import logging

#需要本地安装flask

#Flask实现本地服务器部署
app = Flask(__name__)

#CORS实现跨域请求
CORS(app)

#终端显示
app.logger.setLevel(logging.INFO) 

#路由挂载
@app.route('/receive.py', methods=['GET','POST'])
def process_text():
    data = request.json
    input_text = data['text']

    #……input_text的使用和response_text的获得……

    response_text = '你好！请问有什么可以帮助你的？'
    return jsonify({'text': response_text})

#服务器（浏览器）占位用URL
@app.route('/', methods=['GET'])
def index():
    return "Waiting"

#定义一致端口运行
if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000)