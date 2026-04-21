import streamlit as st
from groq import Groq

# 1. إعداد الصفحة
st.set_page_config(page_title="برق الذكي", page_icon="⚡")
st.title("⚡ مساعدك الذكي برق")

# 2. المفتاح والعميل
API_KEY = "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"
client = Groq(api_key=API_KEY)

# 3. تهيئة الذاكرة (Session State) بشكل صحيح
if "messages" not in st.session_state:
    st.session_state.messages = []

# 4. عرض المحادثات المخزنة
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 5. منطق استقبال وإرسال الرسائل
if prompt := st.chat_input("اكتب سؤالك هنا..."):
    # إضافة رسالة المستخدم للذاكرة وعرضها فوراً
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # توليد الرد
    with st.chat_message("assistant"):
        try:
            # نرسل آخر 10 رسائل فقط لضمان السرعة وعدم التعليق
            completion = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages[-10:]],
                max_tokens=1024,
                temperature=0.7
            )
            response = completion.choices[0].message.content
            st.markdown(response)
            
            # حفظ رد المساعد في الذاكرة
            st.session_state.messages.append({"role": "assistant", "content": response})
            
            # --- هذا هو السطر السحري لحل مشكلة الرسالة الواحدة ---
            st.rerun() 

        except Exception as e:
            st.error("حدث خطأ بسيط، حاول إرسال الرسالة مرة أخرى.")
