# from transformers import AutoTokenizer, AutoModel
#
# # 加载预训练模型和分词器
# model_name = 'bert-base-chinese'
# tokenizer = AutoTokenizer.from_pretrained(model_name)
# model = AutoModel.from_pretrained(model_name)
#
# # 输入文本
# text = "我爱北京天安门"
#
# # 将文本转化为模型输入格式
# inputs = tokenizer(text, return_tensors='pt')
#
# # 获取模型输出
# outputs = model(**inputs)
#
# # 获取句子向量
# sentence_embedding = outputs[1].detach().numpy()
#
# print(sentence_embedding)
from langchain.document_loaders import UnstructuredPDFLoader

loader = UnstructuredPDFLoader("pdf/机器学习.pdf", mode="elements")
data = loader.load()
import re

# 假设原始字符串为一个名为 s 的字符串
start_val = '3'  # 起始位置的值
end_val = '7'  # 结束位置的值

start_match = re.search(start_val, s)  # 查找起始位置的匹配
end_match = re.search(end_val, s)  # 查找结束位置的匹配
start = start_match.start()  # 获取起始位置的索引
end = end_match.start()  # 获取结束位置的索引
substring = s[start:end]  # 截取子字符串
print(data)