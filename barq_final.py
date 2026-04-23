import streamlit as st
from groq import Groq

st.set_page_config(page_title="برق الذكي", page_icon="⚡")

# التأكد من المفتاح
if "GROQ_API_KEY" not in st.secrets:
    st.error("المفتاح غير موجود في Secrets!")
    st.stop()

client = Groq(api_key=st.secrets["GROQ_API_KEY"])

if "messages" not in st.session_state:
    st.session_state.messages = []

st.title("⚡ ذكاء برق")

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("اكتب شيئاً..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            completion = client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[{"role": "user", "content": prompt}]
            )
            res = completion.choices[0].message.content
            st.markdown(res)
            st.session_state.messages.append({"role": "assistant", "content": res})
        except Exception as e:
            st.error(f"خطأ: {e}")
