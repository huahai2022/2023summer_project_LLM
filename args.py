import argparse

from config import LOAD_IN_8BIT, LLM_MODEL

parser=argparse.ArgumentParser(prog="llm",usage="提供文档生成本地知识库，用户提问进行对答",description="基于langchain的本地问答系统",)
parser.add_argument("--model_name",type=str,default=LLM_MODEL)
parser.add_argument("--load_in_8bit",action="store_true",default=LOAD_IN_8BIT)
args=parser.parse_args()     #获取从控制台传入的参数
USING_ARGS=vars(args)    #将使用的参数转变成全局变量，方便使用