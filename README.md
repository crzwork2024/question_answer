# 问题回答系统  
  
这是一个利用Python、Streamlit、ModelScope以及Chroma Database共同构建的问题回答系统。  
  
## 设置步骤  
  
1. **克隆仓库**：  
   ```bash  
   git clone https://github.com/您的GitHub用户名/问题回答系统.git  
   cd 问题回答系统
   ```

2. **安装所需依赖**：
```bash
    pip install -r requirements.txt
```
3. **运行storedata脚本**：
此脚本负责将示例数据保存到向量数据库中。
```bash
    python storedata.py
```

4. **启动后端服务器**：
使用Uvicorn来运行后端。
```bash
    uvicorn backend:app --reload
```

5. **运行前端界面**：
通过Streamlit来启动前端。
```bash
    streamlit run frontend.py
```

**文件与目录结构**
utilities：存放项目中使用的实用函数; <br>
config：包含项目的所有配置文件; <br>
frontend：包含Streamlit的前端代码; <br>
backend：包含后端代码，其中包含一个Flask应用; <br>
storedata：一个用于将示例数据保存到向量数据库中的脚本。<br>

**使用方法**
在完成storedata脚本、后端服务器和前端的运行后，网页浏览器会自动打开，问答系统准备就绪。

