import streamlit as st
import requests
import pandas as pd
from gtts import gTTS
import os
from googletrans import Translator


def determine_language(language='Portuguese (Brazilian)'):
    """
    Convert the language selected by each user into the appropriate abbreviated version
    for Google Translate
    """

    lang_dict = {
        'Portuguese (Brazilian)' : 'pt',
        'Spanish (Mexican)': 'es',
        }
    
    return lang_dict.get(language)



def read_and_record(word, filepath, lang='pt', localization='com.br'):
    """Read each word and save the mp3 file in the correct location.
    Full localized accents can be found here:  
    https://gtts.readthedocs.io/en/latest/module.html#playing-sound-directly"""
    
    w = word
    tts = gTTS(w, lang='pt', tld='com.br')
    
    # replace all special characters before saving
    w = w.replace('/', '_')
    w = w.replace('?', '')
    w = w.replace('¿','')
    w = w.replace('!', '')
    w = w.replace('.', '_')
    w = w.replace(' ', '_')
    
    new_filename = w + '.mp3'
    
    tts.save(filepath + '/' + new_filename)
    
    return new_filename



def return_translated_text(raw_text, source, destination='en'):
    
    # create a translator object for text translations
    translator = Translator()
    
    
    # return object with translations
    result = translator.translate(raw_text, src = source, dest = destination)
    
    return result
    
    


########

st.title('Create Portuguese Notecards')
st.write('<br>', unsafe_allow_html=True)
########

selected_language = st.selectbox('Which language are you studying?', ('Portuguese (Brazilian)', 'Spanish (Mexican)'))

st.write('You selected:', selected_language)

lang = determine_language(selected_language)

st.write('<br>', unsafe_allow_html=True)


folder = st.text_input('Please specify an output folder name', 'output')
output_filename = st.text_input('Please specify an notecard file name', 'test.csv')
st.write('<br><br>', unsafe_allow_html=True)
uploaded_file = st.file_uploader('Please upload a file')


if uploaded_file is not None:
    
    df = pd.read_csv(uploaded_file)
    
    df.columns = map(str.lower, df.columns)
    
    filepath = 'output_files/' + folder
    isExist = os.path.exists(filepath)
    
    if not isExist:
        os.makedirs(filepath)
        
    # For each row on the spreadsheet.   Read the text, save the audio file.   Update the dataframe """
    for index, row in df.iterrows():
        
        if df.loc[index, 'portuguese'] == 'x':
            st.write(f'Hello, I am translating from English to {selected_language}.')
            translation = return_translated_text(df.loc[index, 'english'], source = 'en', destination = lang)
            df.loc[index, 'portuguese'] = str(translation.text)

        if df.loc[index, 'english'] == 'x':
            st.write(f'I am translating from {selected_language} to English.')
            translation = return_translated_text(df.loc[index, 'portuguese'], source = lang, destination = 'en')
            df.loc[index, 'english'] = str(translation.text)
            
        file_name = read_and_record(df.loc[index, 'portuguese'], filepath)
        df.loc[index, 'audio'] = f"[sound:{file_name}]"
    
    st.subheader('Results')
    st.write(df)
    
    st.write("Saved to filepath: " + filepath)
    
    df.to_csv(filepath + '/' + output_filename, index=False) 

    
    with open(filepath + '/' + output_filename) as f:
        st.download_button('Download CSV', f)
    



        
        
  