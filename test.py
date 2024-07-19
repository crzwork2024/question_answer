import streamlit as st  
import pandas as pd  
  
# 假设有一个DataFrame  
df = pd.DataFrame({  
    'documents': ['问题1', '问题2', '问题3']  
})  
  
# 在侧边栏中添加一个下拉列表  
option = st.sidebar.selectbox('选取一个问题来回答', df['documents'])  
  
# 根据选择更新状态  
if option:  
    st.session_state.selected_option = option  
  
# 根据状态条件性地渲染内容  
if 'selected_option' in st.session_state:  
    st.write("你选择了：", st.session_state.selected_option)  
    # 这里可以添加更多依赖于选择的代码