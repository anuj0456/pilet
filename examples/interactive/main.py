import os
import streamlit as st
from streamlit_option_menu import option_menu

from static import menu, icons
from utils import Utility


# st.markdown("""
#             <style>
#                 div[data-testid="column"] {
#                     width: fit-content !important;
#                     flex: unset;
#                 }
#                 div[data-testid="column"] * {
#                     width: fit-content !important;
#                 }
#             </style>
#             """, unsafe_allow_html=True)

with st.sidebar:
    selected = option_menu("Main Menu", menu,
                           icons=icons, menu_icon="cast", default_index=0)


if selected == menu[0]:
    option = st.selectbox('Please choose an option below',
                          options=('Convert Code', 'Find Bugs', 'Write Unit Test'))
    if option == 'Convert Code':
        option = st.selectbox('Please choose an option below',
                              options=('Java-2-Python', 'Angular-2-React'))

    if option != 'Convert Code':
        col1, col2, col3 = st.columns([1, 1, 1])

        with col1:
            but1 = st.button('Upload Single File')
        with col2:
            but2 = st.button('Upload Multiple Files')

        if but1:
            uploaded_file = st.file_uploader("Choose a file", type=(["pdf", "docx", "txt", "png", "jpg"]))
            if uploaded_file is not None:
                bytes_data = uploaded_file.getvalue()
                st.write(bytes_data)
        elif but2:
            folder_path = st.text_input('Input folder path')

            # Scan the folder with files.
            file_paths = []
            if os.path.isdir(folder_path):
                for fn in os.listdir(folder_path):
                    fp = f'{folder_path}/{fn}'
                    if os.path.isfile(fp):
                        file_paths.append(fp)
