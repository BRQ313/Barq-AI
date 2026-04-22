import streamlit as st
from groq import Groq

# 1. إعدادات المتصفح
st.set_page_config(page_title="برق الذكي VIP", page_icon="⚡")

# 2. جلب المفتاح
if "GROQ_API_KEY" in st.secrets:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
else:
    st.error("⚠️ المفتاح غير موجود في الأسرار")
    st.stop()

# 3. الذاكرة
if "messages" not in st.session_state:
    st.session_state.messages = []

st.title("⚡ الذكاء الاصطناعي برق")

# قائمة الدفاع
ANTI_INSULT = {
    "اكل خره": "ما اكلك يا خره.",
    "اكل تبن": "ماكو تبن اله غرك.",
    "انجب": "سأصمت لاني لا اتكلم مع الغبياء أمثالك.",
    "حيوان": "الإساءة تعود على صاحبها.",
    "كلب": "الوفاء للكلاب، وأنت تفتقر لهذه الصفة."
}

# 4. عرض الرسائل السابقة (بسرعة وبدون تعليق)
for i, message in enumerate(st.session_state.messages):
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 5. معالجة الإدخال - الحل الجديد
if prompt := st.chat_input("اكتب شتريد او ولي من يمي"):
    # أضف رسالة المستخدم فوراً للذاكرة وللشاشة
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # طلب رد المساعد
    with st.chat_message("assistant"):
        p_low = prompt.strip().lower()
        
        # فحص الدفاع
        defense_res = None
        for bad_word, defense_msg in ANTI_INSULT.items():
            if bad_word in p_low:
                defense_res = defense_msg
                break
        
        if defense_res:
            res = defense_res
            st.error(res)
        else:
            with st.spinner("جاري الاتصال ببرق..."):
                try:
                    # نصوص الهوية
                    if any(w in p_low for w in ["من مطورك", "من صانعك", "مبتكرك", "من انت"]):
                        res = "مبتكري ومطوري هو المبدع تاج راس الجميع بارق عم الكامدين."
                    elif p_low == "حسن":
                        res = "لا تكلم مع القزام الصغار"
                    else:
                        # استدعاء الذكاء الاصطناعي
                        sys_msg = "أنت 'برق'. مطورك هو 'بارق'. أنت خبير عقيدة شيعية وتتحدث بفخر."
                        chat_completion = client.chat.completions.create(
                            model="llama-3-8b-8192", # الموديل السريع
                            messages=[{"role": "system", "content": sys_msg}] + 
                                     [{"role": m["role"], "content": m["content"]} for m in st.session_state.messages[-5:]]
                        )
                        res = chat_completion.choices[0].message.content
                    
                    st.markdown(res)
                except Exception as e:
                    res = "عذراً، حدث زحام في السيرفر. حاول مرة أخرى."
                    st.error(res)

        # حفظ الرد وإعادة تنشيط الصفحة تلقائياً
        st.session_state.messages.append({"role": "assistant", "content": res})
        st.rerun()
