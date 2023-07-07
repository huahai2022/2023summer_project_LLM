import gc
import sys
from pathlib import Path
from typing import Any, Optional, Dict
import json

import torch
import transformers
from transformers import AutoConfig, AutoModel, AutoModelForCausalLM, LlamaTokenizer, AutoTokenizer

from config import LLM_DEVICE, llm_model_dict, ACCESS_HUGGING_TOKEN, LLM_HISTORY_LEN
from models import ChatGLM, MOSS


def load_model(model_name:str=None,use_ptuning_v2:bool=False,loaderCheckpoint:object=None)->Any:
	pre_model_name=loaderCheckpoint.model_name
	llm_model_config=llm_model_dict[pre_model_name]
	# if use_ptuning_v2:
	# 	loaderCheckpoint.use_ptuning_v2=use_ptuning_v2
	# if model_name:
	# 	llm_model_config=llm_model_dict[model_name]
	loaderCheckpoint.model_name=llm_model_config["pretrained_model_name"]
	loaderCheckpoint.model_path=llm_model_config["local_model_path"]
	loaderCheckpoint.reload_model()
	if loaderCheckpoint.model_name.lower().startswith("thudm"):
		provides_class=ChatGLM
	elif loaderCheckpoint.model_name.lower().startswith("fnlp"):
		provides_class=MOSS
	else:
		# provides_class=LLamaLLM
		pass
	modelLLM=provides_class(checkPoint=loaderCheckpoint)
	modelLLM.history_len=LLM_HISTORY_LEN
	return modelLLM

