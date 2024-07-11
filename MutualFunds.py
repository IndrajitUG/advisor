import os
import streamlit as st
from PIL import Image


logo_path = "./avendus.png"
logo_url = "https://media.licdn.com/dms/image/D4D0BAQFIdC9CJFGppg/company-logo_200_200/0/1687269247270?e=2147483647&v=beta&t=83wAMv0VQSvsVbvyE7g80oKJJ6MgILP3ExSsIIGT5wg"

if os.path.exists(logo_path):
    logo = Image.open(logo_path)
else:
    logo = logo_url

def create_portfolio(option,risk):
    from openai import OpenAI
    client = OpenAI()
    prompt = f'''
    Create a {option} portfolio for an Indian investor on the basis of the following risk level:
     {risk}
     Explain the reasoning behind selecting a particular {option}
     Include names of the {option} too.
    '''
    messages = [
        {'role':'system','content':'Your an experienced financial advisor.You have knowledge about all of the mutual funds in indian stock exchange.'},
        {'role':'user','content':prompt}
    ]
    response = client.chat.completions.create(
        model = 'gpt-4o',
        messages = messages,
        temperature = 0.5,
        max_tokens = 1024,
        n=1,
    )
    return response.choices[0].message.content

if __name__== "__main__":
    import os 
    from dotenv import load_dotenv, find_dotenv
    load_dotenv(find_dotenv(), override = True)
    st.session_state['portfolio'] = ""

    st.image(logo, width=80)
    st.header("AI Financial Advisor Co-pilot")
    with st.sidebar:
        options = ['Mutual Funds']
        option = st.radio(' Mutual Funds',options,index=0,key="your_option")

        risk_level = ['low','medium','high']
        risk = st.selectbox("Level of risk you are willing to take",risk_level,index=0)

        if st.button("Suggest"):
            st.session_state['portfolio'] = create_portfolio(option, risk)
    
    st.text_area('Suggestions: ',value=st.session_state.portfolio, height = 500)