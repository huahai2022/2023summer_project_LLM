from typing import Any

from config import LLM_DEVICE


class LoadCheckpoint:
	#模型名称
	model_name:str=None
	tokenizer:object=None   #定义分词器
	#模型路径
	model_path:str=None
	model:object=None
	model_config:object=None
	use_ptuning_v2:bool=False
	ptuning_dir:str=None
	load_in_8bit:bool=False
	bf16:bool=False   #是否使用16精度数据
	#定义网络设备
	llm_device=LLM_DEVICE
	def __init__(self,params:dict=None):
		self.model=None
		self.tokenizer=None
		self.params=params
		self.model_name=params.get("model_name",None)
		self.model_path=params.get("model_path",None)
		self.use_ptuning_v2=params.get("use_ptuning_v2",False)
		self.ptuning_dir=params.get("ptuning_dir","ptuning-v2")
		self.load_in_8bit=params.get("load_in_8bit",False)
		self.bf16=params.get("bf16",False)





loaderCheckpoint:LoadCheckpoint=None
def load_model(model_name:str=None,use_ptuning_v2:bool=False)->Any:
	pre_model_name=loaderCheckpoint.model_name
	llm_model_config=None
