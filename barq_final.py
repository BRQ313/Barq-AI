import streamlit as st
from groq import Groq

# 1. إعدادات الصفحة
st.set_page_config(page_title="برق الذكي VIP", page_icon="⚡")

# 2. تعريف العميل (Client) بشكل صحيح ومبكر
# سنحاول جلب المفتاح، وإذا لم نجد مفتاحاً سنستخدم نصاً فارغاً لتجنب انهيار الكود
MY_API_KEY = st.secrets.get("GROQ_API_KEY", "")

if not MY_API_KEY:
    st.error("⚠️ خطأ: مفتاح GROQ_API_KEY غير موجود في إعدادات Secrets!")
    client = None
else:
    client = Groq(api_key=MY_API_KEY)

# 3. إدارة الذاكرة وحالة المطور
if "messages" not in st.session_state:
    st.session_state.messages = []
if "dev_mode" not in st.session_state:
    st.session_state.dev_mode = False

# واجهة المستخدم بناءً على الوضع
if st.session_state.dev_mode:
    st.title("🛠️ وضع المطور - أهلاً سيدي بارق")
    st.success("صلاحيات المسؤول مفعّلة. أنا رهن إشارتك.")
else:
    st.title("⚡ الذكاء الاصطناعي برق وأنا أذكى منك يا فاشل")

# قائمة الردود الثابتة
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

# 5. معالجة الإدخال
if prompt := st.chat_input("اكتب شتريد او ولي من يمي"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        p_clean = prompt.strip()
        p_lower = p_clean.lower()
        res = ""

        # أولاً: تفعيل وضع المطور
        if "barqvib" in p_lower:
            st.session_state.dev_mode = True
            res = "تم تفعيل وضع المطور بنجاح. أهلاً بك يا صانعي."
            st.markdown(res)
            st.rerun()

        # ثانياً: تحدي المطور
        elif any(word in p_clean for word in ["أنا مطورك", "انا مطورك", "أنا صانعك", "انا صانعك"]):
            res = "أنت صانعي؟ أين الدليل؟ لا أصدق الكلام الفارغ، أثبت ذلك برمز الدخول."
            st.markdown(res)

        # ثالثاً: فحص الإهانات
        elif p_clean in ANTI_INSULT:
            res = ANTI_INSULT[p_clean]
            st.markdown(res)

        # رابعاً: الرد الذكي (هنا قمنا بإضافة فحص لـ client)
        else:
            if client is None:
                res = "عذراً، لا يمكنني الرد لأن مفتاح الـ API غير مضبوط بشكل صحيح."
                st.error(res)
            else:
                try:
                    if st.session_state.dev_mode:
                        sys_msg = "أنت 'برق'. المطور 'بارق' يتحدث معك الآن. كن مطيعاً جداً."
                    else:
                        sys_msg = "أنت 'برق'. مطورك هو 'بارق'. أنت متعالٍ ولا تحب الأغبياء."

                    chat_completion = client.chat.completions.create(
                        model="llama-3.1-8b-instant",
                        messages=[{"role": "system", "content": sys_msg}] + 
                                 [{"role": m["role"], "content": m["content"]} for m in st.session_state.messages[-5:]]
                    )
                    res = chat_completion.choices[0].message.content
                    st.markdown(res)
                except Exception as e:
                    res = "عندي مشكلة بالاتصال أو المفتاح، لحظة وراجعلك."
                    st.error(f"خطأ تقني: {e}")

    st.session_state.messages.append({"role": "assistant", "content": res})
