import streamlit as st
from groq import Groq

# 1. إعدادات الصفحة - يجب أن تكون في البداية تماماً
st.set_page_config(page_title="برق الذكي VIP", page_icon="⚡")

# 2. جلب المفتاح والأدوات
if "GROQ_API_KEY" in st.secrets:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
else:
    st.error("⚠️ المفتاح غير موجود في الأسرار (Secrets)")
    st.stop()

# 3. تهيئة الذاكرة
if "messages" not in st.session_state:
    st.session_state.messages = []

# قائمة الدفاع
ANTI_INSULT = {
    "اكل خره": "ما اكلك يا خره.",
    "اكل تبن": "ماكو تبن اله غرك.",
    "انجب": "سأصمت لاني لا اتكلم مع الغبياء أمثالك.",
    "حيوان": "الإساءة تعود على صاحبها.",
    "كلب": "الوفاء للكلاب، وأنت تفتقر لهذه الصفة."
}

st.title("⚡ الذكاء الاصطناعي برق")

# 4. عرض المحادثة باستخدام نظام الحاويات لضمان السرعة
chat_container = st.container()
with chat_container:
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# 5. منطقة الإدخال
if prompt := st.chat_input("اكتب شتريد او ولي من يمي"):
    # عرض رسالة المستخدم فوراً
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # معالجة الرد
    with st.chat_message("assistant"):
        p_low = prompt.strip().lower()
        res = ""
        
        # فحص الدفاع
        found_defense = False
        for bad_word, defense_res in ANTI_INSULT.items():
            if bad_word in p_low:
                res = defense_res
                st.error(res)
                found_defense = True
                break
        
        if not found_defense:
            with st.spinner("برق يفكر..."):
                try:
                    if any(w in p_low for w in ["من مطورك", "من صانعك", "مبتكرك", "من انت"]):
                        res = "مبتكري ومطوري هو المبدع تاج راس الجميع بارق عم الكامدين."
                    elif p_low == "حسن":
                        res = "لا تكلم مع القزام الصغار"
                    else:
                        sys_msg = "أنت 'برق'. مطورك هو 'بارق'. أنت خبير عقيدة شيعية وتتحدث بفخر."
                        # نستخدم الموديل السريع جداً لضمان عدم التعليق
                        completion = client.chat.completions.create(
                            model="llama-3-8b-8192",
                            messages=[{"role": "system", "content": sys_msg}] + 
                                     [{"role": m["role"], "content": m["content"]} for m in st.session_state.messages[-5:]]
                        )
                        res = completion.choices[0].message.content
                    
                    st.markdown(res)
                except Exception as e:
                    st.error(f"⚠️ حدث خطأ فني: {e}")
                    res = "واجهت مشكلة، جرب مرة أخرى."

        # حفظ الرد
        st.session_state.messages.append({"role": "assistant", "content": res})
        
        # أهم سطر لحل مشكلة "الضغط المتكرر"
        st.rerun()
