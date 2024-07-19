# 从fastapi包中导入FastAPI类和HTTPException异常类  
from fastapi import FastAPI, HTTPException    
# 从pydantic包中导入BaseModel基类，用于数据验证  
from pydantic import BaseModel    
# 从langchain.vectorstores包中导入Chroma类，可能用于向量存储或检索  
from langchain.vectorstores import Chroma    
# 从utilities模块中导入所有内容，这可能包含一些实用函数或类  
from utilities import *  
# 从config模块中导入所有内容，这可能包含配置信息或设置  
from config import *


# 创建了一个 FastAPI 应用实例
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
    retriever = vectorstore.as_retriever(search_kwargs={"k": VECTORSTORE_MAX_K})  
    results = retriever.get_relevant_documents(item.query)  
  
    if not results:  
        raise HTTPException(status_code=404, detail="查询结果为空")  
  
    return {"results": results}  

@app.post("/add/")  
async def add_item(item: Item):  
    
    # 存储数据到向量数据库  
    Answers_list_dict = [{'回答':"暂无回答"}]
    vectorstore = index_texts([item.query], embeddings, persist_directory, collection_name, Answers_list_dict)
    
@app.post("/filter/")  
async def filter():  
    
    # 筛选暂未回答的问题
    results = vectorstore.get(where={'回答':"暂无回答"})
    
    df = pd.DataFrame({  
    'ids': results['ids'],  
    'documents': results['documents'],  
    'metadatas': results['metadatas']})  
    
    return df, results

@app.post("/update/")  
async def update(d: dict):  
    from langchain_core.documents import Document


    doc = Document(
    page_content=d["page_content"],
    metadata=d["answer"]
    )
  
    id = d["id"]
    
    vectorstore.update_document(id, doc)
        
# 运行 FastAPI 应用   uvicorn backend:app --reload
if __name__ == "__main__":  
    import uvicorn  
    uvicorn.run(app, host=UVICORN_HOST, port=UVICORN_HOST_PORT)