import streamlit as st
from groq import Groq

st.set_page_config(page_title="برق الذكي", page_icon="⚡")
st.title("⚡ مساعدك الذكي برق")

# التأكد من وجود مفتاح السر
if "GROQ_API_KEY" in st.secrets:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
else:
    st.error("الرجاء إضافة GROQ_API_KEY في الإعدادات")
    st.stop()

# تهيئة ذاكرة المحادثة إذا كانت فارغة
if "messages" not in st.session_state:
    st.session_state.messages = []

# عرض الرسائل السابقة
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# استقبال رسالة المستخدم
if prompt := st.chat_input("اكتب رسالتك هنا..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # طلب الرد من الذكاء الاصطناعي
    with st.chat_message("assistant"):
        try:
            response = client.chat.completions.create(
                model="llama3-8b-8192",
                messages=[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages],
            )
            full_response = response.choices[0].message.content
            st.markdown(full_response)
            st.session_state.messages.append({"role": "assistant", "content": full_response})
        except Exception as e:
            st.error(f"حدث خطأ: {e}")
