from langchain_community.embeddings import ModelScopeEmbeddings  
from langchain.vectorstores import Chroma  
import pandas as pd
  
# 加载预训练的文本嵌入模型  
model_id = r"C:\Users\RONGZHEN CHEN\Desktop\Projects\models\acge_text_embedding"  
embeddings = ModelScopeEmbeddings(model_id=model_id)  


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
 
Questions_list, Answers_list = load_data()     



#初始化Chroma向量数据库  
persist_directory = r"C:\Users\RONGZHEN CHEN\Desktop\Projects\data\vectordatabase"  
collection_name = 'test'  
 

# 删除数据库内容 （真实环境中可以删除这段代码）
vectorstore =  Chroma(persist_directory=persist_directory, collection_name = collection_name)
doc_ids = vectorstore.get()["ids"]
if len(doc_ids)>0:
    vectorstore.delete(ids=doc_ids)
    
      
# 将数据库中的文本转换为向量并存储到向量数据库中  
def index_texts(texts, embeddings, persist_directory, collection_name, metadata):  
    vectorstore = Chroma.from_texts(texts=texts, embedding=embeddings, persist_directory=persist_directory, collection_name=collection_name, metadatas=metadata)  
    return vectorstore  
  
# 存储数据到向量数据库  

Answers_list_dict = [{'回答':x} for x in Answers_list]
vectorstore = index_texts(Questions_list, embeddings, persist_directory, collection_name, Answers_list_dict)
