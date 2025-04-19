import streamlit as st

def st_plot_matplotlib(plt):
    st.pyplot(plt.gcf())
    plt.clf()
