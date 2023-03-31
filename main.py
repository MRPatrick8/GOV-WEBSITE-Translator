import streamlit as st 
from translator import *
import pandas as pd
from accuracy import *


st.title("GOV Website Contents Translation")


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
    st.markdown('<div class="center">', unsafe_allow_html=True)
    file_upload = st.file_uploader('Upload CSV file', type=['csv'])
    st.markdown('</div>', unsafe_allow_html=True)

# file_upload = st.file_uploader('Upload CSV file', type=['csv', 'html'])


def process_upload(df):
    with st.spinner("Translating ......."):
        df['translated_text']=translate_dataframe(df, target_lang='rw', source_lang='en')
        df['Back_translated_text']=back_translate_dataframe(df, target_lang='en', source_lang='rw')

    return df

def calc_accuracy(df):
    # Iterate over the DataFrame rows and compare the paragraphs in each row
    for i, row in df.iterrows():
        similarity = compare_paragraphs(row['content'], row['Back_translated_text'])
        df.at[i, 'Condidence level'] = similarity
    return df[['content','translated_text','Condidence level']]


# Print the updated dataframe
if file_upload:
    if st.button('Translate'):
        #Save the csv file
        with open('data/dataset.csv', 'wb+') as file:
            file.write(file_upload.read())
        
        df = pd.read_csv('data/dataset.csv')
        df = process_upload(df)

        st.header("Displaying the confidence level of the translation")
        df = calc_accuracy(df)

        st.dataframe(df)

        #Save the output
        df.to_csv('output.csv')
        @st.cache_data
        def convert_df(df):
            # IMPORTANT: Cache the conversion to prevent computation on every rerun
            return df.to_csv().encode('utf-8')

        csv = convert_df(df)

        st.download_button(label="Download a CSV",file_name='output.csv',data=csv, mime='text/csv')





        



