import os
import validators, streamlit as st
from langchain.prompts import PromptTemplate
from langchain_groq import ChatGroq
from langchain.chains.summarize import load_summarize_chain
from langchain_community.document_loaders import YoutubeLoader, UnstructuredURLLoader

## create streamlit app
st.set_page_config(page_title="LangChain: Summarize Text from Youtube or any Website")
st.title("LangChain: Summarize Text from Youtube or any Website")
st.subheader('Summarize URL')

# run streamlit
with st.sidebar:
    groq_api_key = st.text_input("GROQ_API_KEY", value="", type="password")

generic_url = st.text_input("URL", label_visibility="collapsed")

# Gemma Model
llm = ChatGroq(model="Gemma-7b-It", groq_api_key= groq_api_key)

prompt_template = """
Provide a summary if the following content in 500 words:
Content:{text}

"""

prompt = PromptTemplate(template=prompt_template, input_variables=["text"])

if st.button("Summarize the Content"):
    if not groq_api_key.strip() or not generic_url.strip():
        st.error("Please provide the required information")
    elif not validators.url(generic_url):
        st.error("Please enter Valid URL")
        
    else:
        try:
            with st.spinner("Waiting...."):
                if "youtube.com" in generic_url:
                    loader = YoutubeLoader.from_youtube_url(generic_url, add_video_info = True)
                else:
                    loader = UnstructuredURLLoader(urls=[generic_url], ssl_verify = False, headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_5_1) AppleWebKit/537.36 (KHTML, like Gecto) Chrome/116.0.0.0 Safari/537.36"})
                
                docs = loader.load()
                
                # summarization

                chain = load_summarize_chain(llm, chain_type="stuff", prompt = prompt)
                output_summary = chain.run(docs)
                
                st.success(output_summary)
        except Exception as e:
            st.exception(f"Exception: {e}")
                    
    