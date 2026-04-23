import streamlit as st
from groq import Groq

# 1. الإعدادات
st.set_page_config(page_title="برق VIP", page_icon="⚡")

# 2. الربط مع جروق
# نستخدم get لتجنب انهيار التطبيق إذا فقد المفتاح
api_key = st.secrets.get("GROQ_API_KEY", "")

if not api_key:
    st.error("⚠️ خطأ: المفتاح غير موجود في إعدادات Secrets!")
    st.stop()

client = Groq(api_key=api_key)

# 3. الذاكرة
if "messages" not in st.session_state:
    st.session_state.messages = []
if "dev_mode" not in st.session_state:
    st.session_state.dev_mode = False

# الواجهة
st.title("🛠️ وضع المطور" if st.session_state.dev_mode else "⚡ ذكاء برق")

# 4. عرض المحادثة
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 5. معالجة الإرسال
if prompt := st.chat_input("اكتب شيئاً..."):
    # إضافة رسالة المستخدم للذاكرة
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        # التحقق من الأوامر الخاصة أولاً
        if "barqvib" in prompt.lower():
            st.session_state.dev_mode = True
            res = "تم تفعيل وضع المطور بنجاح سيدي بارق."
            st.markdown(res)
            st.rerun()
        
        elif any(word in prompt for word in ["أنا مطورك", "انا مطورك"]):
            res = "أثبت ذلك برمز الدخول أولاً."
            st.markdown(res)
        
        else:
            try:
                # رسالة النظام لضبط اللغة والشخصية
                sys_msg = "أنت برق، مساعد ذكي ترد باللغة العربية فقط. "
                if st.session_state.dev_mode:
                    sys_msg += "أنت الآن في وضع المطور وتتحدث مع صانعك بارق."

                chat_completion = client.chat.completions.create(
                    model="llama-3.1-8b-instant",
                    messages=[{"role": "system", "content": sys_msg}] + 
                             [{"role": m["role"], "content": m["content"]} for m in st.session_state.messages[-5:]]
                )
                res = chat_completion.choices[0].message.content
                st.markdown(res)
            except Exception as e:
                st.error(f"حدث خطأ: {e}")
                res = "عذراً، واجهت مشكلة في الاتصال."

    st.session_state.messages.append({"role": "assistant", "content": res})
