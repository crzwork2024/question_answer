from fastapi import FastAPI, HTTPException  
from pydantic import BaseModel  
from langchain.vectorstores import Chroma  
from langchain_community.embeddings import ModelScopeEmbeddings 
  
app = FastAPI()  
  
# 定义请求体  
class Item(BaseModel):  
    query: str  
 
# 加载预训练的文本嵌入模型  
model_id = r"C:\Users\RONGZHEN CHEN\Desktop\Projects\models\acge_text_embedding"  
embeddings = ModelScopeEmbeddings(model_id=model_id)  
  
# 加载向量数据库  
persist_directory = r"C:\Users\RONGZHEN CHEN\Desktop\Projects\data\vectordatabase"  
collection_name = 'test'  
#vectorstore = Chroma.load_from_directory(persist_directory, collection_name=collection_name)  
vectorstore = Chroma(persist_directory=persist_directory, collection_name=collection_name, embedding_function=embeddings)
  
@app.post("/search/")  
async def search(item: Item):  
    retriever = vectorstore.as_retriever(search_kwargs={"k": 4})  
    results = retriever.get_relevant_documents(item.query)  
  
    if not results:  
        raise HTTPException(status_code=404, detail="查询结果为空")  
  
    return {"results": results}  
  
# 运行 FastAPI 应用  
# uvicorn backend:app --reload
if __name__ == "__main__":  
    import uvicorn  
    uvicorn.run(app, host="127.0.0.1", port=8000)