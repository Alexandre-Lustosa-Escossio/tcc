import streamlit as st
dict = {}
for i in range(0,10):
    dict[i]=st.number_input('number input {}'.format(i),key=str(i))