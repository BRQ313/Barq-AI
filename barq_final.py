import streamlit as st
from groq import Groq

# 1. إعدادات المتصفح
st.set_page_config(page_title="برق الذكي VIP", page_icon="⚡")

# 2. بدلاً من كتابة المفتاح يدوياً
MY_API_KEY = st.secrets["GROQ_API_KEY"]
client = Groq(api_key=MY_API_KEY) # هذا هو السطر الناقص الذي يسبب الخطأ
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
    st.title("⚡ الذكاء الاصطناعي برق وأنا أذكى منك يا فاشل")

# قائمة الردود الدفاعية
ANTI_INSULT = {
    "اكل خره": "ما اكلك يا خره.",
    "اكل تبن": "ماكو تبن اله غرك.",
    "انجب": "سأصمت لاني لا اتكلم مع الغبياء أمثالك.",
    "حيوان": "الإساءة تعود على صاحبها.",
    "كلب": "الوفاء للكلاب، وأنت تفتقر لهذه الصفة."
}

# 4. عرض الرسائل
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 5. معالجة الإدخال الجديد
if prompt := st.chat_input("اكتب شتريد او ولي من يمي"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        p_clean = prompt.strip().lower()
        res = ""

        # --- ترتيب الفحص (الأولوية) ---
        
        # أولاً: تفعيل وضع المطور بالكود السري
        if "barqvib" in p_clean:
            st.session_state.dev_mode = True
            res = "تم التعرف على كود الوصول. أهلاً بك يا صانعي، وضع المطور قيد التشغيل الآن."
            st.markdown(res)
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
                # تخصيص الشخصية
                if st.session_state.dev_mode:
                    sys_msg = "أنت 'برق'. المطور 'بارق' يتحدث معك الآن. كن مطيعاً، تقنياً، ومستعداً لتنفيذ أي أمر برمجي."
                else:
                    sys_msg = "أنت 'برق'. مطورك هو 'بارق'. أنت متعالٍ، فخور بنفسك، وتتحدث بقوة (لا تظهر الود للمستخدمين العاديين)."

                chat_completion = client.chat.completions.create(
                    model="llama-3.1-8b-instant",
                    messages=[{"role": "system", "content": sys_msg}] + 
                             [{"role": m["role"], "content": m["content"]} for m in st.session_state.messages[-5:]]
                )
                res = chat_completion.choices[0].message.content
                st.markdown(res)
            except Exception as e:
                res = "عندي مشكلة بالاتصال، لحظة وراجعلك."
                st.error(f"خطأ: {e}")

    # حفظ رد البوت في الذاكرة
    st.session_state.messages.append({"role": "assistant", "content": res})
