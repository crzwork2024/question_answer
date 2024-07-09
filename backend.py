from fastapi import FastAPI, HTTPException  
from pydantic import BaseModel  
from langchain.vectorstores import Chroma  
from langchain_community.embeddings import ModelScopeEmbeddings 
from langchain_core.vectorstores import VectorStoreRetriever
from utilities import *
from config import *

app = FastAPI()  
  
# 定义请求体  
class Item(BaseModel):  
    query: str  
 
# 加载预训练的文本嵌入模型  
embeddings = ModelScopeEmbeddings(model_id=model_id)  
  
# 加载向量数据库  

vectorstore = Chroma(persist_directory=persist_directory, collection_name=collection_name, embedding_function=embeddings)
  
@app.post("/search/")  
async def search(item: Item):  
    retriever = vectorstore.as_retriever(search_kwargs={"k": 4})  
    results = retriever.get_relevant_documents(item.query)  
  
    if not results:  
        raise HTTPException(status_code=404, detail="查询结果为空")  
  
    return {"results": results}  

@app.post("/add/")  
async def add_item(item: Item):  
    #vectorstore.from_documents(item.query,embeddings)
    #print("###################", item.query)
    
    # 存储数据到向量数据库  
    Answers_list_dict = [{'回答':"暂无回答"}]
    vectorstore = index_texts([item.query], embeddings, persist_directory, collection_name, Answers_list_dict)

    #vectorstore.add_texts(texts=item.query,  metadatas=item.metadata)
    #document_id = vectorstore.add_documents([{"page_content":"test"}])  
    #return {"document_id": document_id, "message": "文档已成功添加"}
    #retriever = VectorStoreRetriever.from_vectorstore(vectorstore)  
    #results = retriever.get_relevant_documents(item.query)  
      
    # 检查查询结果  
    #if results:  
     #   print("查询验证成功，找到了新添加的文本！")  
    #else:  
    #    print("查询验证失败，未找到新添加的文本。") 
        
        
# 运行 FastAPI 应用  
# uvicorn backend:app --reload
if __name__ == "__main__":  
    import uvicorn  
    uvicorn.run(app, host="127.0.0.1", port=8000)