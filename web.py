from DB import MyLocalDB
from args import parser
from config import *
import gradio as gr
from model import load_model
from models.loader import LoadCheckpoint

flag_csv_logger=gr.CSVLogger()
def init_model():
	args=parser.parse_args()
	args_dict=vars(args)
	loadCheckpoint=LoadCheckpoint(args_dict)
	model=load_model(loaderCheckpoint=loadCheckpoint)
	global localDB
	localDB=MyLocalDB(llm_model=model)
	reply="""模型已经加载完成，可以开始对话"""
	logger.info(reply)
	return reply
def get_answer(question,db_path,history,mode):
	if mode=="知识库问答":
		for response,history in localDB.get_answer_based_query(query=question,vs_path=db_path, chat_history=history,stream=True ):
			source="\n\n"
			source+="".join(
                [f""" 出处 [{i + 1}] {os.path.split(doc.metadata["source"])[-1]}\n\n"""
                 f"""{doc.page_content}\n\t相似度得分为{doc.metadata["score"]}\n\n"""
                 for i, doc in
                 enumerate(response["source_documents"])
				 ])
			history[-1][-1]+=source
			yield history,""
	else:
		for answer_result in localDB.llm.generatorAnswer(prompt=question,history=history,streaming=True):
			response=answer_result.llm_output["answer"]
			history=answer_result.history
			history[-1][-1]=response
			yield history,""
	logger.info(f"question={question},db_path={db_path},mode={mode},history={history}")
	flag_csv_logger.flag([question,db_path,history,mode])



model_info=init_model()
with gr.Blocks() as web:
	db_path,file_info,model_info=gr.State(os.path.join(ROOT_PATH,"vector_store")),gr.State(""),gr.State(model_info)
	gr.Markdown(WEB_TITLE)
	with gr.Tab("畅谈"):
		with gr.Row():

			with gr.Column(scale=10):
				chatbot=gr.Chatbot([[None,model_info.value]],elem_id="chat-box",show_label=False).style(height=500)
				question=gr.Textbox(show_label=False,placeholder="请输入你的问题，ENTER以提交").style(container=False)

			with gr.Column(scale=5):
				mode=gr.Radio(["自由对话","知识库问答"],
							  label="请选择你要使用的模式",
							  value="知识库问答",)

				flag_csv_logger.setup([question,db_path,chatbot,mode],"flagged")
				question.submit(fn=get_answer,inputs=[question,db_path,chatbot,mode],
								outputs=[chatbot,question])
(web.queue(concurrency_count=2).launch(server_name="0.0.0.0",server_port=12345,show_api=False,share=True,inbrowser=False))