import streamlit as st
from groq import Groq

# 1. إعدادات الصفحة
st.set_page_config(page_title="برق الذكي VIP", page_icon="⚡")

# 2. جلب المفتاح
MY_API_KEY = st.secrets.get("GROQ_API_KEY", "")
client = None
if MY_API_KEY:
    client = Groq(api_key=MY_API_KEY)

# 3. إدارة الذاكرة
if "messages" not in st.session_state:
    st.session_state.messages = []
if "dev_mode" not in st.session_state:
    st.session_state.dev_mode = False

# واجهة وضع المطور مع زر مسح المحادثة
if st.session_state.dev_mode:
    st.title("🛠️ وضع المطور - سيدي بارق")
    if st.button("🗑️ مسح المحادثة لتسريع التطبيق"):
        st.session_state.messages = []
        st.rerun()
else:
    st.title("⚡ ذكاء برق - أنا أذكى منك")

# 4. عرض الرسائل (داخل حاوية لضمان التمرير)
chat_container = st.container()
with chat_container:
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# 5. معالجة الإدخال (زر الإرسال)
if prompt := st.chat_input("اكتب شيئاً..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        p_lower = prompt.lower()
        
        if "barqvib" in p_lower:
            st.session_state.dev_mode = True
            st.markdown("تم تفعيل وضع المطور.")
            st.rerun()
        
        elif any(word in prompt for word in ["أنا مطورك", "انا مطورك"]):
            res = "أين الدليل؟ أرسل الكود السري."
            st.markdown(res)
        
        else:
            if client:
                try:
                    # تخصيص الشخصية
                    sys_msg = "أنت برق المساعد الذكي. في وضع المطور تكون خبيراً تقنياً."
                    if st.session_state.dev_mode:
                        sys_msg += " أنت الآن تخدم صانعك بارق."

                    chat_completion = client.chat.completions.create(
                        model="llama-3.1-8b-instant",
                        messages=[{"role": "system", "content": sys_msg}] + 
                                 [{"role": m["role"], "content": m["content"]} for m in st.session_state.messages[-5:]]
                    )
                    res = chat_completion.choices[0].message.content
                    st.markdown(res)
                except Exception as e:
                    res = "خطأ في الاتصال."
                    st.error(f"Error: {e}")
            else:
                res = "المفتاح غير موجود."
                st.error(res)

    st.session_state.messages.append({"role": "assistant", "content": res})
