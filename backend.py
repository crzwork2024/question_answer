from fastapi import FastAPI, HTTPException  
from pydantic import BaseModel  
from langchain.vectorstores import Chroma  


from utilities import *
from config import *

app = FastAPI()  
  
# 定义请求体  
class Item(BaseModel):  
    query: str  
 
# 加载预训练的文本嵌入模型  
embeddings = CustomEmbeddings(model_name=model_id)
  
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
    
    # 存储数据到向量数据库  
    Answers_list_dict = [{'回答':"暂无回答"}]
    vectorstore = index_texts([item.query], embeddings, persist_directory, collection_name, Answers_list_dict)
        
# 运行 FastAPI 应用   uvicorn backend:app --reload
if __name__ == "__main__":  
    import uvicorn  
    uvicorn.run(app, host="127.0.0.1", port=8000)