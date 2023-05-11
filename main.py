import streamlit as st 
from translator import *
import pandas as pd
from accuracy import *
from docx import Document
from io import BytesIO
import re


st.title("GOV Contents Translation")

col1, col2 = st.columns(2)

with col1:
   st.image("https://www.developmentaid.org/files/organizationLogos/huzalabs-435178.jpg")

with col2:
   st.image("images/Rwanda Gov.png")

st.image("images/GIZ_HUZALABS_FAIRFORWARD.png")

# with st.sidebar:
#     st.header("Choose an option")
# Add CSS styling to center the element
st.markdown(
    """
    <style>
    .center {
        display: flex;
        justify-content: center;
        align-items: center;
        height: 80px;
        margin: 0 auto;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Add the file uploader element inside a div with the center class
with st.container():
    st.header("Upload your file")
    file_upload = st.file_uploader('', type=['docx', 'txt'])
    

    #save file file
    if file_upload:
        if file_upload.type == 'text/plain': # For txt files
            text = file_upload.read().decode('utf-8')
            st.session_state['text_area'] = text
        else: # For docx files
            with open('data/content.docx', "wb+") as doc_file:
                doc_file.write(file_upload.read())
            #Read the doc file
            doc = Document('data/content.docx')
            paragraphs = []
            for i in range(len(doc.paragraphs)):
                paragraphs.append(doc.paragraphs[i].text)
            st.session_state['text_area'] = "\n".join(paragraphs)

    st.header("Or Paste/Type your Text Here")
    #Paste in your text docs
    st.text_area("", key='text_area', height=10)
   

translate_button, download_button, a, b = st.columns(4)

with translate_button:
    translate_button = st.button("Translate")

def clean_text(text):
    # Remove non-alphabetic characters
    text = re.sub('[^a-zA-Z\s]', '', text)
    # Convert to lowercase
    text = text.lower()
    # Remove extra spaces
    text = re.sub('\s+', ' ', text)
    # Remove leading/trailing spaces
    text = text.strip()
    return text

if translate_button:
    if 'text_area' in st.session_state:
        paragraphs = st.session_state['text_area'].split('\n')
        texts = []
        progress_bar = st.progress(0)
        for i, text in enumerate(paragraphs):
            if text:
                # Clean the text before translating
                cleaned_text = clean_text(text)
                trans_text, accuracy = translate_row(cleaned_text, target_lang='rw', source_lang='en')
                texts.append(trans_text)
            # Update the progress bar
            progress_bar.progress(int((i+1)/len(paragraphs)*100))
        if len(texts) > 0:
            st.text_area("Translation", value='\n'.join(texts), disabled=False, height=20)
            st.session_state['translated_texts'] = texts
    else:
        st.warning("Please upload a file or enter text to translate.")

with download_button:
    download_button = st.button("Download Dataset")
if 'accuracies' not in st.session_state:
    st.session_state['accuracies'] = []
if download_button:
    if 'translated_texts' in st.session_state:
        doc = Document()
        for i, para in enumerate(st.session_state['translated_texts']):
            doc.add_paragraph(para)
            if 'accuracies' in st.session_state and i < len(st.session_state['accuracies']):
                if st.session_state['accuracies'][i] == min(st.session_state['accuracies']):
                    doc.paragraphs[i].style = 'Warning Text' #highlight the lowest accuracy paragraph
        doc_io = BytesIO()
        doc.save(doc_io)
        doc_io.seek(0)
        st.download_button(
            label="Download Translated Docx File",
            data=doc_io.getvalue(),
            file_name="translated_doc.docx",
            mime="application/octet-stream"
        )
    else:
        st.warning("Please translate a text before downloading the file.")
