import os.path
# from langchain.document_loaders import TextLoader, CSVLoader, UnstructuredFileLoader, UnstructuredPDFLoader
# import re
# from typing import List
# from langchain.text_splitter import CharacterTextSplitter
# import PyPDF2
# from langchain.embeddings.huggingface import HuggingFaceInstructEmbeddings,HuggingFaceEmbeddings
# from langchain.vectorstores import VectorStore

from DB import MyLocalDB
from args import parser
from config import SENTENCE_SIZE, STREAME, REPLY_WITH_SOURCE_SOCRE
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

    global db_path
    flag=True
    model=load_model(loaderCheckpoint=loaderCheckpoint)
    print("模型加载完毕~")
    #创建本地知识库，使用向量库管理
    localDB= MyLocalDB(llm_model=model)
    while True:
        print("昔有一仙，名道安，修行百年，得仙道精髓，晓天地玄机。录毕生之学创奇书，曰《天人感应》。载天地万物之变，及修行之道。然，奇书自道安仙人飞升后，陨落凡间，众人忘之。时光荏苒，岁月如梭。历千年，一侠客得此书，勤学之，长修行。为后世通《天人感应》之秘，历千险，经万难，遂创vector_store知识库，录修行，载传说，修道行，以助后人。我们相信，vector_store知识库将成为您修行之路上的重要伙伴，为您提供有用的帮助和指导。\n使用该知识库请输入1\n如果你想要往vector_store里面添加内容，请输入2\n如果你想要创建新的知识库，请输入3\n退出程序请输入4\n")
        print("哎呦~你干嘛~\n")
        option=input("请输入你的选择:")
        try:
            option=int(option)
        except ValueError:
            print("认真点！！！")
            continue
        if (option==1):
            #TODO:使用本地知识库
            db_path=localDB.use_local_vector_stroe()
            break
        elif(option==2):
            # TODO:往本地知识库输入内容
            filepath = input("请输入你本地知识文件路径，感谢你为《天人感应》做出的贡献")
            while not filepath or not os.path.exists(filepath):
                print("你没有输入或者你输入了一个不存在的路径~搞笑男，真下头")
                filepath = input("请重新输入你的本地文件路径：输入exit退出")
                if filepath =="exit":
                    flag=False
                    break
            if flag==False:
                continue
            else:
                db_path=localDB.add_file_to_vector_stroe(filepath,db_name="vector_store")
            break
        elif(option==3):
            #TODO:创建新的知识库,但是这里没有做文件检查
            db_name = input("请输入你新建的知识库名称:")
            filepath = input("请输入你本地知识文件路径")
            db_path=localDB.create_new_vectors(db_name,filepath)
            while True:
                next_option=input("是否继续添加文件，输入1继续，输入2退出")
                try :
                    next_option=int(next_option)
                except ValueError:
                    print("请你认真点")
                    continue
                if next_option==1:
                    filepath=input("请输入你的本地知识文件路径")

                    localDB.add_file_to_vector_stroe(filepath,db_name=db_name)
                elif next_option==2:
                    break
                else:
                    print("输入无效~~")
                    continue
            continue
        elif(option==4):
            return
    history=[]
    while True:
        #这段代码可能存在问题
        query=input("请输入你的问题:")
        last_print_len = 0
        for response,history in localDB.get_answer_based_query(query=query,
                                                               vs_path=db_path,
                                                               chat_history=history,
                                                               stream=STREAME):
            if STREAME:
                print(response['result'][last_print_len:],end="",flush=True)
                last_print_len=len(response["result"])
            else:
                print(response["result"])
        if REPLY_WITH_SOURCE_SOCRE:
            source_text=[f"""来自[{num+1}]\n{doc.metadata["source"]}\t相关度：{doc.metadata["score"]}\n\n{doc.page_content}"""
                         for num,doc in
                         enumerate(response["source_documents"])]
            print("\n\n"+"\n\n".join(source_text))
            # print(response)


if __name__ == "__main__":
    args=None
    args=parser.parse_args() #获取参数
    args_dict=vars(args)
    print(args_dict)
    loaderCheckpoint=LoadCheckpoint(args_dict)
    main()