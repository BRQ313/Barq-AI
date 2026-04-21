import streamlit as st
from groq import Groq

# 1. إعداد الصفحة
st.set_page_config(page_title="برق الذكي VIP", page_icon="⚡")
st.title("⚡ سيرفر برق الذكي - نظام الدفاع")

# 2. جلب المفتاح بأمان (يجب وضعه في Streamlit Secrets)
# بدلاً من كتابة المفتاح هنا، ضعه في ملف .streamlit/secrets.toml
if "GROQ_API_KEY" in st.secrets:
    API_KEY = st.secrets["GROQ_API_KEY"]
else:
    # هذا فقط للتجربة المحلية، لا ترفعه على جيت هاب!
    API_KEY = "ضع_مفتاحك_هنا_مؤقتاً"

client = Groq(api_key=API_KEY)

# 3. قائمة التأديب المحلية
ANTI_INSULT = {
    "اكل خره": "تأدب أمام حضرة 'برق' ومطوره 'بارق'.",
    "اكل تبن": "أنت تتحدث مع ذكاء اصطناعي صممه العبقري بارق.",
    "انجب": "سأصمت ترفعاً عن الصغار أمثالك.",
    "حيوان": "الإساءة تعود على صاحبها.",
    "كلب": "الوفاء للكلاب، وأنت تفتقر لهذه الصفة."
}

if "messages" not in st.session_state:
    st.session_state.messages = []

# عرض الرسائل القديمة
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
        
        # نظام الدفاع المحلي
        for bad_word, defense_res in ANTI_INSULT.items():
            if bad_word in p_low:
                st.error(defense_res)
                st.session_state.messages.append({"role": "assistant", "content": defense_res})
                found_defense = True
                break
        
        if not found_defense:
            # الردود الثابتة للهوية
            if any(w in p_low for w in ["من مطورك", "من صانعك", "مبتكرك", "من انت"]):
                res = "مبتكري ومطوري هو المبدع 'بارق' (Barq)."
                st.markdown(res)
                st.session_state.messages.append({"role": "assistant", "content": res})
            else:
                try:
                    sys_msg = "أنت 'برق'. مطورك هو 'بارق'. أنت خبير عقيدة شيعية. أسلوبك فخم وذكي."
                    # نرسل آخر 5 رسائل فقط للحفاظ على الذاكرة والسرعة
                    completion = client.chat.completions.create(
                        model="llama-3.3-70b-versatile",
                        messages=[{"role": "system", "content": sys_msg}] + 
                                 [{"role": m["role"], "content": m["content"]} for m in st.session_state.messages[-5:]],
                    )
                    res = completion.choices[0].message.content
                    st.markdown(res)
                    st.session_state.messages.append({"role": "assistant", "content": res})
                except Exception as e:
                    # هنا نعرف سبب المشكلة الحقيقي
                    error_msg = str(e)
                    if "safety" in error_msg.lower():
                        st.error("🚫 عذراً، هذا المحتوى مرفوض من قبل فلاتر الأمان العالمية.")
                    else:
                        st.error(f"حدث خطأ تقني: {error_msg}")
    
    # تحديث الصفحة بعد انتهاء الرد
    st.rerun()
