import logging
import os
KNOWLEDGE_BASE_INFO=(
	"你已经进入知识库模式,可以使用我们目前已经现有的知识库，也可以新建知识库"
)
WEB_TITLE="""
#🎉🤟🎈这里是基于langchain实现的智能客服机器人，我的默认模型是ChatGLM-6B
"""
LOAD_IN_8BIT = False
LLM_DEVICE = "cuda"
LLM_MODEL = "chatglm-6b"
LLM_HISTORY_LEN=1
VECTOR_SEARCH_TOP_K=2
CHUNK_SIZE=200   #匹配单段上下文的长度
VECTOR_SEARCH_SCORE_THRESHOLD=0  #数据库的匹配相似度，为0不生效，这个值不确定
SENTENCE_SIZE=20
STREAME=False
ROOT_PATH=os.path.join(os.path.dirname(os.path.dirname(__file__)), "knowledge_base")
REPLY_WITH_SOURCE_SOCRE=True
REPLY_WITH_SCORE=False
LOG_FORMAT = "%(levelname) -5s %(asctime)s" "-1d: %(message)s"
logger=logging.getLogger()
logger.setLevel(logging.INFO)
logging.basicConfig(format=LOG_FORMAT)
PROMPT_TEMPLATE="""已知信息：{context}
根据上述已知信息，简洁且专业地回答用户地问题。如果问题不清晰或无法从已知信息中得到答案，请回复"根据已知信息无法回答该问题，请提供足够的本地知识库信息"，切勿在答案中胡编乱造，切勿回答已知信息以外的问题，问题不明确的时，请回答问题不明确，答案请使用中文。问题是：{question}"""
# PROMPT_TEMPLATE="""已知问题：{question}请先判断该问题是不是问题，如果不是，请说”请明确你的问题“。如果是，根据以下已知信息，简洁且专业地回复用户信息，如果无法从已知信息中得到答案，请回复请提供足够的知识，切勿在答案中胡编乱造，切勿在答案中回复与已知信息无关的内容，已知信息是{context}"""
ACCESS_HUGGING_TOKEN="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"
llm_model_dict = {
	"chatglm-6b-int4-qe": {
		"name": "chatglm-6b-int4-qe",
		"pretrained_model_name": "THUDM/chatglm-6b-int4-qe",
		"local_model_path": None,
		"provides": "ChatGLM"
	},
	"chatglm-6b-int4": {
		"name": "chatglm-6b-int4",
		"pretrained_model_name": "THUDM/chatglm-6b-int4",
		"local_model_path": None,
		"provides": "ChatGLM"
	},
	"chatglm-6b-int8": {
		"name": "chatglm-6b-int8",
		"pretrained_model_name": "THUDM/chatglm-6b-int8",
		"local_model_path": None,
		"provides": "ChatGLM"
	},
	"chatglm-6b": {
		"name": "chatglm-6b",
		"pretrained_model_name": "THUDM/chatglm-6b",
		"local_model_path": None,
		"provides": "ChatGLM"
	},

	"chatyuan": {
		"name": "chatyuan",
		"pretrained_model_name": "ClueAI/ChatYuan-large-v2",
		"local_model_path": None,
		"provides": None
	},
	"moss": {
		"name": "moss",
		"pretrained_model_name": "fnlp/moss-moon-003-sft",
		"local_model_path": None,
		"provides": "MOSSLLM"
	},
	"vicuna-13b-hf": {
		"name": "vicuna-13b-hf",
		"pretrained_model_name": "vicuna-13b-hf",
		"local_model_path": None,
		"provides": "LLamaLLM"
	},

	# 通过 fastchat 调用的模型请参考如下格式
	"fastchat-chatglm-6b": {
		"name": "chatglm-6b",  # "name"修改为fastchat服务中的"model_name"
		"pretrained_model_name": "chatglm-6b",
		"local_model_path": None,
		"provides": "FastChatOpenAILLM",  # 使用fastchat api时，需保证"provides"为"FastChatOpenAILLM"
		"api_base_url": "http://localhost:8000/v1"  # "name"修改为fastchat服务中的"api_base_url"
	},

	# 通过 fastchat 调用的模型请参考如下格式
	"fastchat-vicuna-13b-hf": {
		"name": "vicuna-13b-hf",  # "name"修改为fastchat服务中的"model_name"
		"pretrained_model_name": "vicuna-13b-hf",
		"local_model_path": None,
		"provides": "FastChatOpenAILLM",  # 使用fastchat api时，需保证"provides"为"FastChatOpenAILLM"
		"api_base_url": "http://localhost:8000/v1"  # "name"修改为fastchat服务中的"api_base_url"
	},
}


# 在以下字典中修改属性值，以指定本地embedding模型存储位置
# 如将 "text2vec": "GanymedeNil/text2vec-large-chinese" 修改为 "text2vec": "User/Downloads/text2vec-large-chinese"
# 此处请写绝对路径
embedding_model_dict = {
    "ernie-tiny": "nghuyong/ernie-3.0-nano-zh",
    "ernie-base": "nghuyong/ernie-3.0-base-zh",
    "text2vec-base": "shibing624/text2vec-base-chinese",
    "text2vec": "GanymedeNil/text2vec-large-chinese",
    "m3e-small": "moka-ai/m3e-small",
    "m3e-base": "moka-ai/m3e-base",
}
