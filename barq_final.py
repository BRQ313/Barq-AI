import streamlit as st
from groq import Groq

# 1. إعدادات الصفحة (تبسيط تام لتجنب الأخطاء)
st.set_page_config(page_title="برق الذكي", page_icon="⚡")

st.title("⚡ مساعدك الذكي برق")
st.caption("أنا برق، جاهز لمساعدتك!")

# 2. مفتاح الربط
API_KEY = "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"
client = Groq(api_key=API_KEY)

# 3. الذاكرة
if "messages" not in st.session_state:
    st.session_state.messages = []

# 4. عرض المحادثة
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 5. الإرسال والرد
if prompt := st.chat_input("تحدث مع برق..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            completion = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages],
                max_tokens=1024,
                temperature=0.7
            )
            response = completion.choices[0].message.content
            st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})
        except Exception as e:
            st.error(f"حدث خطأ: {e}")
