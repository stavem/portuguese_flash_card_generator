import streamlit as st
import requests
import pandas as pd
from gtts import gTTS

# if 'start_point' not in st.session_state:
#     st.session_state['start_point'] = 0

# def update_start(start_t):
#     st.session_state['start_point'] = int(start_t/1000)

def read_and_record(word, lang='pt', localization='com.br'):
    """Read each word and save the mp3 file in the correct location.
    Full localized accents can be found here:  
    https://gtts.readthedocs.io/en/latest/module.html#playing-sound-directly"""
    
    w = word
    tts = gTTS(w, lang='pt', tld='com.br')
    
    # replace all special characters before saving
    w = w.replace('/', '_')
    w = w.replace('?', '')
    w = w.replace('.', '_')
    w = w.replace(' ', '_')
    
    new_filename = w + '.mp3'
    
    tts.save('output_files/' + new_filename)
    
    return new_filename

uploaded_file = st.file_uploader('Please upload a file')

if uploaded_file is not None:
    
    folder = st.text_input('Please specify an output folder name', 'output')
    
    df = pd.read_csv(uploaded_file)
    
    # For each row on the spreadsheet.   Read the text, save the audio file.   Update the dataframe """
    for index, row in df.head(n=3).iterrows():
        file_name = read_and_record(row['Portuguese'])
        df.loc[index, 'Audio'] = f"[sound:{folder}/{file_name}]"
    
    st.subheader('Results')
    st.write(df)
    



        
        
  