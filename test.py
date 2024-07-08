import streamlit as st  
  
def on_button_click():  
    st.success('操作成功！')  
  
if st.button('点击我'):  
    on_button_click()