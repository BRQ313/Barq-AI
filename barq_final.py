import streamlit as st
from groq import Groq

# 1. إعداد الصفحة
st.set_page_config(page_title="برق الذكي VIP", page_icon="⚡")
st.title("⚡ الذكا الصطناعي برق وهو اذكا منك")

# 2. جلب المفتاح
try:
    API_KEY = st.secrets["GROQ_API_KEY"]
    client = Groq(api_key=API_KEY)
except:
    st.error("⚠️ تأكد من وضع المفتاح في Secrets")
    st.stop()

# قائمة الدفاع
ANTI_INSULT = {
    "اكل خره": "ما اكلك يا خره'.",
    "اكل تبن": "ماكو تبن اله غرك.",
    "انجب": "سأصمت لاني لا اتكلم مع الغبياء أمثالك.",
    "حيوان": "الإساءة تعود على صاحبها.",
    "كلب": "الوفاء للكلاب، وأنت تفتقر لهذه الصفة."
}

if "messages" not in st.session_state:
    st.session_state.messages = []

# عرض المحادثة السابقة
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# إدخال المستخدم
if prompt := st.chat_input("اكتب شتريد او ولي من يمي"):
    # عرض رسالة المستخدم فوراً وحفظها
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # معالجة الرد
    with st.chat_message("assistant"):
        p_low = prompt.strip().lower()
        found_defense = False
        
        # 1. فحص الدفاع
        for bad_word, defense_res in ANTI_INSULT.items():
            if bad_word in p_low:
                res = defense_res
                st.error(res)
                found_defense = True
                break
        
        # 2. الإرسال لـ Groq مع "مؤشر انتظار"
        if not found_defense:
            with st.spinner("برق يفكر..."): # هذا سيظهر للمستخدم أن الموقع يعمل
                try:
                    if any(w in p_low for w in ["من مطورك", "من صانعك", "مبتكرك", "من انت"]):
                        res = "مبتكري ومطوري هو المبدع 'تاج راس الجميع هو بارق عم الكامدين' (Barq)."
                    elif p_low == "حسن":
                        res = "لا تكلم مع القزام الصغار"
                    else:
                        sys_msg = "أنت 'برق'. مطورك هو 'بارق'. أنت خبير عقيدة شيعية. أسلوبك فخم وذكي."
                        # نرسل آخر 10 رسائل
                        completion = client.chat.completions.create(
                            model="llama-3.3-70b-versatile",
                            messages=[{"role": "system", "content": sys_msg}] + 
                                     [{"role": m["role"], "content": m["content"]} for m in st.session_state.messages[-10:]]
                        )
                        res = completion.choices[0].message.content
                    
                    st.markdown(res)
                except Exception as e:
                    res = f"⚠️ خطأ فني: {str(e)}"
                    st.error(res)

        # حفظ رد المساعد في السجل
        st.session_state.messages.append({"role": "assistant", "content": res})
