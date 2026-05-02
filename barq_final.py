import streamlit as st
from groq import Groq

# إعداد الصفحة لتجنب مشاكل الريندر
st.set_page_config(page_title="برق AI", page_icon="⚡")

# التأكد من وجود المفتاح في Secrets
if "GROQ_API_KEY" not in st.secrets:
    st.error("المفتاح مفقود! فضلاً أضفه في إعدادات Secrets باسم GROQ_API_KEY")
    st.stop()

client = Groq(api_key=st.secrets["GROQ_API_KEY"])

st.title("⚡ تطبيق برق الذكي")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("تفضل، اسأل برق..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        chat_completion = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="llama3-8b-8192",
        )
        response = chat_completion.choices[0].message.content
        st.markdown(response)
        st.session_state.messages.append({"role": "assistant", "content": response})import streamlit as st
from groq import Groq

# إعداد الصفحة لتجنب مشاكل الريندر
st.set_page_config(page_title="برق AI", page_icon="⚡")

# التأكد من وجود المفتاح في Secrets
if "GROQ_API_KEY" not in st.secrets:
    st.error("المفتاح مفقود! فضلاً أضفه في إعدادات Secrets باسم GROQ_API_KEY")
    st.stop()

client = Groq(api_key=st.secrets["GROQ_API_KEY"])

st.title("⚡ تطبيق برق الذكي")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("تفضل، اسأل برق..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        chat_completion = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="llama3-8b-8192",
        )
        response = chat_completion.choices[0].message.content
        st.markdown(response)
        st.session_state.messages.append({"role": "assistant", "content": response})import streamlit as st
from groq import Groq

# إعداد الصفحة لتجنب مشاكل الريندر
st.set_page_config(page_title="برق AI", page_icon="⚡")

# التأكد من وجود المفتاح في Secrets
if "GROQ_API_KEY" not in st.secrets:
    st.error("المفتاح مفقود! فضلاً أضفه في إعدادات Secrets باسم GROQ_API_KEY")
    st.stop()

client = Groq(api_key=st.secrets["GROQ_API_KEY"])

st.title("⚡ تطبيق برق الذكي")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("تفضل، اسأل برق..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        chat_completion = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="llama3-8b-8192",
        )
        response = chat_completion.choices[0].message.content
        st.markdown(response)
        st.session_state.messages.append({"role": "assistant", "content": response})
