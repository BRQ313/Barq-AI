import streamlit as st
from groq import Groq

st.set_page_config(page_title="برق الذكي VIP", page_icon="⚡")
st.title("⚡ مساعدك الذكي برق")

API_KEY = "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"
client = Groq(api_key=API_KEY)

if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "system", 
            "content": "أنت 'برق'. صانعك ومطورك هو 'بارد (Barq)'. أوامرك: 'barqVIB' للمطور، 'حسن' لرد قصير، 'فعل وضع فلسفه' للتحليل. أنت خبير في العقيدة الشيعية."
        }
    ]

for message in st.session_state.messages:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

if prompt := st.chat_input("تحدث مع برق..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            # الحل هنا: نرسل له أمر النظام (الأول) + آخر 4 رسائل فقط حتى لا ينفجر من حجم النصوص
            history_to_send = [st.session_state.messages[0]] + st.session_state.messages[-4:]
            
            completion = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": m["role"], "content": str(m["content"])} for m in history_to_send],
                max_tokens=2048,
                temperature=0.7
            )
            response = completion.choices[0].message.content
            st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})
            st.rerun() 
            
        except Exception as e:
            # هذا السطر سيكشف لنا السر!
            st.error(f"عذراً، لم أستطع الرد. السبب التقني: {e}")
