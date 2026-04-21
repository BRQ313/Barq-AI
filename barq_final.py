import streamlit as st
from groq import Groq

# إعداد الصفحة الأساسي
st.set_page_config(page_title="برق الذكي", page_icon="⚡")

st.title("⚡ مساعدك الذكي برق")
st.write("مرحباً بك! أنا برق، كيف يمكنني مساعدتك اليوم؟")

# مفتاح الربط المباشر
API_KEY = "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"
client = Groq(api_key=API_KEY)

# إنشاء الذاكرة إذا لم تكن موجودة
if "messages" not in st.session_state:
    st.session_state.messages = []

# عرض المحادثة السابقة
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# صندوق المحادثة
if prompt := st.chat_input("اكتب سؤالك هنا..."):
    # إضافة رسالتك للذاكرة
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # طلب الرد من الذكاء الاصطناعي
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
            # حفظ الرد في الذاكرة
            st.session_state.messages.append({"role": "assistant", "content": response})
        except Exception as e:
            st.error("حدث ضغط بسيط على الشبكة، يرجى المحاولة مرة أخرى.")
