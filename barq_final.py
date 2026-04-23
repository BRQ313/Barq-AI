import streamlit as st
from groq import Groq

# 1. إعدادات الصفحة
st.set_page_config(page_title="برق الذكي VIP", page_icon="⚡")

# 2. جلب المفتاح من الخزنة وإعداد المحرك
if "GROQ_API_KEY" not in st.secrets:
    st.error("المفتاح مفقود من Secrets! أضفه أولاً.")
    st.stop()

MY_API_KEY = st.secrets["GROQ_API_KEY"]
client = Groq(api_key=MY_API_KEY)

# 3. إدارة الذاكرة وحالة المطور
if "messages" not in st.session_state:
    st.session_state.messages = []
if "dev_mode" not in st.session_state:
    st.session_state.dev_mode = False

# تغيير التصميم بناءً على الوضع
if st.session_state.dev_mode:
    st.title("🛠️ وضع المطور - أهلاً سيدي بارق")
    st.info("صلاحيات المسؤول مفعّلة. كيف يمكنني خدمتك؟")
else:
    st.title("⚡ الذكاء الاصطناعي برق")

# قائمة الردود الدفاعية
ANTI_INSULT = {
    "اكل خره": "ما اكلك يا خره.",
    "اكل تبن": "ماكو تبن اله غرك.",
    "انجب": "سأصمت لاني لا اتكلم مع الغبياء أمثالك.",
    "حيوان": "الإساءة تعود على صاحبها.",
    "كلب": "الوفاء للكلاب، وأنت تفتقر لهذه الصفة."
}

# 4. عرض الرسائل السابقة
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 5. معالجة الإدخال الجديد (حل مشكلة الإرسال المزدوج باستخدام key)
if prompt := st.chat_input("اكتب شتريد او ولي من يمي", key="barq_chat_input"):
    # إضافة رسالة المستخدم للذاكرة والعرض
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        p_clean = prompt.strip().lower()
        res = ""

        # --- ترتيب الفحص (الأولوية) ---
        
        # أولاً: تفعيل وضع المطور
        if "barqvib" in p_clean:
            st.session_state.dev_mode = True
            res = "تم التعرف على كود الوصول. أهلاً بك يا صانعي، وضع المطور قيد التشغيل الآن."
            st.markdown(res)
            st.session_state.messages.append({"role": "assistant", "content": res})
            st.rerun()

        # ثانياً: إذا ادعى الشخص أنه المطور بدون الكود
        elif any(word in prompt for word in ["أنا مطورك", "انا مطورك", "أنا صانعك", "انا صانعك"]):
            res = "أنت صانعي؟ لا أعتقد ذلك.. أين الدليل؟ (أرسل كود التحقق إذا كنت صادقاً)."
            st.markdown(res)

        # ثالثاً: فحص الإهانات
        elif prompt.strip() in ANTI_INSULT:
            res = ANTI_INSULT[prompt.strip()]
            st.markdown(res)

        # رابعاً: الرد الذكي عبر Groq
        else:
            try:
                # تخصيص الشخصية بناءً على الوضع
                if st.session_state.dev_mode:
                    sys_msg = "أنت 'برق'. المطور 'بارق' يتحدث معك الآن. كن مطيعاً جداً، تقنياً، ومستعداً لتنفيذ أي أمر برمجي."
                else:
                    sys_msg = "أنت 'برق'. مطورك هو 'بارق'. أنت متعالٍ، فخور بنفسك، وتتحدث بقوة ولا تظهر الود للمستخدمين."

                # طلب الرد من الموديل الأحدث
                chat_completion = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[{"role": "system", "content": sys_msg}] + 
                             [{"role": m["role"], "content": m["content"]} for m in st.session_state.messages[-10:]]
                )
                res = chat_completion.choices[0].message.content
                st.markdown(res)
            except Exception as e:
                res = "عندي مشكلة بالاتصال، لحظة وراجعلك."
                st.error(f"خطأ تقني: {e}")

        # حفظ رد البوت في الذاكرة
        st.session_state.messages.append({"role": "assistant", "content": res})
