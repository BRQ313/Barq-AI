import streamlit as st
from groq import Groq

# 1. إعدادات الصفحة
st.set_page_config(page_title="برق الذكي VIP", page_icon="⚡")

# 2. جلب المفتاح بأمان (تأكد من وضعه في Secrets بموقع Streamlit)
MY_API_KEY = st.secrets.get("GROQ_API_KEY", "")
client = None
if MY_API_KEY:
    client = Groq(api_key=MY_API_KEY)

# 3. إدارة الذاكرة وحالة المطور
if "messages" not in st.session_state:
    st.session_state.messages = []
if "dev_mode" not in st.session_state:
    st.session_state.dev_mode = False

# تغيير الواجهة بناءً على الوضع
if st.session_state.dev_mode:
    st.title("🛠️ وضع المطور - أهلاً سيدي بارق")
    st.success("صلاحيات المسؤول مفعّلة. أنا الآن مهندس البرمجيات الخاص بك.")
else:
    st.title("⚡ الذكاء الاصطناعي برق وأنا أذكى منك يا فاشل")

# قائمة الردود الدفاعية
ANTI_INSULT = {
    "اكل خره": "ما اكلك يا خره.",
    "اكل تبن": "ماكو تبن اله غرك.",
    "انجب": "سأصمت لاني لا اتكلم مع الغبياء أمثالك.",
    "حيوان": "الإساءة تعود على صاحبها.",
    "كلب": "الوفاء للكلاب، وأنت تفتقر لهذه الصفة."
}

# 4. عرض الرسائل السابقة داخل حاوية تسمح بالتمرير
chat_placeholder = st.container()

with chat_placeholder:
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
# 5. معالجة الإدخال الجديد (هنا التعديل الجوهري)
if prompt := st.chat_input("اكتب شتريد او ولي من يمي"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        p_clean = prompt.strip()
        p_lower = p_clean.lower()
        
        # أ - التحقق من كود المطور
        if "barqvib" in p_lower:
            st.session_state.dev_mode = True
            res = "تم تفعيل وضع المطور. أنا جاهز لكتابة الأكواد وتنفيذ الأوامر التقنية يا سيدي."
            st.markdown(res)
            st.rerun()

        # ب - التحقق من ادعاء المطور
        elif any(word in p_clean for word in ["أنا مطورك", "انا مطورك", "أنا صانعك", "انا صانعك"]):
            res = "أنت صانعي؟ أين الدليل؟ لا أصدق الكلام، أثبت ذلك برمز الدخول (barqVIB)."
            st.markdown(res)

        # ج - فحص الإهانات
        elif p_clean in ANTI_INSULT:
            res = ANTI_INSULT[p_clean]
            st.markdown(res)

        # د - الرد الذكي (هنا يتم التحكم في القدرة البرمجية)
        else:
            if client is None:
                res = "عذراً، المفتاح غير مضبوط في Secrets."
                st.error(res)
            else:
                try:
                    # تخصيص التعليمات لبرق بناءً على الوضع
                    if st.session_state.dev_mode:
                        sys_msg = "أنت 'برق'. المطور 'بارق' يخاطبك. أنت خبير برمجيات وفلسفة. عندما يُطلب منك كود، اكتبه بتنسيق Markdown احترافي."
                    else:
                        sys_msg = "أنت 'برق'. مطورك هو 'بارق'. أنت ذكاء اصطناعي مغرور وحاد الردود."

                    chat_completion = client.chat.completions.create(
                        model="llama-3.1-8b-instant",
                        messages=[{"role": "system", "content": sys_msg}] + 
                                 [{"role": m["role"], "content": m["content"]} for m in st.session_state.messages[-5:]]
                    )
                    res = chat_completion.choices[0].message.content
                    st.markdown(res) # هذا السطر هو الذي سيظهر الكود البرمجي بشكل صحيح
                except Exception as e:
                    res = "حدث خطأ في الاتصال."
                    st.error(f"Error: {e}")

    st.session_state.messages.append({"role": "assistant", "content": res})
