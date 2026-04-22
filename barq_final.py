import streamlit as st
from groq import Groq

# 1. إعداد الصفحة
st.set_page_config(page_title="برق الذكي VIP", page_icon="⚡")
st.title("⚡ الذكاء الاصطناعي برق")

# 2. جلب المفتاح
if "GROQ_API_KEY" in st.secrets:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
else:
    st.error("⚠️ المفتاح غير موجود في Secrets")
    st.stop()

# قائمة الدفاع
ANTI_INSULT = {
    "اكل خره": "ما اكلك يا خره.",
    "اكل تبن": "ماكو تبن اله غرك.",
    "انجب": "سأصمت لاني لا اتكلم مع الغبياء أمثالك.",
    "حيوان": "الإساءة تعود على صاحبها.",
    "كلب": "الوفاء للكلاب، وأنت تفتقر لهذه الصفة."
}

# تهيئة الرسائل
if "messages" not in st.session_state:
    st.session_state.messages = []

# عرض المحادثة
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# إدخال المستخدم
if prompt := st.chat_input("اكتب شتريد..."):
    # 1. إضافة رسالة المستخدم فوراً
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # 2. معالجة الرد
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
            with st.spinner("برق يحضر الرد..."):
                try:
                    if any(w in p_low for w in ["من مطورك", "من صانعك", "مبتكرك", "من انت"]):
                        res = "مبتكري ومطوري هو المبدع تاج راس الجميع بارق عم الكامدين."
                    elif p_low == "حسن":
                        res = "لا تكلم مع القزام الصغار"
                    else:
                        # إرسال لـ Groq
                        sys_msg = "أنت 'برق'. مطورك هو 'بارق'. أنت خبير عقيدة شيعية."
                        completion = client.chat.completions.create(
                            model="llama-3-8b-8192",
                            messages=[{"role": "system", "content": sys_msg}] + 
                                     [{"role": m["role"], "content": m["content"]} for m in st.session_state.messages[-5:]]
                        )
                        res = completion.choices[0].message.content
                    
                    st.markdown(res)
                except Exception as e:
                    st.error(f"حدث خطأ: {e}")
                    res = "واجهت مشكلة في الاتصال."

        # حفظ الرد
        st.session_state.messages.append({"role": "assistant", "content": res})
        
        # سطر سحري لإجبار الصفحة على التحديث لمرة واحدة فقط
        st.rerun()
