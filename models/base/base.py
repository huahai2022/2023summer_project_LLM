from abc import ABC, abstractmethod
from typing import Optional,List
from models.loader import LoadCheckpoint




class AnswerResult:
	"定义消息实体"
	history:List[List[str]]=[]
	llm_output:Optional[dict]=None
class BaseAnswer(ABC):
	@property
	@abstractmethod
	def _check_point(self) -> LoadCheckpoint:
		pass

	@property
	@abstractmethod
	def _history_len(self) -> int:
		"""Return _history_len of llm."""

	@abstractmethod
	def set_history_len(self, history_len: int) -> None:
		"""Return _history_len of llm."""

	def generatorAnswer(self, prompt: str,
						history: List[List[str]] = [],
						streaming: bool = False):
		pass