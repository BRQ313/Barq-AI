import streamlit as st
from groq import Groq

# 1. إعدادات الصفحة
st.set_page_config(page_title="برق الذكي VIP", page_icon="⚡")

# 2. جلب المفتاح بأمان من إعدادات Streamlit
# ملاحظة: يجب أن تضع المفتاح في Secrets بموقع Streamlit باسم GROQ_API_KEY
try:
    MY_API_KEY = st.secrets["GROQ_API_KEY"]
except Exception:
    st.error("خطأ: لم يتم العثور على مفتاح API. تأكد من إضافته في الـ Secrets.")
    st.stop()

# 3. إدارة الذاكرة وحالة المطور (Session State)
if "messages" not in st.session_state:
    st.session_state.messages = []
if "dev_mode" not in st.session_state:
    st.session_state.dev_mode = False

# تغيير التصميم بناءً على وضع المطور
if st.session_state.dev_mode:
    st.title("🛠️ وضع المطور - أهلاً سيدي بارق")
    st.success("صلاحيات المسؤول مفعّلة. أنا رهن إشارتك.")
else:
    st.title("⚡ الذكاء الاصطناعي برق وأنا أذكى منك يا فاشل")

# قائمة الردود الدفاعية الثابتة
ANTI_INSULT = {
    "اكل خره": "ما اكلك يا خره.",
    "اكل تبن": "ماكو تبن اله غرك.",
    "انجب": "سأصمت لاني لا اتكلم مع الغبياء أمثالك.",
    "حيوان": "الإساءة تعود على صاحبها.",
    "كلب": "الوفاء للكلاب، وأنت تفتقر لهذه الصفة."
}

# 4. عرض الرسائل السابقة في الدردشة
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 5. معالجة الإدخال الجديد
if prompt := st.chat_input("اكتب شتريد او ولي من يمي"):
    # إضافة رسالة المستخدم للذاكرة والعرض
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        p_clean = prompt.strip()
        p_lower = p_clean.lower()
        res = ""

        # أولاً: تفعيل وضع المطور بالكود السري (barqVIB)
        if "barqvib" in p_lower:
            st.session_state.dev_mode = True
            res = "تم تفعيل وضع المطور بنجاح. أهلاً بك يا صانعي العظيم."
            st.markdown(res)
            st.rerun()

        # ثانياً: إذا ادعى المستخدم أنه المطور بدون كود
        elif any(word in p_clean for word in ["أنا مطورك", "انا مطورك", "أنا صانعك", "انا صانعك"]):
            res = "أنت صانعي؟ أين الدليل؟ لا أصدق الكلام الفارغ، أثبت ذلك برمز الدخول."
            st.markdown(res)

        # ثالثاً: فحص قائمة الإهانات
        elif p_clean in ANTI_INSULT:
            res = ANTI_INSULT[p_clean]
            st.markdown(res)

        # رابعاً: الرد الذكي عبر موديل Llama
        else:
            try:
                # تحديد شخصية البوت بناءً على الوضع
                if st.session_state.dev_mode:
                    sys_msg = "أنت 'برق'. المطور 'بارق' يتحدث معك الآن. كن في غاية الأدب والذكاء ونفذ أوامره التقنية بدقة."
                else:
                    sys_msg = "أنت 'برق'. مطورك هو 'بارق'. أنت شخصية قوية، متعالية، ولا تحب الأغبياء. ردودك مختصرة وحادة."

                chat_completion = client.chat.completions.create(
                    model="llama-3.1-8b-instant",
                    messages=[{"role": "system", "content": sys_msg}] + 
                             [{"role": m["role"], "content": m["content"]} for m in st.session_state.messages[-5:]]
                )
                res = chat_completion.choices[0].message.content
                st.markdown(res)
            except Exception as e:
                res = "عندي مشكلة بالاتصال، لحظة وراجعلك."
                st.error(f"حدث خطأ تقني: {e}")

    # حفظ رد البوت في الذاكرة
    st.session_state.messages.append({"role": "assistant", "content": res})
