import streamlit as st
from groq import Groq

# إعدادات الصفحة
st.set_page_config(page_title="برق الذكي", page_icon="⚡")
st.title("⚡ مساعدك الذكي برق")

# تفعيل المحرك
if "GROQ_API_KEY" in st.secrets:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
else:
    st.error("أضف مفتاح السر في الإعدادات أولاً!")
    st.stop()

# إنشاء الذاكرة
if "messages" not in st.session_state:
    st.session_state.messages = []

# عرض المحادثة
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

# منطقة الكتابة
if prompt := st.chat_input():
    # حفظ رسالتك
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)
    
    # طلب الرد
    with st.chat_message("assistant"):
        try:
            response = client.chat.completions.create(
                model="llama3-8b-8192",
                messages=st.session_state.messages
            )
            answer = response.choices[0].message.content
            st.write(answer)
            st.session_state.messages.append({"role": "assistant", "content": answer})
        except Exception as e:
            st.error("تعثر برق قليلاً.. حاول مجدداً")
