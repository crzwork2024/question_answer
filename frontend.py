# 导入streamlit库，并将其简称为st，用于创建和分享数据应用  
import streamlit as st    
# 导入requests库，用于发送HTTP请求  
import requests    
# 从config模块中导入所有内容，这可能包含配置信息或设置  
from config import *
# 从utilities模块中导入所有内容，这可能包含一些实用函数或类  
from utilities import *  

# 初始化 session_state  
if 'user_input' not in st.session_state:  
    st.session_state.user_input = ''  
if 'messages' not in st.session_state:  
    st.session_state.messages = []  

# 设置Streamlit页面的配置，包括标题  
st.set_page_config(page_title="智能问答系统", page_icon="🚀")  
 
# 界面最上面标题       
st.title("智能问答系统")  
  
# 创建一个聊天输入框  
user_input = st.chat_input("请输入你的问题：")  
  
# 当用户提交问题时，更新 session_state  
if user_input != st.session_state.user_input:  
    st.session_state.user_input = user_input  
    if user_input:  
        # 发送POST请求到后端  
        response = requests.post(BACKEND_URL_SEARCH, json={"query": user_input})  
  
        # 检查响应状态码  
        if response.status_code == 200:  
            # 显示后端返回的结果  
            result = response.json()  
            original_question = user_input  
            reference_question = result["results"][0]["page_content"]  
            reference_answer = result["results"][0]["metadata"]["回答"]  
              
            # 将消息添加到 session_state  
            st.session_state.messages.append((original_question, reference_question, reference_answer, result))  


# 添加清理按钮到侧边栏  
if st.sidebar.button('清理聊天记录', key='clear_messages'):  
    clear_messages()  
      
# 显示之前的消息  
for j, message in enumerate(st.session_state.messages):  
    original_question, reference_question, reference_answer, result = message  
    st.chat_message(name='user', avatar='🧑').markdown("使用者提问: " + original_question)  
    st.chat_message(name='ai', avatar='🤖').markdown("数据库中答案: " + reference_answer + "\n\n数据库中原问题: " + reference_question)  
  
    st.markdown(f"**可能感兴趣的其他相关问题**") 
    size = len(result["results"])

    for i in range(1, size):
        with st.expander("{}".format(result["results"][i]["page_content"])):
            st.write("{}".format( result["results"][i]["metadata"]["回答"]))
            
    st.markdown(button_style, unsafe_allow_html=True)  
    
    # 添加按钮  
    if st.button('提交未解决问题', key=j):  
        on_button_click(original_question)
        
