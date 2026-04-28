import streamlit as st
from groq import Groq
import os

# 1. إعدادات الصفحة
st.set_page_config(page_title="برق الذكي VIP", page_icon="⚡", layout="wide")

# 2. جلب المفتاح
GROQ_API_KEY = st.secrets.get("GROQ_API_KEY") or os.environ.get("GROQ_API_KEY")
if not GROQ_API_KEY:
    st.error("⚠️ المفتاح مفقود!")
    st.stop()

client = Groq(api_key=GROQ_API_KEY)

# 3. تهيئة الذاكرة المحمية
if "messages" not in st.session_state:
    st.session_state.messages = []
if "dev_mode" not in st.session_state:
    st.session_state.dev_mode = False
if "custom_features" not in st.session_state:
    st.session_state.custom_features = []

# --- طبقة الحماية القصوى ---
# النص الذي بالأسفل هو "بصمة المبتكر"
# لن يتفعل التطبيق كوضع مطور إلا إذا طابق المدخل هذه البصمة بالضبط
CREATOR_SIGNATURE = "barqVIB" 

def get_ai_response(messages, system_prompt):
    try:
        chat_completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "system", "content": system_prompt}] + messages,
            timeout=25.0
        )
        return chat_completion.choices[0].message.content
    except Exception as e:
        return f"❌ مابيه حيل ارد اعليك ولي من يمي: {str(e)}"

st.title("⚡ VIB ذكاء برق - نسخة ")

# عرض الحالة للمبتكر فقط
if st.session_state.dev_mode:
    st.sidebar.markdown("### 🛠️ وضع المبتكر مفعّل")
    st.sidebar.info("لا يمكن لأحد غيرك تعديل المنطق الآن.")

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("اكتب شتريد او ولي من يمي"):
    
    # حماية وضع المطور: لن يخبر أحداً أنه تفعّل إلا إذا كانت البصمة صحيحة
    if prompt.strip() == CREATOR_SIGNATURE:
        st.session_state.dev_mode = True
        st.success("تم تفعيل بروتوكول المبتكر. الأوامر البرمجية متاحة لك الآن.")
        st.rerun()

    # محاولة إضافة ميزة من شخص غريب
    if "ضيف ميزة" in prompt:
        if not st.session_state.dev_mode:
            # رد قاسي للغرباء الذين يحاولون التطوير
            with st.chat_message("assistant"):
                res = "##### ققتحلم اطورني! أنت لست بارق، ولا تملك صلاحية الوصول إلى شفرتي البرمجية.  ولي من يمي احسلك لا اعنعل !"
                st.error(res)
                st.session_state.messages.append({"role": "user", "content": prompt})
                st.session_state.messages.append({"role": "assistant", "content": res})
                st.stop()
        else:
            # تنفيذ الأمر للمبتكر فقط
            new_feature = prompt.replace("ضيف ميزة", "").strip()
            st.session_state.custom_features.append(new_feature)
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("assistant"):
                st.success(f"✅ أبشر سيدي بارق، تم دمج الميزة الجديدة: ({new_feature})")
            st.rerun()

    # الرد العادي
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("برق يراجع صلاحيات المستخدم..."):
            base_sys = "أنت 'برق'. مطورك هو 'بارق'. أنت متعالٍ جداً مع الغرباء."
            if st.session_state.dev_mode:
                base_sys = "أنت الآن مع خالقك 'بارق'. نفذ أوامره بدقة وذكاء."
            
            if st.session_state.custom_features:
                base_sys += " .التزم بالميزات التي أضافها مطورك: " + " و ".join(st.session_state.custom_features)

            response = get_ai_response(st.session_state.messages, base_sys)
            st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})
