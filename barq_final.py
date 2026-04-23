import streamlit as st
from groq import Groq

# 1. إعداد الصفحة
st.set_page_config(page_title="برق الذكي VIP", page_icon="⚡")

# 2. جلب المفتاح بأمان من Secrets
# تأكد أنك وضعت المفتاح في موقع Streamlit باسم GROQ_API_KEY
MY_API_KEY = st.secrets.get("GROQ_API_KEY", "")

client = None
if MY_API_KEY:
    try:
        client = Groq(api_key=MY_API_KEY)
    except:
        client = None

# 3. إدارة الذاكرة
if "messages" not in st.session_state:
    st.session_state.messages = []
if "dev_mode" not in st.session_state:
    st.session_state.dev_mode = False

# واجهة التطبيق
if st.session_state.dev_mode:
    st.title("🛠️ وضع المطور - اهلن سيد بارق")
    st.success("تم تفعيل صلاحيات التحكم الكامل.")
else:
    st.title("⚡ ذكاء برق العظيم")

# 4. عرض الرسائل السابقة
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 5. معالجة الإدخال
if prompt := st.chat_input("اكتب شيئاً لبرق..."):
    # تنظيف النص لضمان عدم وجود فراغات تعيق الإرسال
    user_input = " ".join(prompt.split())
    
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        p_lower = user_input.lower()
        res = ""

        # أولاً: تفعيل وضع المطور
        if "barqvib" in p_lower:
            st.session_state.dev_mode = True
            res = "تم تفعيل وضع المطور بنجاح. أهلاً بك يا صانعي."
            st.markdown(res)
            st.rerun()

        # ثانياً: إذا ادعى المستخدم أنه المطور
        elif any(word in user_input for word in ["أنا مطورك", "انا مبتكرك"]):
            res = "أنت صانعي؟ أثبت ذلك برمز الدخول السري."
            st.markdown(res)

        # ثالثاً: الرد الذكي
        else:
            if client:
                try:
                    # توجيه الموديل للرد بالعربية ومنع اللغات الأخرى
                    if st.session_state.dev_mode:
                        sys_msg = "أنت 'برق'. تتحدث مع مطورك 'بارق'. أنت خبير برمجيات، ترد بالعربية فقط، وتكتب أكواداً احترافية."
                    else:
                        sys_msg = "أنت 'برق'. مطورك هو 'بارق'. أنت ذكاء اصطناعي واثق وحاد، ترد بالعربية فقط."

                    chat_completion = client.chat.completions.create(
                        model="llama-3.1-8b-instant",
                        messages=[{"role": "system", "content": sys_msg}] + 
                                 [{"role": m["role"], "content": m["content"]} for m in st.session_state.messages[-5:]]
                    )
                    res = chat_completion.choices[0].message.content
                    st.markdown(res)
                except Exception as e:
                    res = "خطأ في الاتصال بالسيرفر."
                    st.error(f"Error: {e}")
            else:
                res = "⚠️ المفتاح غير موجود! اذهب إلى إعدادات Streamlit وأضف GROQ_API_KEY."
                st.error(res)

    st.session_state.messages.append({"role": "assistant", "content": res})
