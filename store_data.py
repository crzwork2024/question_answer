# 从utilities模块中导入所有内容
from utilities import *  
# 从config模块中导入所有内容
from config import *

# 使用指定的模型名称（model_id）创建一个CustomEmbeddings类的实例，并将其赋值给变量embeddings  
embeddings = CustomEmbeddings(model_name=model_id)

# 加载CSV数据
Questions_list, Answers_list = load_data(raw_data_path)     

# 删除向量数据库中的数据
delete_db(persist_directory, collection_name)
  
# 存储数据到向量数据库  
Answers_list_dict = [{'回答':x} for x in Answers_list]
vectorstore = index_texts(Questions_list, embeddings, persist_directory, collection_name, Answers_list_dict)
