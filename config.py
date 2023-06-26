LOAD_IN_8BIT = False
LLM_DEVICE = "cuda"
LLM_MODEL = "chatglm-6b"
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
