
import streamlit as st  
import requests  
from config import *  
from utilities import *  
  
# 初始化 session_state  
if 'user_input' not in st.session_state:  
    st.session_state.user_input = ''  
if 'messages' not in st.session_state:  
    st.session_state.messages = []  
if 'show_chat_input' not in st.session_state:  
    st.session_state.show_chat_input = True  # 默认显示聊天输入框  
if 'selected_column' not in st.session_state:  
    st.session_state.selected_column = None 
      
# 设置Streamlit页面的配置，包括标题  
st.set_page_config(page_title="智能问答系统", page_icon="🚀")  
  
# 界面最上面标题  
st.title("智能问答系统")  
  
# 添加清理按钮到侧边栏  
if st.sidebar.button('清理聊天记录', key='clear_messages'):  
    clear_messages()  

#st.write(st.session_state)

# 根据条件显示聊天输入框  
if st.session_state.show_chat_input:  
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
  
    # 显示之前的消息  
    for j, message in enumerate(st.session_state.messages):  
        original_question, reference_question, reference_answer, result = message  
        st.chat_message(name='user', avatar='🧑').markdown("使用者提问: " + original_question)  
        st.chat_message(name='ai', avatar='🤖').markdown("数据库中答案: " + reference_answer + "\n\n数据库中原问题: " + reference_question)  
    
        st.markdown(f"**可能感兴趣的其他相关问题**")  
        size = len(result["results"])  
    
        for i in range(1, size):  
            with st.expander("{}".format(result["results"][i]["page_content"])):  
                st.write("{}".format(result["results"][i]["metadata"]["回答"]))  
    
        st.markdown(button_style, unsafe_allow_html=True)  
    
        # 添加按钮  
        if st.button('提交未解决问题', key=j):  
            on_button_click(original_question)
            

# 添加查询暂未回答的问题按钮  
if st.sidebar.button('查询暂未回答的问题', key='filter_messages'):  
    st.session_state.show_chat_input = False  
    response = requests.post(BACKEND_URL_FILTER)  
    if response.status_code == 200:  
        result = response.json()  
        st.write("暂未回答的问题:")  
        df = pd.DataFrame(result)  
        st.dataframe(df)  
        st.session_state.df = df  # 保存DataFrame到session_state  
  
# 根据session_state中的DataFrame显示selectbox  
if 'df' in st.session_state:  
    selected_column = st.sidebar.selectbox('选取一个问题来回答', st.session_state.df['documents'])  
    if selected_column:  
        st.session_state.selected_column = selected_column  
        st.write("你选择了：", st.session_state.selected_column)
    
        df_temp = pd.DataFrame(st.session_state.df)
        #id = 
        #doc =
        st.dataframe(df_temp)
        #example_db.update_document(ids[0], docs[0])
        
        