import streamlit as st
from groq import Groq

# إعداد بسيط جداً
st.title("⚡ برق")

# التأكد من المفتاح
if "GROQ_API_KEY" not in st.secrets:
    st.error("أضف المفتاح في Secrets أولاً!")
    st.stop()

client = Groq(api_key=st.secrets["GROQ_API_KEY"])

if "messages" not in st.session_state:
    st.session_state.messages = []

# عرض المحادثة
for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.write(m["content"])

# منطقة الإرسال
prompt = st.chat_input("اكتب شيئاً...")

if prompt:
    # 1. إظهار رسالة المستخدم
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    # 2. جلب رد البوت
    with st.chat_message("assistant"):
        try:
            response = client.chat.completions.create(
                model="llama3-8b-8192",
                messages=[{"role": "user", "content": prompt}]
            )
            answer = response.choices[0].message.content
            st.write(answer)
            st.session_state.messages.append({"role": "assistant", "content": answer})
        except Exception as e:
            st.error(f"عذراً، حدث خطأ: {e}")
