import streamlit as st
from groq import Groq

st.set_page_config(page_title="برق الذكي", page_icon="⚡")
st.title("⚡ مساعدك الذكي برق")

# تفعيل الاتصال
if "GROQ_API_KEY" in st.secrets:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
else:
    st.error("أضف مفتاح السر في الإعدادات!")
    st.stop()

# ذاكرة بسيطة
if "messages" not in st.session_state:
    st.session_state.messages = []

# عرض الرسائل
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# إرسال واستقبال
if prompt := st.chat_input("تحدث مع برق..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            # طلب الرد من الموديل
            completion = client.chat.completions.create(
                model="llama3-8b-8192",
                messages=[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages]
            )
            response = completion.choices[0].message.content
            st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})
        except Exception as e:
            st.error("حدث خطأ بسيط، جرب ترسل مرة ثانية.")
