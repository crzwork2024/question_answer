# 从typing模块中导入List类型，用于类型注解  
from typing import List  
# 从langchain.vectorstores包中导入Chroma类，用于向量存储或检索  
from langchain.vectorstores import Chroma  
# 导入pandas库，并简称为pd，用于数据处理和分析  
import pandas as pd  
# 从sentence_transformers库导入SentenceTransformer类，用于文本嵌入  
from sentence_transformers import SentenceTransformer  
# 从langchain.embeddings.base模块导入Embeddings基类，用于定义嵌入相关的功能  
from langchain.embeddings.base import Embeddings
# 导入streamlit库，并将其简称为st，用于创建和分享数据应用  
import streamlit as st    
# 导入requests库，用于发送HTTP请求  
import requests    
# 从config模块中导入所有内容，这可能包含配置信息或设置   
from config import *

# 将数据库中的文本转换为向量并存储到向量数据库中  
def index_texts(texts, embeddings, persist_directory, collection_name, metadata):  
    vectorstore = Chroma.from_texts(texts=texts, embedding=embeddings, persist_directory=persist_directory, collection_name=collection_name, metadatas=metadata)  
    return vectorstore  

# 导入原始数据
def load_data(file_path):
        
        #使用pandas的read_csv函数读取文件，设置sep为'?'  
        df = pd.read_csv(file_path, sep='？，')  # header=None 假设文件没有标题行  
  
        # 如果你知道列的名称，可以手动设置它们  
        column_names = ['Questions', 'Answers']  
        df.columns = column_names 

        #result_dict = {row['Questions']: row['Answers'] for index, row in df.iterrows()}  

        Questions_list = df['Questions'].tolist()  
        Answers_list = df['Answers'].tolist()
        return Questions_list, Answers_list
    
# 定义一个名为delete_db的函数，删除数据库内容      
def delete_db(persist_directory, collection_name):
# 删除数据库内容 
    vectorstore =  Chroma(persist_directory=persist_directory, collection_name = collection_name)
    doc_ids = vectorstore.get()["ids"]
    if len(doc_ids)>0:
        vectorstore.delete(ids=doc_ids)
        

# 定义一个名为CustomEmbeddings的类，它继承自Embeddings类  
class CustomEmbeddings(Embeddings):  
    # 类的构造函数，接收一个模型名称作为参数  
    def __init__(self, model_name: str):  
        # 使用提供的模型名称初始化SentenceTransformer模型，并将其存储在实例变量self.model中  
        self.model = SentenceTransformer(model_name)  
  
    # 定义一个方法，用于将文档列表转换为嵌入向量列表  
    def embed_documents(self, documents: List[str]) -> List[List[float]]:  
        # 使用列表推导式和模型的encode方法，将每个文档转换为嵌入向量，并返回这些向量的列表  
        return [self.model.encode(d).tolist() for d in documents]  
  
    # 定义一个方法，用于将单个查询转换为嵌入向量  
    def embed_query(self, query: str) -> List[float]:  
        # 将查询包装在列表中，使用模型的encode方法进行转换，并返回转换后的嵌入向量的列表形式（取第一个元素）  
        return self.model.encode([query])[0].tolist()
        

def on_button_click(original_question):  
    
    response = requests.post(BACKEND_URL_ADD, json={"query":original_question})  
    #st.write(response.json())
    if response.status_code == 200: 
       
        # 拆分消息，并只对original_question部分应用颜色  
        message_part1 = "问题"  
        message_part2 = f'已成功添加至数据库，随后我们将邀请专家前来解答！'  
        colored_question = f'<span style="color: green;">{original_question}</span>'  
        
        # 组合消息并显示  
        full_message = f'{message_part1} {colored_question}{message_part2}'  
        st.markdown(full_message, unsafe_allow_html=True)
    
def clear_messages():  
    # 清空聊天记录  
    st.session_state.messages = []  