
from utilities import *
from config import *

    
embeddings = CustomEmbeddings(model_name=model_id)

# 加载CSV数据
Questions_list, Answers_list = load_data()     

# 删除向量数据库中的数据
delete_db(persist_directory, collection_name)
  
# 存储数据到向量数据库  
Answers_list_dict = [{'回答':x} for x in Answers_list]
vectorstore = index_texts(Questions_list, embeddings, persist_directory, collection_name, Answers_list_dict)
