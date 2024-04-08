from openai import OpenAI
import streamlit as st
from streamlit_js_eval import streamlit_js_eval


# Setting page title and header
st.set_page_config(page_title="The SEO Works Persona Plotter", page_icon="https://www.seoworks.co.uk/wp-content/themes/seoworks/assets/images/fav.png", layout="wide",initial_sidebar_state="collapsed")


st.image("resources/SeoWorksLogo-Dark.png",width=250)
st.title("PersonaPlotter by The SEO Works")


st.markdown("***PersonaPlotter reveals audience personas with targeted keywords and their most pressing questions.***")

with st.expander("See explanation"):
    st.write("Introducing PersonaPlotter, the innovative tool designed to help you understand and engage with your target audience. If you are a marketer, product developer or content creator, \
             PersonaPlotter is a great source of ideas. The tool analyses a given topic to build out user personas, each brought to life with keywords and questions they might have about your \
             topic of interest. Just enter your topic and go!")

topic = st.text_input("Enter your topic")


client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"]) 

#  client = OpenAI(api_key=api_key) 

if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-3.5-turbo"

if "messages" not in st.session_state:
    st.session_state.messages = []
        
if topic := topic:
    prompt = "You are a categorisation GPT. Your topic is "+"'"+topic+"'. "+"For the "+"'"+topic+"'"+"create 5 user personas. \
    Put these in the first column of a table. Then give me a list of 20 long tail keywords a content write could use to marke articles for the related to the persona you created and the topic"+"'"+topic+"' . Put these in the second column of the table"+". \
    Finally make a numbered list of the most important questions that each of the personas may have on the topic. \
    Put these in the third column of the table. Return the result in a table format "
    
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown("Here is the response, hope its useful!")

    with st.chat_message("assistant"):
        stream = client.chat.completions.create(
            model=st.session_state["openai_model"],
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            stream=True,
        )
        
        response = st.write_stream(stream)

    st.session_state.messages.append({"role": "assistant", "content": response})

