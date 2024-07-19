
# 初始化Chroma向量数据库  
persist_directory = r"C:\Users\RONGZHEN CHEN\Desktop\Projects\data\vectordatabase"  
# 集合（Collection）可以看作是一组文档的集合，类似数据库中的表
collection_name = 'test1' 

# 模型文件夹路径
model_id = r"C:\Users\RONGZHEN CHEN\Desktop\Projects\models\acge_text_embedding"  

# 返回与查询最相关的前k个结果
VECTORSTORE_MAX_K = 4

# 设置Uvicorn的主机地址
UVICORN_HOST = "127.0.0.1"

# 设置Uvicorn的主机端口
UVICORN_HOST_PORT = 8000

# 后端SEARCH API的URL  
BACKEND_URL_ADD = "http://127.0.0.1:8000/add/" 

# 后端SEARCH API的URL  
BACKEND_URL_SEARCH = "http://127.0.0.1:8000/search/" 

# 插入CSS样式  
button_style = """  
<style>  
    div.stButton > button:first-child {  
        background-color: #4CAF50; /* 按钮背景色 */  
        color: white; /* 字体色 */  
        border: none; /* 移除边框 */  
    }  
    div.stButton > button:first-child:hover {  
        background-color: #45a049; /* 鼠标悬停时的背景色 */  
    }  
</style>  
"""  

