from openai import OpenAI
import streamlit as st
from streamlit_js_eval import streamlit_js_eval
import time



# Setting page title and header
st.set_page_config(page_title="The SEO Works Persona Plotter", 
                   page_icon="https://www.seoworks.co.uk/wp-content/themes/seoworks/assets/images/fav.png", 
                   layout="wide",initial_sidebar_state="collapsed")

with open( "resources/style.css" ) as css:
	st.markdown( f'<style>{css.read()}</style>' , unsafe_allow_html= True)
	
# custom styling to remove red bar at top
st.markdown("""
<style>
	[data-testid="stDecoration"] {
		display: none;
	}
</style>                
            """,
unsafe_allow_html=True)



col1, col2, col3 = st.columns(3)

with col1:
   st.header("")
   
with col2:
   st.header("")
   st.image("resources/SeoWorksLogo-Dark.png")

with col3:
   st.header("")


st.markdown('<div style="text-align: center; font-size:40px;">PersonaPlotter by The SEO Works</div>', unsafe_allow_html=True)
st.markdown('<div style="text-align: center; font-size:20px;">PersonaPlotter reveals audience personas with targeted keywords and their most pressing questions.</div>', unsafe_allow_html=True)

# Spacers for layout purposes
st.write("#")
# st.header("PersonaPlotter by The SEO Works")
# st.markdown("***PersonaPlotter reveals audience personas with targeted keywords and their most pressing questions.***")

with st.expander("How it works"):
    st.write("Introducing PersonaPlotter, the innovative tool designed to help you understand and engage with your target audience. If you are a marketer, product developer or content creator, \
             PersonaPlotter is a great source of ideas. The tool analyses a given topic to build out user personas, each brought to life with keywords and questions they might have about your \
             topic of interest. Just enter your topic and go!")

topic = st.text_input("Enter your topic", placeholder="Add your topic and press enter")

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"]) 

#  client = OpenAI(api_key=api_key) 

if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-3.5-turbo"

if "messages" not in st.session_state:
    st.session_state.messages = []
        
if topic := topic:
    prompt = "You are a categorisation GPT. The topic you will work with is "+"'"+topic+"'. "+". You will now create a table. In the first column create 5 user persona's for the topic"+"('"+topic+")'"+"\
    .In the second column of the table create a numbered list of 20 long tail keywords each user persona will use for the topic "+"'"+topic+"'. The title of the second column must be 'Search phrases'.\
    In the third column make a numbered list of the most important questions that each of the personas may have on the topic. Return the results in a table format."
    
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.status("Plotting Personas...", expanded = True, state="running") as status:
        time.sleep(1)
        st.write("Not be long..")
        time.sleep(2)
        status.update(label="Done!", state="complete", expanded=False)
    
    with st.chat_message("user"):
        st.markdown("Here are your personas, search phrases and questions.")
    
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

st.divider()
# Spacers for layout purposes
st.write("#")

st.markdown('<div style="text-align: center; font-size:30px;"><strong>About The SEO Works<strong></div>', unsafe_allow_html=True)
with st.container():
   st.write("We are the Digital Growth Experts. As an award-winning provider of digital \
            marketing and websites to leading brands, we've worked for more than a decade \
            with one key goal in mind - to get businesses more customers online. Find out more about us (link to https://www.seoworks.co.uk/)")


