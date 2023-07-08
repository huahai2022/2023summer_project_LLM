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
