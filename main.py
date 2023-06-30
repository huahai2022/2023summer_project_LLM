import os.path
from langchain.document_loaders import TextLoader, CSVLoader, UnstructuredFileLoader, UnstructuredPDFLoader
import re
from typing import List
from langchain.text_splitter import CharacterTextSplitter
import PyPDF2
from langchain.embeddings.huggingface import HuggingFaceInstructEmbeddings,HuggingFaceEmbeddings
from langchain.vectorstores import VectorStore

from DB import MyLocalDB
from args import parser
from config import SENTENCE_SIZE
from model import load_model
from models.loader import LoadCheckpoint

# import MyFAISS
# import model
# from args import parser
sentence_size=SENTENCE_SIZE
 #最大句子长度是20
# `SENTENCE_SIZE` 的大小应该根据具体应用场景和需求进行调整。一般而言，句子的长度应该控制在一定范围内，以便于阅读和理解。在中文文本中，句子长度一般在 10 到 30 个字之间比较合适，但是也会有一些较长的句子。
#
# 在设置 `SENTENCE_SIZE` 的值时，需要考虑到文本的类型、领域和语言习惯等因素。如果文本是新闻报道、科技文章等主题较为专业的文本，句子的长度可能会更长；如果文本是小说、散文等文学作品，句子的长度可能会更短。
#
# 另外，也可以根据实际的处理效果进行调整。如果句子长度设置过短，则会导致过多的分句，增加处理的时间和复杂度；如果句子长度设置过长，则会导致分句不准确，影响后续的处理和分析。
#
# 综上所述，`SENTENCE_SIZE` 的大小应该根据具体的应用场景和需求进行调整，一般建议将句子长度控制在 10 到 30 个字之间。在实际使用中，可以根据处理效果进行适当的调整，以达到更好的分句效果。



#定义一个类，用来处理，中文的语义分割



def main():

    model=load_model(loaderCheckpoint=loaderCheckpoint)
    print("模型加载完毕~")
    #创建本地知识库，使用向量库管理
    localDB= MyLocalDB()
    filepath = input("请输入你的本地文件路径：")
    while not filepath or not os.path.exists(filepath):
        print("你没有输入或者你输入了一个不存在的路径~搞笑男，真下头")
        filepath = input("请重新输入你的本地文件路径：")
    #集成到向量库那个文件
    db_path,_= localDB.init_vector_stroe(filepath,db_path=args.vs_path)
    history=[]
    while True:
        query=input("请输入你的问题:")
        last_print_len = 0
        for response,history in localDB.get_answer_based_query()

if __name__ == "__main__":
    args=None
    args=parser.parse_args() #获取参数
    args_dict=vars(args)
    print(args_dict)
    loaderCheckpoint=LoadCheckpoint(args_dict)
    main()