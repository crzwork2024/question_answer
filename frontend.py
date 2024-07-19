import streamlit as st  
import requests  
import pandas as pd  
from config import BACKEND_URL_SEARCH, BACKEND_URL_FILTER, BACKEND_URL_UPDATE  
from utilities import clear_messages, on_button_click  
  
# 初始化 session_state  
if 'user_input' not in st.session_state:  
    st.session_state.user_input = ''  
if 'messages' not in st.session_state:  
    st.session_state.messages = []  
if 'show_chat_input' not in st.session_state:  
    st.session_state.show_chat_input = True  # 默认显示聊天输入框  
if 'selected_column' not in st.session_state:  
    st.session_state.selected_column = None  
if 'mode' not in st.session_state:  
    st.session_state.mode = 'chat'  # 默认模式为聊天  
if 'user_input_answer' not in st.session_state:  
    st.session_state.user_input_answer = ''  
  
# 设置Streamlit页面的配置  
st.set_page_config(page_title="智能问答系统", page_icon="🚀")  
  
# 在侧边栏顶部加载并显示JPEG照片  
image_path = r'C:\Users\RONGZHEN CHEN\Desktop\Projects\data\CRRC_LOGO.jpeg'  # 替换为你的图片路径  
st.sidebar.image(image_path, use_column_width=True)  
  
# 界面最上面标题  
st.title("智能问答系统")  
  
# 侧边栏按钮  
if st.sidebar.button('清理聊天记录', key='clear_messages'):  
    clear_messages()  
  
# 侧边栏按钮 - 智能问答窗口  
if st.sidebar.button('智能问答窗口', key='chat_button'):  
    st.session_state.show_chat_input = True  
    st.session_state.mode = 'chat'  
    # 如果从过滤模式切换到聊天模式，清除与过滤模式相关的状态  
    if st.session_state.mode != 'chat':  
        st.session_state.pop('df', None)  
        st.session_state.selected_column = None  
        st.session_state.user_input_answer = ''  


def fetch_unanswered_questions():  
    """从后端获取暂未回答的问题并更新session_state"""  
    response = requests.post(BACKEND_URL_FILTER)  
    if response.status_code == 200:  
        result = response.json()  
        st.subheader("暂未回答的问题:")  
        df = pd.DataFrame(result)  
        st.dataframe(df)  
        st.session_state.df = df  
    else:  
        st.error(f"获取暂未回答的问题失败: {response.status_code}")  
          
# 侧边栏按钮 - 查询暂未回答的问题  
if st.sidebar.button('查询暂未回答的问题', key='filter_messages_button'):  
    st.session_state.show_chat_input = False  
    st.session_state.mode = 'filter'  
    fetch_unanswered_questions()  
  

  
# 根据条件显示不同的UI元素  
if st.session_state.mode == 'chat' and st.session_state.show_chat_input:  
    # 聊天模式的代码（这里仅展示框架，具体内容保持不变）  
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
  
        # 添加按钮  
        if st.button('提交未解决问题', key=j):  
            on_button_click(original_question)
  
if st.session_state.mode == 'filter':  
    # 过滤模式的代码（这里仅关注selectbox、text_input和提交答案的逻辑）  
  
    # 显示selectbox让用户选择一个问题  
    if 'df' in st.session_state and not st.session_state.df.empty:  
        selected_column = st.sidebar.selectbox('选取一个问题来回答', st.session_state.df['documents'])  
        if selected_column:  
            st.session_state.selected_column = selected_column  
            st.write("暂未回答问题：", st.session_state.selected_column)  
  
            # 用户输入答案  
            user_input_answer = st.text_input("请输入暂未回答问题的答案：", key='user_input_answer')  
  
            # 提交答案的逻辑  
            if st.button('提交问题答案', key='submit_answer_button'):  
                try:  
                    # 获取选中问题的ID（假设每个问题只有一个ID，且'ids'列存在）  
                    df_temp = pd.DataFrame(st.session_state.df)  
                    id_value = df_temp[df_temp['documents'] == selected_column]['ids'].iloc[0]  
  
                    # 准备提交到后端的JSON数据  
                    js = {'id': id_value, 'page_content': selected_column, 'answer': {'回答': user_input_answer}}  
  
                    # 发送POST请求到后端更新答案  
                    response = requests.post(BACKEND_URL_UPDATE, json=js)  
  
                    # 根据响应状态码显示不同的消息  
                    if response.status_code == 200:  
                        message_part1 = "答案"  
                        message_part2 = f'已成功添加至数据库！'  
                        colored_question = f'<span style="color: green;">{user_input_answer}</span>'  
                        full_message = f'{message_part1} {colored_question}{message_part2}'  
                        st.markdown(full_message, unsafe_allow_html=True)  
                                
                        df_update = st.session_state.df
                        df_update = df_update[df_update['documents'] != selected_column] 
                        st.session_state.df = df_update
                                
                        # 清空输入框答案  
                        # st.session_state.user_input_answer = ''  
  
                    else:  
                        message_part1 = "答案"  
                        message_part2 = f'添加失败，状态码：{response.status_code}，请通知管理员！'  
                        colored_question = f'<span style="color: red;">{user_input_answer}</span>'  
                        full_message = f'{message_part1} {colored_question}{message_part2}'  
                        st.markdown(full_message, unsafe_allow_html=True)  
  
                except requests.RequestException as e:  
                    # 处理请求异常  
                    st.error(f"提交答案时发生错误：{e}")  
                except (IndexError, KeyError) as e:  
                    # 处理DataFrame索引或键错误（例如，如果'ids'列不存在或为空）  
                    st.error(f"处理数据时发生错误：{e}")  
                except Exception as e:  
                    # 处理其他未预料的异常  
                    st.error(f"发生未知错误：{e}")  
  