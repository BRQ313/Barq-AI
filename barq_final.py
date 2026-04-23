import streamlit as st
from groq import Groq

# 1. إعداد الصفحة لتعمل بشكل أسرع
st.set_page_config(page_title="برق VIP", page_icon="⚡")

# 2. جلب المفتاح (تأكد من وجوده في Secrets)
api_key = st.secrets.get("GROQ_API_KEY", "")

if not api_key:
    st.error("المفتاح مفقود من Secrets!")
    st.stop()

# تعريف العميل مرة واحدة فقط
@st.cache_resource
def get_client():
    return Groq(api_key=api_key)

client = get_client()

# 3. إدارة الذاكرة
if "messages" not in st.session_state:
    st.session_state.messages = []
if "dev_mode" not in st.session_state:
    st.session_state.dev_mode = False

# واجهة المستخدم
st.title("🛠️ وضع المطور" if st.session_state.dev_mode else "⚡ ذكاء برق")

# 4. عرض المحادثة
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 5. معالجة الإدخال
if prompt := st.chat_input("اكتب شتريد او ولي من يمي"):
    # عرض رسالة المستخدم فوراً
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # توليد رد البوت
    with st.chat_message("assistant"):
        with st.spinner("برق يفكر..."): # هذه العلامة تضمن عدم ضياع الطلب
            p_lower = prompt.strip().lower()
            
            # أوامر خاصة
            if "barqvib" in p_lower:
                st.session_state.dev_mode = True
                res = "تم تفعيل وضع المطور بنجاح سيد بارق."
                st.markdown(res)
                st.session_state.messages.append({"role": "assistant", "content": res})
                st.rerun()
            
            elif any(word in prompt for word in ["أنا مطورك", "انا مطورك"]):
                res = "أين الدليل؟ أرسل الكود السري (barqVIB)."
                st.markdown(res)
            
            else:
                try:
                    # رسالة النظام
                    sys_msg = "أنت برق، مساعد ذكي ترد بالعربية فقط وبلهجة واثقة."
                    if st.session_state.dev_mode:
                        sys_msg = "أنت برق في وضع المطور، خبير برمجيات مطيع لصانعك بارق."

                    # إرسال الطلب مع تحديد الحد الأقصى للكلمات لسرعة الرد
                    completion = client.chat.completions.create(
                        model="llama-3.1-8b-instant",
                        messages=[{"role": "system", "content": sys_msg}] + 
                                 [{"role": m["role"], "content": m["content"]} for m in st.session_state.messages[-5:]],
                        max_tokens=500 
                    )
                    res = completion.choices[0].message.content
                    st.markdown(res)
                except Exception as e:
                    res = "واجهت مشكلة في الاتصال، حاول مرة أخرى."
                    st.error(f"خطأ: {e}")

    # حفظ الرد في الذاكرة
    st.session_state.messages.append({"role": "assistant", "content": res})
