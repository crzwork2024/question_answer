import streamlit as st  
import requests  
import sys
import time  
  
def on_button_click():  
    st.success('操作成功！')  
  
    
    
 
st.title("智能问答系统")
  
# 后端API的URL  
BACKEND_URL = "http://127.0.0.1:8000/search/"  
  
# 创建一个聊天输入框  
user_input = st.chat_input("请输入你的问题：")  
  
# 当用户提交问题时，发送请求到后端API  
if user_input:  
    # 发送POST请求到后端  
    response = requests.post(BACKEND_URL, json={"query": user_input})  
      
    # 检查响应状态码  
    if response.status_code == 200:  
        # 显示后端返回的结果  
        result = response.json() 
        #st.write("最接近的文本是：", result["results"])
    
        original_question = user_input
        reference_question = result["results"][0]["page_content"]
        reference_answer = result["results"][0]["metadata"]["回答"]
       
        st.chat_message(name='user', avatar='🧑').markdown("使用者提问: "+original_question)
        st.chat_message(name='ai', avatar='🤖').markdown("数据库中答案: "+reference_answer + "\n\n数据库中原问题: "+reference_question ) 
    
        st.markdown(f"**可能感兴趣的其他相关问题**") 
        
        size = len(result["results"])
       
        for i in range(1, size):
            with st.expander("{}".format(result["results"][i]["page_content"])):
                st.write("{}".format( result["results"][i]["metadata"]["回答"]))
                

        if st.button('点击我'):  
            on_button_click()
    
    else:  
        # 显示错误信息  
        st.write("错误：", response.status_code, response.text)
        
        
        
        
