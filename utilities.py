from typing import List
from langchain.vectorstores import Chroma  
import pandas as pd
from sentence_transformers import SentenceTransformer
from langchain.embeddings.base import Embeddings


# 将数据库中的文本转换为向量并存储到向量数据库中  
def index_texts(texts, embeddings, persist_directory, collection_name, metadata):  
    vectorstore = Chroma.from_texts(texts=texts, embedding=embeddings, persist_directory=persist_directory, collection_name=collection_name, metadatas=metadata)  
    return vectorstore  


def load_data():
        
        #假设你的txt文件名为'data.txt'  
        file_path = r'C:\Users\RONGZHEN CHEN\Desktop\Projects\data\sample_data.txt'
        
        #使用pandas的read_csv函数读取文件，设置sep为'?'  
        df = pd.read_csv(file_path, sep='？，')  # header=None 假设文件没有标题行  
  
        # 如果你知道列的名称，可以手动设置它们  
        column_names = ['Questions', 'Answers']  
        df.columns = column_names 

        #result_dict = {row['Questions']: row['Answers'] for index, row in df.iterrows()}  

        Questions_list = df['Questions'].tolist()  
        Answers_list = df['Answers'].tolist()
        return Questions_list, Answers_list
    
    
def delete_db(persist_directory, collection_name):
# 删除数据库内容 （真实环境中可以删除这段代码）
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
        

    