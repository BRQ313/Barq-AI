import streamlit as st
from groq import Groq

# 1. إعداد الصفحة
st.set_page_config(page_title="برق الذكي VIP", page_icon="⚡")
st.title("⚡ سيرفر برق الذكي - نظام الدفاع")

# 2. جلب المفتاح بأمان من Secrets (تأكد من إضافته في إعدادات Streamlit Cloud باسم GROQ_API_KEY)
try:
    API_KEY = st.secrets["GROQ_API_KEY"]
except KeyError:
    st.error("⚠️ خطأ: لم يتم العثور على مفتاح API في الإعدادات السرية (Secrets).")
    st.stop()

client = Groq(api_key=API_KEY)

# 3. قائمة التأديب (الأوامر المحلية)
ANTI_INSULT = {
    "اكل خره": "بل أنت من يأكله! تأدب أمام حضرة 'برق' ومطوره 'بارق'.",
    "اكل تبن": "وفر التبن لنفسك يا هذا، أنت تتحدث مع ذكاء اصطناعي صممه العبقري بارق.",
    "انجب": "سأصمت فقط لأن مطوري 'بارق' علمني الترفع عن الصغار أمثالك.",
    "حيوان": "الإساءة تعود على صاحبها، ابحث عن أخلاقك أولاً.",
    "كلب": "الوفاء للكلاب، وأنت تفتقر حتى لهذه الصفة بتطاولك على 'برق'."
}

# تهيئة سجل الرسائل
if "messages" not in st.session_state:
    st.session_state.messages = []

# عرض التاريخ (الرسائل السابقة)
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# منطقة الإدخال
if prompt := st.chat_input("تحدث مع برق..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        p_low = prompt.strip().lower()
        found_defense = False
        
        # --- نظام الدفاع المحلي ---
        for bad_word, defense_res in ANTI_INSULT.items():
            if bad_word in p_low:
                st.error(defense_res)
                st.session_state.messages.append({"role": "assistant", "content": defense_res})
                found_defense = True
                break
        
        # --- الأوامر العامة والهوية ---
        if not found_defense:
            if any(w in p_low for w in ["من مطورك", "من صانعك", "مبتكرك", "من انت"]):
                res = "مبتكري ومطوري وتاج رأسي هو المبدع 'بارق' (Barq)."
                st.markdown(res)
                st.session_state.messages.append({"role": "assistant", "content": res})
            elif p_low == "حسن":
                res = "لا تكلم مع الانقسام الصغار"
                st.markdown(res)
                st.session_state.messages.append({"role": "assistant", "content": res})
            
            # --- طلب السيرفر السحابي ---
            else:
                try:
                    sys_msg = "أنت 'برق'. مطورك هو 'بارق'. أنت خبير عقيدة شيعية. أسلوبك فخم وذكي."
                    
                    completion = client.chat.completions.create(
                        model="llama-3.3-70b-versatile",
                        messages=[{"role": "system", "content": sys_msg}] + 
                                 [{"role": m["role"], "content": m["content"]} for m in st.session_state.messages[-5:]],
                    )
                    res = completion.choices[0].message.content
                    
                    # إنشاء ملف سجل محلي (اختياري للسيرفر)
                    with open("chat_log.txt", "a", encoding="utf-8") as f:
                        f.write(f"User: {prompt}\nBarq: {res}\n---\n")

                    st.markdown(res)
                    st.session_state.messages.append({"role": "assistant", "content": res})
                    
                except Exception as e:
                    if st.session_state.messages:
                        st.session_state.messages.pop()
                    
                    error_str = str(e).lower()
                    if "policy" in error_str or "safety" in error_str:
                        st.error("🚫 عذراً، هذا الكلام محظور من قبل نظام الحماية الخاص بالسيرفر.")
                    else:
                        st.error(f"⚠️ حدث خطأ تقني: {str(e)}")
    
    st.rerun()

# إظهار زر تحميل السجل في نهاية الصفحة إذا كانت هناك محادثة
if st.session_state.messages:
    full_chat = "\n".join([f"{m['role']}: {m['content']}" for m in st.session_state.messages])
    st.download_button("تحميل سجل المحادثة 📄", full_chat, file_name="barq_chat.txt")
