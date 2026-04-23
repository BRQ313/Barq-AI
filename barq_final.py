import streamlit as st
from groq import Groq

st.set_page_config(page_title="برق VIP", page_icon="⚡")

# جلب المفتاح - تأكد أنه موجود في Secrets
try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except:
    st.error("المفتاح غير موجود في Secrets!")
    st.stop()

if "messages" not in st.session_state:
    st.session_state.messages = []
if "dev_mode" not in st.session_state:
    st.session_state.dev_mode = False

st.title("🛠️ وضع المطور" if st.session_state.dev_mode else "⚡ ذكاء برق")

# عرض الرسائل
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# الإدخال
if prompt := st.chat_input("اكتب هنا..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        if "barqvib" in prompt.lower():
            st.session_state.dev_mode = True
            res = "تم التفعيل."
            st.rerun()
        else:
            try:
                response = client.chat.completions.create(
                    model="llama-3.1-8b-instant",
                    messages=[{"role": "user", "content": prompt}]
                )
                res = response.choices[0].message.content
                st.markdown(res)
            except Exception as e:
                st.error(f"خطأ: {e}")
                res = "فشل الإرسال."

    st.session_state.messages.append({"role": "assistant", "content": res})
