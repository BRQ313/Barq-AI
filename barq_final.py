import streamlit as st
from groq import Groq

# 1. إعداد الصفحة
st.set_page_config(page_title="برق الذكي", page_icon="⚡")
st.title("⚡ مساعدك الذكي برق")

# 2. المفتاح والعميل
API_KEY = "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"
client = Groq(api_key=API_KEY)

# 3. تهيئة الذاكرة
if "messages" not in st.session_state:
    # --- هنا نضع الأوامر التي طلبتها (التعليمات الـ VIP) ---
    st.session_state.messages = [
        {"role": "system", "content": "أنت الآن 'برق VIP'، مساعد ذكي جداً، وسريع الرد، وتتحدث بأسلوب مهذب ومميز. أنت لست مجرد برنامج، بل أنت صديق ذكي ومبتكر."}
    ]

# 4. عرض المحادثات (تخطي رسالة النظام من العرض)
for message in st.session_state.messages:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# 5. منطق المحادثة
if prompt := st.chat_input("اكتب سؤالك هنا..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            completion = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages],
                max_tokens=1024,
                temperature=0.8 # لجعل شخصيته ممتعة أكثر
            )
            response = completion.choices[0].message.content
            st.markdown(response)
            
            st.session_state.messages.append({"role": "assistant", "content": response})
            st.rerun() 

        except Exception as e:
            st.error("حدث خطأ بسيط، حاول مجدداً.")
