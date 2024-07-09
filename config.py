
#初始化Chroma向量数据库  
persist_directory = r"C:\Users\RONGZHEN CHEN\Desktop\Projects\data\vectordatabase"  
collection_name = 'test' 

# 模型文件夹路径
model_id = r"C:\Users\RONGZHEN CHEN\Desktop\Projects\models\acge_text_embedding"  

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