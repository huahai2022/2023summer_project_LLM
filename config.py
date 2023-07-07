<<<<<<< HEAD
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
VECTOR_SEARCH_TOP_K=3
CHUNK_SIZE=200   #匹配单段上下文的长度
VECTOR_SEARCH_SCORE_THRESHOLD=5  #数据库的匹配相似度，为0不生效，这个值不确定
SENTENCE_SIZE=20
STREAME=True
ROOT_PATH=os.path.join(os.path.dirname(os.path.dirname(__file__)), "knowledge_base")
REPLY_WITH_SOURCE_SOCRE=True
REPLY_WITH_SCORE=False
LOG_FORMAT = "%(levelname) -5s %(asctime)s" "-1d: %(message)s"
logger=logging.getLogger()
logger.setLevel(logging.INFO)
logging.basicConfig(format=LOG_FORMAT)
PROMPT_TEMPLATE="""已知信息：{context}\t\t问题：{question}请注意，回答必须简洁明了、专业准确，仅基于已知信息提供答案。如果问题不明确或无法从已知信息中得到答案，应回复"根据已知信息无法回答该问题，请提供足够的本地知识库信息"。同时，请勿在回答中编造信息或超出已知信息范围回答问题。答案请使用中文。"""
# PROMPT_TEMPLATE="""已知问题：{question}请先判断该问题是不是问题，如果不是，请说”请明确你的问题“。如果是，根据以下已知信息，简洁且专业地回复用户信息，如果无法从已知信息中得到答案，请回复请提供足够的知识，切勿在答案中胡编乱造，切勿在答案中回复与已知信息无关的内容，已知信息是{context}"""
ACCESS_HUGGING_TOKEN="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"
llm_model_dict = {
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

	"moss": {
		"name": "moss",
		"pretrained_model_name": "fnlp/moss-moon-003-sft",
		"local_model_path": None,
		"provides": "MOSSLLM"
	},

}


# 在以下字典中修改属性值，以指定本地embedding模型存储位置
# 如将 "text2vec": "GanymedeNil/text2vec-large-chinese" 修改为 "text2vec": "User/Downloads/text2vec-large-chinese"
# 此处请写绝对路径
embedding_model_dict = {
    "text2vec-base": "shibing624/text2vec-base-chinese",
    "text2vec": "GanymedeNil/text2vec-large-chinese",
}
=======
import os

import torch

# device config
EMBEDDING_DEVICE = "cuda" if torch.cuda.is_available(
) else "mps" if torch.backends.mps.is_available() else "cpu"
LLM_DEVICE = "cuda" if torch.cuda.is_available(
) else "mps" if torch.backends.mps.is_available() else "cpu"
num_gpus = torch.cuda.device_count()

# model cache config
MODEL_CACHE_PATH = os.path.join(os.path.dirname(__file__), 'model_cache')


# vector storage config
VECTOR_STORE_PATH='./vector_store'
COLLECTION_NAME='my_collection'


# init model config
init_llm = "ChatGLM-6B-int8"
init_embedding_model = "text2vec-base"

# model config
embedding_model_dict = {
    "ernie-tiny": "nghuyong/ernie-3.0-nano-zh",
    "ernie-base": "nghuyong/ernie-3.0-base-zh",
    "ernie-medium": "nghuyong/ernie-3.0-medium-zh",
    "ernie-xbase": "nghuyong/ernie-3.0-xbase-zh",
    "text2vec-base": "GanymedeNil/text2vec-base-chinese",
    'simbert-base-chinese': 'WangZeJun/simbert-base-chinese',
    'paraphrase-multilingual-MiniLM-L12-v2': "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
}


llm_model_dict = {
    "chatglm": {
        "ChatGLM-6B": "THUDM/chatglm-6b",
        "ChatGLM-6B-int4": "THUDM/chatglm-6b-int4",
        "ChatGLM-6B-int8": "THUDM/chatglm-6b-int8",
        "ChatGLM-6b-int4-qe": "THUDM/chatglm-6b-int4-qe"
    },
    "belle": {
        "BELLE-LLaMA-Local": "/pretrainmodel/belle",
    },
    "vicuna": {
        "Vicuna-Local": "/pretrainmodel/vicuna",
    }
}
>>>>>>> 33ec2a55e31a7a49367b754399c8ddfe9750a4e2
