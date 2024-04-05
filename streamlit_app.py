from openai import OpenAI
import streamlit as st
from streamlit_js_eval import streamlit_js_eval


# Setting page title and header
st.set_page_config(page_title="The SEO Works category helper", page_icon="https://www.seoworks.co.uk/wp-content/themes/seoworks/assets/images/fav.png", layout="wide",    menu_items={
        'Get Help': 'https://www.seoworks.co.uk',
        'Report a bug': "mailto:james@seoworks.co.uk",
        'About': "Let us know what you think of the app?"
    },initial_sidebar_state="expanded")
st.title("The SEO Works Category Helper")

# Sidebar configuration
st.sidebar.image("https://www.seoworks.co.uk/wp-content/themes/seoworks/assets/logos/Seoworks-Logo-Light.svg")
topic = st.sidebar.text_input("Enter your topic")

with st.sidebar:
    if st.button("Clear output"):
        streamlit_js_eval(js_expressions="parent.window.location.reload()")

#  api_key = st.sidebar.text_input("Enter your api key")

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"]) 

#  client = OpenAI(api_key=api_key) 

if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-3.5-turbo"

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


if topic := topic:
    prompt = "You are a categorisation GPT. Your topic is "+"'"+topic+"'. "+"You will create a 3 column table. For the "+"'"+topic+"'"+"create a list of user personas. \
    Put these in the first column of the table. Then list at 20 keywords related to the persona and the topic. \
          Put these in the second column of the table. Finally make a numbered list of the most important questions that each of the personas may have on the topic. \
          Put these in the third column of the table."
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown("Here is the response....hope its useful!")

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
