import streamlit as st
from groq import Groq

st.set_page_config(page_title="برق الذكي", page_icon="⚡")
st.title("⚡ مساعدك الذكي برق")

API_KEY = "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"
client = Groq(api_key=API_KEY)

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("تحدث مع برق..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            # هنا التعديل المهم: استخدمنا الموديل الجديد المتاح حالياً
            completion = client.chat.completions.create(
                model="llama-3.3-70b-versatile", 
                messages=[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages]
            )
            response = completion.choices[0].message.content
            st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})
        except Exception as e:
            st.error(f"حدث خطأ: {e}")
