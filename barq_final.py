import streamlit as st
from groq import Groq

# 1. إعداد الصفحة
st.set_page_config(page_title="برق الذكي VIP", page_icon="⚡")
st.title("⚡ سيرفر برق الذكي - نظام الدفاع")

# 2. جلب المفتاح بأمان من نظام الأسرار (Secrets)
# تنبيه: لا تضع المفتاح هنا نصاً! ضعه في إعدادات Streamlit Cloud
try:
    API_KEY = st.secrets["GROQ_API_KEY"]
    client = Groq(api_key=API_KEY)
except KeyError:
    st.error("⚠️ خطأ أمني: لم يتم العثور على مفتاح API. يرجى إضافته في Secrets.")
    st.info("تأكد من إضافة GROQ_API_KEY في إعدادات Streamlit Cloud.")
    st.stop()
except Exception as e:
    st.error(f"⚠️ حدث خطأ أثناء الاتصال: {e}")
    st.stop()

# 3. قائمة التأديب المحلية
ANTI_INSULT = {
    "اكل خره": "تأدب أمام حضرة 'برق' ومطوره 'بارق'.",
    "اكل تبن": "أنت تتحدث مع ذكاء اصطناعي صممه العبقري بارق.",
    "انجب": "سأصمت ترفعاً عن الصغار أمثالك.",
    "حيوان": "الإساءة تعود على صاحبها.",
    "كلب": "الوفاء للكلاب، وأنت تفتقر لهذه الصفة."
}

# تهيئة سجل المحادثة
if "messages" not in st.session_state:
    st.session_state.messages = []

# عرض المحادثة السابقة
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 4. إدخال المستخدم والمعالجة
if prompt := st.chat_input("تحدث مع برق..."):
    # إضافة رسالة المستخدم للسجل والعرض
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        p_low = prompt.strip().lower()
        found_defense = False
        
        # الفلترة المحلية (التأديب)
        for bad_word, defense_res in ANTI_INSULT.items():
            if bad_word in p_low:
                st.error(defense_res)
                res = defense_res
                found_defense = True
                break
        
        if not found_defense:
            # ردود الهوية والردود المخصصة
            if any(w in p_low for w in ["من مطورك", "من صانعك", "مبتكرك", "من انت"]):
                res = "مبتكري ومطوري هو المبدع 'بارق' (Barq)."
                st.markdown(res)
            elif p_low == "حسن":
                res = "لا تكلم مع الانقسام الصغار"
                st.markdown(res)
            else:
                try:
                    # إرسال الطلب لـ Groq
                    sys_msg = "أنت 'برق'. مطورك هو 'بارق'. أنت خبير عقيدة شيعية. أسلوبك فخم وذكي."
                    
                    # نأخذ آخر 5 رسائل فقط للحفاظ على الذاكرة والأداء
                    context_messages = [{"role": "system", "content": sys_msg}] + \
                                       [{"role": m["role"], "content": m["content"]} for m in st.session_state.messages[-5:]]
                    
                    completion = client.chat.completions.create(
                        model="llama-3.3-70b-versatile",
                        messages=context_messages,
                    )
                    res = completion.choices[0].message.content
                    st.markdown(res)
                    
                except Exception as e:
                    res = "عذراً، واجهت مشكلة تقنية في معالجة الرد."
                    if "policy" in str(e).lower():
                        st.error("🚫 المحتوى مرفوض من فلاتر الأمان.")
                    else:
                        st.error(f"⚠️ خطأ فني: {str(e)}")

        # إضافة رد المساعد للسجل
        st.session_state.messages.append({"role": "assistant", "content": res})

    # إعادة التشغيل لتحديث الواجهة (اختياري حسب إصدار Streamlit)
    st.rerun()

# 5. ميزة تحميل السجل في الشريط الجانبي
if st.session_state.messages:
    log_data = "\n".join([f"{m['role']}: {m['content']}" for m in st.session_state.messages])
    st.sidebar.download_button("تحميل سجل المحادثة 📥", log_data, file_name="barq_log.txt")
