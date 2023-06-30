import os

LOAD_IN_8BIT = False
LLM_DEVICE = "cuda"
LLM_MODEL = "chatglm-6b"
LLM_HISTORY_LEN=10
VECTOR_SEARCH_TOP_K=5
CHUNK_SIZE=250   #匹配单段上下文的长度
VECTOR_SEARCH_SCORE_THRESHOLD=0  #数据库的匹配相似度，为0不生效，这个值不确定
SENTENCE_SIZE=20
STREAME=True
ROOT_PATH=os.path.join(os.path.dirname(os.path.dirname(__file__)), "knowledge_base")
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
