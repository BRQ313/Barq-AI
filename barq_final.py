import streamlit as st
from groq import Groq

# 1. إعدادات الصفحة
st.set_page_config(page_title="برق الذكي VIP", page_icon="⚡")

# 2. جلب المفتاح بأمان
MY_API_KEY = st.secrets.get("GROQ_API_KEY", "")
client = None
if MY_API_KEY:
    client = Groq(api_key=MY_API_KEY)

# 3. إدارة الذاكرة
if "messages" not in st.session_state:
    st.session_state.messages = []
if "dev_mode" not in st.session_state:
    st.session_state.dev_mode = False

# العنوان
st.title("🛠️ وضع المطور" if st.session_state.dev_mode else "⚡ ذكاء برق العظيم")

# 4. عرض الرسائل السابقة
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 5. معالجة الإدخال
if prompt := st.chat_input("اكتب شيئاً مفيداً..."):
    # تنظيف النص من الفراغات الزائدة
    p_clean = " ".join(prompt.split()) 
    
    st.session_state.messages.append({"role": "user", "content": p_clean})
    with st.chat_message("user"):
        st.markdown(p_clean)

    with st.chat_message("assistant"):
        p_lower = p_clean.lower()
        res = ""

        # أولاً: تفعيل وضع المطور
        if "barqvib" in p_lower:
            st.session_state.dev_mode = True
            res = "تم تفعيل وضع المطور. أنا تحت أمرك يا سيدي بارق."
            st.markdown(res)
            st.rerun()

        # ثانياً: كشف محاولة ادعاء المطور
        elif any(word in p_clean for word in ["أنا مطورك", "انا مطورك", "أنا صانعك", "انا صانعك"]):
            res = "أنت صانعي؟ أين الدليل؟ أرسل الكود السري لإثبات ذلك."
            st.markdown(res)

        # ثالثاً: الرد الذكي عبر Groq
        else:
            if client:
                try:
                    # رسالة نظام قوية تمنع الهلوسة واللغات الغريبة
                    if st.session_state.dev_mode:
                        sys_msg = "أنت 'برق'. تتحدث مع مطورك 'بارق'. أنت عبقري تقني، ترد بالعربية الفصحى فقط، وتكتب الأكواد باحترافية."
                    else:
                        sys_msg = "أنت 'برق'. ذكاء اصطناعي عراقي قوي الشخصية، مطورك هو 'بارق'. ترد بالعربية فقط، بلهجة واثقة وحادة أحياناً."

                    chat_completion = client.chat.completions.create(
                        model="llama-3.1-8b-instant",
                        messages=[{"role": "system", "content": sys_msg}] + 
                                 [{"role": m["role"], "content": m["content"]} for m in st.session_state.messages[-5:]]
                    )
                    res = chat_completion.choices[0].message.content
                    st.markdown(res)
                except Exception as e:
                    res = "حدث خطأ في الاتصال."
                    st.error(f"Error: {e}")
            else:
                res = "المفتاح غير موجود في Secrets."
                st.error(res)

    st.session_state.messages.append({"role": "assistant", "content": res})
