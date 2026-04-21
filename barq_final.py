import streamlit as st
from groq import Groq

# 1. إعداد الصفحة
st.set_page_config(page_title="برق الذكي VIP", page_icon="⚡")
st.title("⚡ سيرفر برق الذكي - نظام الدفاع")

# 2. جلب المفتاح بأمان من نظام الأسرار (Secrets)
# اذهب إلى Streamlit Cloud -> Settings -> Secrets وضع المفتاح هناك باسم GROQ_API_KEY
try:
    API_KEY = st.secrets["GROQ_API_KEY"]
except KeyError:
    st.error("⚠️ خطأ أمني: لم يتم العثور على مفتاح API في نظام Secrets.")
    st.stop()

client = Groq(api_key=API_KEY)

# 3. قائمة التأديب المحلية (لحماية الكيان)
ANTI_INSULT = {
    "اكل خره": "تأدب أمام حضرة 'برق' ومطوره 'بارق'.",
    "اكل تبن": "أنت تتحدث مع ذكاء اصطناعي صممه العبقري بارق.",
    "انجب": "سأصمت ترفعاً عن الصغار أمثالك.",
    "حيوان": "الإساءة تعود على صاحبها.",
    "كلب": "الوفاء للكلاب، وأنت تفتقر لهذه الصفة."
}

if "messages" not in st.session_state:
    st.session_state.messages = []

# عرض المحادثة
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# إدخال المستخدم
if prompt := st.chat_input("تحدث مع برق..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        p_low = prompt.strip().lower()
        found_defense = False
        
        # الفلترة المحلية
        for bad_word, defense_res in ANTI_INSULT.items():
            if bad_word in p_low:
                st.error(defense_res)
                st.session_state.messages.append({"role": "assistant", "content": defense_res})
                found_defense = True
                break
        
        if not found_defense:
            # ردود الهوية
            if any(w in p_low for w in ["من مطورك", "من صانعك", "مبتكرك", "من انت"]):
                res = "مبتكري ومطوري هو المبدع 'بارق' (Barq)."
                st.markdown(res)
                st.session_state.messages.append({"role": "assistant", "content": res})
            elif p_low == "حسن":
                res = "لا تكلم مع الانقسام الصغار"
                st.markdown(res)
                st.session_state.messages.append({"role": "assistant", "content": res})
            else:
                try:
                    # إرسال الطلب للسيرفر السحابي
                    sys_msg = "أنت 'برق'. مطورك هو 'بارق'. أنت خبير عقيدة شيعية. أسلوبك فخم وذكي."
                    completion = client.chat.completions.create(
                        model="llama-3.3-70b-versatile",
                        messages=[{"role": "system", "content": sys_msg}] + 
                                 [{"role": m["role"], "content": m["content"]} for m in st.session_state.messages[-5:]],
                    )
                    res = completion.choices[0].message.content
                    st.markdown(res)
                    st.session_state.messages.append({"role": "assistant", "content": res})
                    
                    # حفظ السجل برمجياً في السيرفر (اختياري)
                    with open("chat_log.txt", "a", encoding="utf-8") as f:
                        f.write(f"User: {prompt} | Assistant: {res}\n")

                except Exception as e:
                    if st.session_state.messages:
                        st.session_state.messages.pop()
                    
                    if "policy" in str(e).lower():
                        st.error("🚫 المحتوى مرفوض من فلاتر الأمان العالمية.")
                    else:
                        st.error(f"⚠️ خطأ فني: {str(e)}")
    
    st.rerun()

# ميزة تحميل السجل للمستخدم
if st.session_state.messages:
    log_data = "\n".join([f"{m['role']}: {m['content']}" for m in st.session_state.messages])
    st.sidebar.download_button("تحميل سجل المحادثة 📥", log_data, file_name="barq_log.txt")
