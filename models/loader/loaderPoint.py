import gc
import sys
from pathlib import Path
from typing import Any, Optional, Dict
import json

import torch
import transformers
from transformers import AutoConfig, AutoModel, AutoModelForCausalLM, LlamaTokenizer, AutoTokenizer
from config import LLM_DEVICE, llm_model_dict, ACCESS_HUGGING_TOKEN

class LoadCheckpoint:
	#模型名称
	model_name:str=None
	tokenizer:object=None   #定义分词器
	# 在机器学习和深度学习中，通常将文本表示为数字或向量，以便计算机可以处理和学习。而将文本转换为数字或向量的第一步是将文本拆分成单词或词组。这个过程就是
	# Tokenization，即将一段文本分解成单词或词组的过程。Tokenizer
	# 可以使用不同的策略来进行文本分解，例如基于空格分隔符的分词、基于规则的分词、基于机器学习的分词等。其中，基于机器学习的分词通常使用深度学习模型，例如循环神经网络（Recurrent
	# NeuralNetwork，RNN）、卷积神经网络（ConvolutionalNeuralNetwork，CNN）和Transformer等模型。
	#模型路径
	model_path:str=None
	model:object=None
	model_config:object=None
	use_ptuning_v2:bool=False
	ptuning_dir:str=None
	load_in_8bit:bool=False
	bf16:bool=False   #是否使用16精度数据
	#定义自定义网络
	device_map:Optional[Dict[str,int]]=None
	#定义网络设备
	llm_device=LLM_DEVICE
	def __init__(self,params:dict=None):
		self.model=None
		self.tokenizer=None
		self.params=params or {}
		self.model_name=params.get("model_name",None)
		self.model_path=params.get("model_path",None)
		self.use_ptuning_v2=params.get("use_ptuning_v2",False)
		self.ptuning_dir=params.get("ptuning_dir","ptuning-v2")
		self.load_in_8bit=params.get("load_in_8bit",False)
		self.bf16=params.get("bf16",False)
	def unload_model(self):
		del self.model
		del self.tokenizer
		self.model=self.tokenizer=None
		gc.collect()
		# `del ` 关键字可以删除对象或变量。在这里，`del self.model` 和 `del self.tokenizer` 语句用于删除对象 `self.model
		# ` 和 `self.tokenizer，以释放内存。在删除对象之后，将`self.model`和`self.tokenizer`设置为
		# `None`是一种良好的编程习惯，它可以帮助开发者避免使用已经删除的对象，从而避免出现"ReferenceError"或"AttributeError"
		# 等错误。将对象设置为`None`可以确保在后续代码中检查该对象时，不会因为对象不存在而导致程序崩溃。
	def reload_model(self):
		self.unload_model()
		print(self.model_name)
		self.model_config=self.load_model_config(self.model_name)
		if self.use_ptuning_v2:
			try:
				prefix_encoder_file=open(Path(f'{self.ptuning_dir}/config.json'),'r')
				prefix_encoder_config=json.loads(prefix_encoder_file.read())
				prefix_encoder_file.close()
				self.model_config.pre_sea_len=prefix_encoder_config['pre_seq_len']
				self.model_config.prefix_projection = prefix_encoder_config['prefix_projection']

				# PTuning
				# 技术的原理是基于半监督学习和自适应训练的思想，通过最大化有标注数据和无标注数据之间的相似度来训练模型，从而提高模型的泛化能力和性能。具体来说，PTuning
				# 技术包括以下两个关键步骤：1.生成前缀序列和前缀投影矩阵在PTuning
				# 技术中，为了适应特定任务的需求，需要生成一个前缀序列和一个前缀投影矩阵，用于微调模型。前缀序列是一个固定长度的序列，可以用于指导模型学习任务相关的特征。前缀投影矩阵是一个
				# 权重矩阵，可以用于将输入向量投影到前缀序列的空间中，从而提高模型在语义匹配和相似度计算任务上的性能。
				# 2.半监督微调在PTuning
				# 技术中，使用少量的有标注数据和大量的无标注数据对模型进行微调，以适应特定任务的需求。在微调过程中，使用前缀序列和前缀投影矩阵来指导模型学习任务相关的特征。具体来说，PTuning
				# 技术使用了一个新的损失函数，称为Pairwise Ranking Loss，用于最大化有标注数据和无标注数据之间的相似度。Pairwise
				# Ranking Loss 可以用于比较两个输入的相似性，从而提高模型在语义匹配和相似度计算任务上的性能。在微调过程中，模型使用有标注数据计算
				# Pairwise Ranking Loss，使用无标注数据计算自监督损失，从而提高模型的泛化能力和性能。总之，PTuning
				# 技术通过使用前缀序列和前缀投影矩阵，以及半监督微调的方式，可以提高模型在语义匹配和相似度计算任务上的性能，并且可以适应不同的任务需求。
			except :
				print(Exception)
				print("加载prefixEncoder失败")
		self.model,self.tokenizer=self.load_model(self.model_name)
		if self.use_ptuning_v2:
			try:
				prefix_state_dict=torch.load(Path(f'{self.ptuning_dir}/pytorch_model.bin'))
				new_prefix_state_dict={}
				for k,v  in prefix_state_dict.items():
					if k.startswith("transformer.prefix_encoder."):
						new_prefix_state_dict[k[len("transformer.prefix_encoder."):]]=v
				self.model.transformer.prefix_encoder.load_state_dict(new_prefix_state_dict)
				self.model.transformer.prefix_encoder.float()
			except Exception as e:
				print(e)
		self.model=self.model.eval()
	def load_model_config(self,model_name):
		if self.model_path:
			checkpoint=Path(f'{self.model_path}')
		else:
			checkpoint=model_name
		print(self.model_path)
		model_config=AutoConfig.from_pretrained(checkpoint,trust_remote_code=True,use_auth_token=ACCESS_HUGGING_TOKEN)
		# print(model_config)ChatGLMConfig {
		#   "_name_or_path": "THUDM/chatglm-6b",
		#   "architectures": [
		#     "ChatGLMModel"
		#   ],
		#   "auto_map": {
		#     "AutoConfig": "THUDM/chatglm-6b--configuration_chatglm.ChatGLMConfig",
		#     "AutoModel": "THUDM/chatglm-6b--modeling_chatglm.ChatGLMForConditionalGeneration",
		#     "AutoModelForSeq2SeqLM": "THUDM/chatglm-6b--modeling_chatglm.ChatGLMForConditionalGeneration"
		#   },
		#   "bos_token_id": 130004,
		#   "eos_token_id": 130005,
		#   "gmask_token_id": 130001,
		#   "hidden_size": 4096,
		#   "inner_hidden_size": 16384,
		#   "layernorm_epsilon": 1e-05,
		#   "mask_token_id": 130000,
		#   "max_sequence_length": 2048,
		#   "model_type": "chatglm",
		#   "num_attention_heads": 32,
		#   "num_layers": 28,
		#   "pad_token_id": 3,
		#   "position_encoding_2d": true,
		#   "pre_seq_len": null,
		#   "prefix_projection": false,
		#   "quantization_bit": 0,
		#   "torch_dtype": "float16",
		#   "transformers_version": "4.30.2",
		#   "use_cache": true,
		#   "vocab_size": 130528
		# }
		return model_config

	def load_model(self, model_name):
		global model
		print(f"稍安勿躁，正在加载{model_name}...")
		if self.model_path:
			checkpoint=Path(f"{self.model_path}")
		else:
			print("未配置本地路径，download from Internet~")
			checkpoint=model_name
		if 'chatglm' in model_name.lower():
			loaderClass=AutoModel
		else:
			loaderClass=AutoModelForCausalLM   #因果语言模型
		#多卡部署
		if self.load_in_8bit:
			from accelerate import init_empty_weights
			from accelerate.utils import get_balanced_memory,infer_auto_device_map
			from transformers import BitsAndBytesConfig
			params={"low_cpu_mem_usage":True}
			if not self.llm_device.lower().startswith("cuda"):
				raise SystemError("8bit模型需要CUDA的支持，或者更改量化后的模型")
			else:
				params["device_map"]='auto'
				params["trust_remote_coda"]=True
				params['quantization_config']=BitsAndBytesConfig(load_in_8bit=True,
																 llm_int8_enable_fp32_cpu_offload=False)
				with init_empty_weights():
					model = loaderClass.from_config(self.model_config, trust_remote_code=True)
				model.tie_weights()
				if self.device_map is not None:
					params['device_map']=self.device_map

				else:
					from accelerate import dispatch_model
					model = loaderClass.from_pretrained(checkpoint, config=self.model_config,
														torch_dtype=torch.bfloat16,
														trust_remote_code=True).half()
					num_gpus = torch.cuda.device_count()
					if 'chatglm' in model_name.lower():
						self.device_map = self.chatglm_config_device_map(num_gpus)
					elif 'moss' in model_name.lower():
						self.device_map = self.moss_config_device_map(num_gpus)
					else:
						self.device_map = self.chatglm_config_device_map(num_gpus)
					model = dispatch_model(model, device_map=self.device_map)
			pass
		else:
			# 多卡部署
			if torch.cuda.is_available() and self.llm_device.lower().startswith("cuda"):
				num_gpus=torch.cuda.device_count()
				if num_gpus==1:
					model=loaderClass.from_pretrained(checkpoint,config=self.model_config,torch_dtype=torch.bfloat16 if self.bf16 else torch.float16,trust_remote_code=True).half().cuda()
				else:
					from accelerate import dispatch_model
					model=loaderClass.from_pretrained(checkpoint,config=self.model_config,torch_dtype=torch.bfloat16 if self.bf16 else torch.float16,trust_remote_code=True).half()
					# 查看模型的层都有哪些
					for name, param in model.named_parameters():
						# 打印参数的名称和形状
						print(f'{name} - {param.shape}')
					#定义每张卡的部署情况
					if not self.device_map :
						if 'chatglm' in model_name.lower():
							self.device_map= self.chatglm_config_device_map(num_gpus)
						elif 'moss' in model_name.lower():
							self.device_map=self.moss_config_device_map(num_gpus)
						else:
							self.device_map=self.chatglm_config_device_map(num_gpus)
					model=dispatch_model(model,device_map=self.device_map)
			else:
			#cpu部署
				model=(loaderClass.from_pretrained(checkpoint,config=self.model_config,trust_remote_code=True).float().to(self.llm_device))


		# loading the tokenizer

		if type(model) is transformers.LlamaForCausalLM:
			tokenizer=LlamaTokenizer.from_pretrained(checkpoint,clean_up_tokenization_spaces=True)
			try:
				tokenizer.eos_token_id = 2
				tokenizer.bos_token_id = 1
				tokenizer.pad_token_id = 0
			except Exception as e:
				print(e)
		else:
			tokenizer=AutoTokenizer.from_pretrained(checkpoint,trust_remote_code=True)
		return model,tokenizer

	def chatglm_config_device_map(self,num_gpus:int)->Dict[str,int]:
		# transformer.word_embeddings 占用1层
		# transformer.final_layernorm 和 lm_head 占用1层
		# transformer.layers 占用 28 层
		num_trans_layers=28
		pre_gpu_layers=30/num_gpus
		layer_prefix='transformer'
		# 在调用chat或者stream_chat时,input_ids会被放到model.device上
		# 如果transformer.word_embeddings.device和model.device不同,则会导致RuntimeError
		# 因此这里将transformer.word_embeddings,transformer.final_layernorm,lm_head都放到第一张卡上
		device_map={f'{layer_prefix}.word_embeddings':0,
					f'{layer_prefix}.final_layernorm':0,
					'lm_head':0,f'base_model.model.lm_head':0,}
		used=2
		gpu_target=0
		for i in range(num_trans_layers):
			if used>=pre_gpu_layers:
				gpu_target+=1
				used=0
			assert gpu_target<num_gpus
			device_map[f'{layer_prefix}.layers.{i}']=gpu_target
			used+=1
		return device_map


	def moss_config_device_map(self,num_gpus:int)->Dict[str,int]:
		from accelerate import init_empty_weights
		from accelerate.utils import get_balanced_memory, infer_auto_device_map
		from transformers.dynamic_module_utils import get_class_from_dynamic_module
		from transformers.modeling_utils import no_init_weights
		from transformers.utils import ContextManagers
		if self.model_path:
			checkpoint=Path(f'{self.model_path}')
		else:
			checkpoint=self.model_name
		cls = get_class_from_dynamic_module(class_reference="fnlp/moss-moon-003-sft--modeling_moss.MossForCausalLM",
											pretrained_model_name_or_path=checkpoint)
		with ContextManagers([no_init_weights(_enable=True), init_empty_weights()]):
			model = cls(self.model_config)
			max_memory = get_balanced_memory(model, dtype=torch.int8 if self.load_in_8bit else None,
											 low_zero=False, no_split_module_classes=model._no_split_modules)
			device_map = infer_auto_device_map(
				model, dtype=torch.float16 if not self.load_in_8bit else torch.int8, max_memory=max_memory,
				no_split_module_classes=model._no_split_modules)
			device_map["transformer.wte"] = 0
			device_map["transformer.drop"] = 0
			device_map["transformer.ln_f"] = 0
			device_map["lm_head"] = 0
			return device_map
