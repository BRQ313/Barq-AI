import streamlit as st
from groq import Groq

# 1. إعداد الصفحة
st.set_page_config(page_title="برق الذكي", page_icon="⚡")

st.title("⚡ مساعدك الذكي برق")

# 2. المفتاح المباشر
API_KEY = "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"
client = Groq(api_key=API_KEY)

# 3. إدارة الذاكرة بشكل احترافي (هذا هو السر!)
if "messages" not in st.session_state:
    st.session_state.messages = []

# عرض المحادثات السابقة
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 4. منطقة الكتابة
if prompt := st.chat_input("اكتب سؤالك هنا..."):
    # إضافة رسالتك وعرضها فوراً
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # طلب الرد من الموديل
    with st.chat_message("assistant"):
        try:
            # نرسل آخر 5 رسائل فقط لتجنب الثقل (حتى لا يعلق)
            recent_messages = st.session_state.messages[-5:]
            
            completion = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": m["role"], "content": m["content"]} for m in recent_messages],
                max_tokens=1024,
                temperature=0.7
            )
            
            response = completion.choices[0].message.content
            st.markdown(response)
            
            # حفظ الرد في الذاكرة
            st.session_state.messages.append({"role": "assistant", "content": response})
            
            # حركة ذكية: إعادة تشغيل الصفحة برمجياً لضمان جاهزية الرسالة التالية
            st.rerun()
            
        except Exception as e:
            st.error("أنا معك، أرسل رسالتك مرة أخرى.")
