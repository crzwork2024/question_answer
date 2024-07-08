import streamlit as st  
import requests  
  
# 初始化 session_state  
if 'user_input' not in st.session_state:  
    st.session_state.user_input = ''  
if 'messages' not in st.session_state:  
    st.session_state.messages = []  
  
def on_button_click(original_question):  
    # 拆分消息，并只对original_question部分应用颜色  
    message_part1 = "问题"  
    message_part2 = f'已成功添加至数据库，随后我们将邀请专家前来解答！'  
    colored_question = f'<span style="color: green;">{original_question}</span>'  
    
    # 组合消息并显示  
    full_message = f'{message_part1} {colored_question}{message_part2}'  
    st.markdown(full_message, unsafe_allow_html=True)
    
def clear_messages():  
    # 清空聊天记录  
    st.session_state.messages = []  
      
st.title("智能问答系统")  
  
# 后端API的URL  
BACKEND_URL = "http://127.0.0.1:8000/search/"  
  
# 创建一个聊天输入框  
user_input = st.chat_input("请输入你的问题：")  
  
# 当用户提交问题时，更新 session_state  
if user_input != st.session_state.user_input:  
    st.session_state.user_input = user_input  
    if user_input:  
        # 发送POST请求到后端  
        response = requests.post(BACKEND_URL, json={"query": user_input})  
  
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
  
    size = len(result["results"])

    for i in range(1, size):
        with st.expander("{}".format(result["results"][i]["page_content"])):
            st.write("{}".format( result["results"][i]["metadata"]["回答"]))
            
            
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
    st.markdown(button_style, unsafe_allow_html=True)  
    
    # 添加按钮  
    if st.button('提交未解决问题', key=j):  
        on_button_click(original_question)
        
