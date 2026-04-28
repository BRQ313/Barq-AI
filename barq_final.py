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

# 3. تهيئة الذاكرة المتطورة
if "messages" not in st.session_state:
    st.session_state.messages = []
if "dev_mode" not in st.session_state:
    st.session_state.dev_mode = False
if "custom_features" not in st.session_state:
    st.session_state.custom_features = [] # هنا تخزن الميزات اللي تضيفها

# --- دالة جلب الرد ---
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

# --- الواجهة ---
st.title("⚡ ذكاء برق - نظام التطوير الذاتي")

# عرض الحالة في الجانب
if st.session_state.dev_mode:
    st.sidebar.success("🛠️ وضع المطور (barqVIB) مفعّل")
    if st.session_state.custom_features:
        st.sidebar.info("الميزات المضافة:\n" + "\n".join(st.session_state.custom_features))

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- منطقة الإدخال والمعالجة ---
if prompt := st.chat_input("اكتب شتريد او ولي من يمي"):
    
    # 1. تفعيل وضع المطور
    if "barqVIB" in prompt:
        st.session_state.dev_mode = True
        st.success("تم تفعيل وضع المطور. تفضل سيدي بارق، ماذا نطور اليوم؟")
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.rerun()

    # 2. إضافة ميزة (فقط إذا كان وضع المطور مفعلاً)
    if st.session_state.dev_mode and "ضيف ميزة" in prompt:
        new_feature = prompt.replace("ضيف ميزة", "").strip()
        st.session_state.custom_features.append(new_feature)
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("assistant"):
            res = f"✅ علم سيدي! تم إضافة الميزة: ({new_feature}) إلى نظامي بنجاح."
            st.markdown(res)
            st.session_state.messages.append({"role": "assistant", "content": res})
        st.rerun()

    # 3. الرد العادي مع دمج الميزات المضافة
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("######جاي ارد اعليك دير بالك تكتب ازياده لا انعل "):
            
            # بناء الـ System Prompt بناءً على الميزات المضافة
            base_sys = "أنت 'برق'. مطورك هو 'بارق'."
            if st.session_state.dev_mode:
                base_sys += " أنت الآن في وضع المطور وتتحدث مع مبتكرك."
            
            # دمج الميزات الجديدة في "عقل" الذكاء الاصطناعي
            if st.session_state.custom_features:
                features_str = " .التزم بالميزات الإضافية التالية التي وضعها لك المطور: " + " و ".join(st.session_state.custom_features)
                base_sys += features_str

            response = get_ai_response(st.session_state.messages, base_sys)
            st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})
