# 问题回答系统  
  
这是一个利用Python、Streamlit、Sentence-transformers、Langchain以及Chroma Database共同构建的问题回答系统。
  
## 设置步骤  
  
1. **克隆仓库**：  
   ```bash  
   git clone https://github.com/crzwork2024/question_answer 
   cd question_answer
   ```

2. **安装所需依赖**：
```bash
    pip install -r requirements.txt
```

3. **配置config脚本**：<br>
此脚本负责配置模型名字，Chroma向量数据库数据存储位置等。
```bash
    python storedata.py
```

4. **运行storedata脚本**：<br>
此脚本负责将示例数据保存到向量数据库中。
```bash
    python storedata.py
```

5. **启动后端服务器**：<br>
使用Uvicorn来运行后端。
```bash
    uvicorn backend:app --reload
```

6. **运行前端界面**：<br>
通过Streamlit来启动前端。
```bash
    streamlit run frontend.py
```

**文件与目录结构**:<br>
utilities.py：存放项目中使用的实用函数; <br>
config.py：包含项目的所有配置文件; <br>
frontend.py：包含Streamlit的前端代码; <br>
backend.py：包含后端代码，其中包含一个Flask应用; <br>
storedata.py：一个用于将示例数据保存到向量数据库中的脚本; <br>
requirements.txt: 列出所以需要安装的包; <br>
.gitignore： 用于指定在版本控制系统Git中应该被忽略的文件和目录。 <br>




**使用方法**:<br>
在完成storedata脚本、后端服务器和前端的运行后，网页浏览器会自动打开，问答系统准备就绪。

