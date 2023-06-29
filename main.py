import os.path
from langchain.document_loaders import TextLoader, CSVLoader, UnstructuredFileLoader, UnstructuredPDFLoader
import re
from typing import List
from langchain.text_splitter import CharacterTextSplitter
import PyPDF2
from langchain.embeddings.huggingface import HuggingFaceInstructEmbeddings,HuggingFaceEmbeddings
from langchain.vectorstores import VectorStore

from args import parser
from model import load_model
from models.loader import LoadCheckpoint

# import MyFAISS
# import model
# from args import parser

SENTENCE_SIZE=20   #最大句子长度是20
# `SENTENCE_SIZE` 的大小应该根据具体应用场景和需求进行调整。一般而言，句子的长度应该控制在一定范围内，以便于阅读和理解。在中文文本中，句子长度一般在 10 到 30 个字之间比较合适，但是也会有一些较长的句子。
#
# 在设置 `SENTENCE_SIZE` 的值时，需要考虑到文本的类型、领域和语言习惯等因素。如果文本是新闻报道、科技文章等主题较为专业的文本，句子的长度可能会更长；如果文本是小说、散文等文学作品，句子的长度可能会更短。
#
# 另外，也可以根据实际的处理效果进行调整。如果句子长度设置过短，则会导致过多的分句，增加处理的时间和复杂度；如果句子长度设置过长，则会导致分句不准确，影响后续的处理和分析。
#
# 综上所述，`SENTENCE_SIZE` 的大小应该根据具体的应用场景和需求进行调整，一般建议将句子长度控制在 10 到 30 个字之间。在实际使用中，可以根据处理效果进行适当的调整，以达到更好的分句效果。



#定义一个类，用来处理，中文的语义分割
class ChineseTextSplitter(CharacterTextSplitter):
    def __init__(self, pdf: bool = False, sentence_size: int = SENTENCE_SIZE,**kwargs):
        super().__init__(**kwargs)
        self.pdf = pdf
        self.sentence_size = sentence_size

    def split_text(self, text: str) -> List[str]:
        # 如果需要对 PDF 文件进行处理
        if self.pdf:
            text = re.sub(r"\n{3,}", r"\n", text)   #出现三个或者三个以上换行符，将他们替换成一个换行符
            text = re.sub(r'\s', " ", text)         #匹配任意空白字符，包括空格，制表符，换行符，替换成一个空格
            text = re.sub(r"\n\n", "", text)        #连续出现两个换行符，替换成一个空字符串
        # 定义分句规则
        sent_sep_pattern = re.compile(r'[。！？…]+|[^\s。！？…]+')
        # 对文本进行分句
        sentences = []
        for sentence in sent_sep_pattern.findall(text):
            # 如果句子长度超过阈值，则进一步分句
            while len(sentence) > self.sentence_size:
                sub_sentence = sentence[:self.sentence_size]
                # 在子句结尾处查找分句符号
                last_sep = re.search(r'[。！？…]', sub_sentence[::-1])
                if last_sep:
                    sub_sentence = sub_sentence[:-last_sep.end()]
                sentences.append(sub_sentence)
                sentence = sentence[len(sub_sentence):]
            sentences.append(sentence)

        return sentences
class ChineseTextSplitter2(CharacterTextSplitter):
    def __init__(self, pdf: bool = False, sentence_size: int = SENTENCE_SIZE,  **kwargs):
        super().__init__(**kwargs)
        self.pdf = pdf
        self.sentence_size = sentence_size

    def split_text1(self, text: str) -> List[str]:
        if self.pdf:
            text = re.sub(r"\n{3,}", "\n", text)
            text = re.sub('\s', ' ', text)
            text = text.replace("\n\n", "")
        sent_sep_pattern = re.compile('([﹒﹔﹖﹗．。！？]["’”」』]{0,2}|(?=["‘“「『]{1,2}|$))')  # del ：；
        sent_list = []
        for ele in sent_sep_pattern.split(text):
            if sent_sep_pattern.match(ele) and sent_list:
                sent_list[-1] += ele
            elif ele:
                sent_list.append(ele)
        return sent_list

    def split_text(self, text: str) -> List[str]:   ##此处需要进一步优化逻辑
        if self.pdf:
            text = re.sub(r"\n{3,}", r"\n", text)
            text = re.sub('\s', " ", text)
            text = re.sub("\n\n", "", text)
        print(text)
        text = re.sub(r'([;；.!?。！？\?])([^”’])', r"\1\n\2", text)  # 单字符断句符
        text = re.sub(r'(\.{6})([^"’”」』])', r"\1\n\2", text)  # 英文省略号
        text = re.sub(r'(\…{2})([^"’”」』])', r"\1\n\2", text)  # 中文省略号
        text = re.sub(r'([;；!?。！？\?]["’”」』]{0,2})([^;；!?，。！？\?])', r'\1\n\2', text)
        # 如果双引号前有终止符，那么双引号才是句子的终点，把分句符\n放到双引号后，注意前面的几句都小心保留了双引号
        text = text.rstrip()  # 段尾如果有多余的\n就去掉它
        # 很多规则中会考虑分号;，但是这里我把它忽略不计，破折号、英文双引号等同样忽略，需要的再做些简单调整即可。
        ls = [i for i in text.split("\n") if i]
        for ele in ls:
            if len(ele) > self.sentence_size:
                ele1 = re.sub(r'([,，.]["’”」』]{0,2})([^,，.])', r'\1\n\2', ele)
                ele1_ls = ele1.split("\n")
                for ele_ele1 in ele1_ls:
                    if len(ele_ele1) > self.sentence_size:
                        ele_ele2 = re.sub(r'([\n]{1,}| {2,}["’”」』]{0,2})([^\s])', r'\1\n\2', ele_ele1)
                        ele2_ls = ele_ele2.split("\n")
                        for ele_ele2 in ele2_ls:
                            if len(ele_ele2) > self.sentence_size:
                                ele_ele3 = re.sub('( ["’”」』]{0,2})([^ ])', r'\1\n\2', ele_ele2)
                                ele2_id = ele2_ls.index(ele_ele2)
                                ele2_ls = ele2_ls[:ele2_id] + [i for i in ele_ele3.split("\n") if i] + ele2_ls[
                                                                                                       ele2_id + 1:]
                        ele_id = ele1_ls.index(ele_ele1)
                        ele1_ls = ele1_ls[:ele_id] + [i for i in ele2_ls if i] + ele1_ls[ele_id + 1:]

                id = ls.index(ele)
                ls = ls[:id] + [i for i in ele1_ls if i] + ls[id + 1:]
        return ls
class ChineseTextSplitter3(CharacterTextSplitter):
    def __init__(self, pdf: bool = False, sentence_size: int = SENTENCE_SIZE,  **kwargs):
        super().__init__(**kwargs)
        self.pdf = pdf
        self.sentence_size = sentence_size

    def split_text(self, text: str) -> List[str]:   ##此处需要进一步优化逻辑
        text = re.sub(r"\n{3,}","", text)
        text = re.sub('\s', "", text)
        text = re.sub("\n\n", "", text)
        # 如果双引号前有终止符，那么双引号才是句子的终点，把分句符\n放到双引号后，注意前面的几句都小心保留了双引号
        text = text.rstrip()  # 段尾如果有多余的\n就去掉它
        sentences=[]
        for i in range(100):
            start_val=str(i+1)
            end_val=str(i+2)
            start_index=re.search(start_val,text).start()
            end_index=re.search(end_val,text).start()
            substring=text[start_index:end_index]
            print(substring)
            sentences.append(substring)
        return sentences

def find_files(filepath):
    file_paths = []  # 用于存储文件路径的列表
    for root, directories, files in os.walk(filepath):
        #root:当前目录路径
        #directories:当前目录名称
        #files:文件名称
        for filename in files:
            # 将文件的完整路径添加到列表中
            filepath = os.path.join(root, filename)
            file_paths.append(filepath)
    return file_paths

def show_docx1(docxs):
    for doc in docxs:
        print(doc)
def show_docx2(docxs):
    docx=""
    for doc in docxs:
        docx+=doc
    docx=docx.replace('\n','')
    print(docx)


def extract_text_from_pdf(filepath):
    """
    提取 PDF 文件中的文本内容
    """
    with open(filepath, 'rb') as f:
        # 创建 PDF 文件读取器
        reader = PyPDF2.PdfReader(f)
        # 获取 PDF 文件中的页数
        num_pages = len(reader.pages)
        # 遍历每一页，提取文本内容
        text = ''
        for i in range(num_pages):
            page = reader.pages[i]
            text += page.extract_text()
    return text

#用来处理大文件
def load_file(filepath,sentence_size=SENTENCE_SIZE):
    if filepath.lower().endswith(".md"):
        loader=UnstructuredFileLoader(filepath,mode="elements")
        # UnstructuredFileLoader类的mode参数定义了在加载文件时如何解析文本内容，具体的mode参数取值及其含义如下：
        # - `"text"`：将整个文本文件加载为一个字符串对象。
        # - `"lines"`：将文本文件按行加载为一个字符串列表，每个字符串代表一行文本。
        # - `"elements"`：将文本文件加载为一个元素对象列表，每个元素代表一个Markdown元素（如段落、标题、列表、代码块等）。
        # - `"json"`：将JSON格式的文本文件加载为一个Python对象。
        # - `"pickle"`：将pickle序列化格式的文本文件加载为一个Python对象。
        # 其中，前三种mode参数适用于Markdown格式的文本文件，后两种mode参数适用于其他格式的文本文件。在使用时，需要根据不同的文本文件类型和数据格式选择合适的mode参数。
        docs=loader.load()
    elif filepath.lower().endswith(".txt"):
        loader=TextLoader(filepath,autodetect_encoding=True)
        txtSplitter=ChineseTextSplitter2(pdf=False)    #定义中文分割规则
        docs=loader.load_and_split(txtSplitter)        #按照中文分割规则进行划分
    # elif filepath.lower().endswith(".pdf"):            #效果一般
    #     docs=extract_text_from_pdf(filepath)
    #     pdfSplitter=ChineseTextSplitter2(pdf=True)
    #     docs=pdfSplitter.split_text(docs)
    elif filepath.lower().endswith(".pdf"):
        loader=UnstructuredPDFLoader(file_path=filepath)
        pdfSplitter=ChineseTextSplitter3(pdf=True)
        docs=loader.load_and_split(pdfSplitter)
    elif filepath.lower().endswith(".csv"):
        loader = CSVLoader(filepath)
        docs = loader.load()
    else:
        loader = UnstructuredFileLoader(filepath, mode="elements")
        textsplitter = ChineseTextSplitter(pdf=False, sentence_size=sentence_size)
        docs = loader.load_and_split(text_splitter=textsplitter)
    return docs
def main():




    loaded_files=[]     #定义知识数据库
    vectors=None
    filepath=input("请输入你的本地文件路径：")
    while not filepath or not os.path.exists(filepath):
        print("你没有输入或者你输入了一个不存在的路径~搞笑男，真下头")
        filepath =input("请重新输入你的本地文件路径：")
    if os.path.isfile(filepath):
        file=os.path.split(filepath)[-1]   #取文件名
        try:
            loaded_files=load_file(filepath,sentence_size=SENTENCE_SIZE)
            print(f"{file}已经成功加载")
        except Exception as e:
            print(e)

    elif os.path.isdir(filepath):
        files=find_files(filepath)
        for file in files:
            try:
                loaded_files +=load_file(file)
            except Exception as e:
                print(e)

    show_docx1(loaded_files)
    print("文件加载完成，生成知识库中~~~")
    # print(loaded_files.__len__())   #查看生成的文本的数量
    # print(vectors)#查看向量库的属性都有哪些
    # ['__bool__', '__class__', '__delattr__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__',
    #  '__gt__', '__hash__', '__init__', '__init_subclass__', '__le__', '__lt__', '__ne__', '__new__', '__reduce__',
    #  '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__']
    model=load_model(loaderCheckpoint=loaderCheckpoint)
if __name__ == "__main__":
    args=None
    args=parser.parse_args() #获取参数
    args_dict=vars(args)
    print(args_dict)
    loaderCheckpoint=LoadCheckpoint(args_dict)
    main()