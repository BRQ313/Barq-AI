import streamlit as st
from groq import Groq
import base64
import os
import io

# 1. إعدادات الصفحة (أضفنا معالجة أسرع)
st.set_page_config(page_title="برق الذكي VIP", page_icon="⚡", layout="wide")

# 2. التأكد من وجود المفاتيح (أفضل ممارسة للسيرفرات)
GROQ_API_KEY = st.secrets.get("GROQ_API_KEY") or os.environ.get("GROQ_API_KEY")

if not GROQ_API_KEY:
    st.error("⚠️ خطأ: مفتاح GROQ_API_KEY غير موجود في الإعدادات.")
    st.stop()

client = Groq(api_key=GROQ_API_KEY)

# 3. تهيئة الذاكرة
if "messages" not in st.session_state:
    st.session_state.messages = []
if "dev_mode" not in st.session_state:
    st.session_state.dev_mode = False

# --- تحسين: دالة لإرسال الطلب مع معالجة الأخطاء (Retry Logic) ---
def get_ai_response(messages, system_prompt):
    try:
        chat_completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "system", "content": system_prompt}] + messages,
            timeout=25.0  # تجنب تعليق السيرفر
        )
        return chat_completion.choices[0].message.content
    except Exception as e:
        return   ما بيه حيل ارد اعليك ولي من يمي: {str(e)}"

# --- واجهة المستخدم (مبسطة لتسريع الأداء) ---
st.title("⚡ VIB ذكاء برق - نسخة Serverless")

# عرض المحادثة
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# منطقة الإدخال
if prompt := st.chat_input("اكتب شتريد او ولي من يمي"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("برق يفكر..."):
            # تحديد شخصية الذكاء الاصطناعي
            system_msg = "أنت 'برق'. مطورك هو 'بارق'. أنت ذكي جداً وردودك حاسمة."
            
            # جلب الرد
            # نرسل آخر 5 رسائل فقط لتوفير الذاكرة وسرعة الرد
            response = get_ai_response(st.session_state.messages[-5:], system_msg)
            st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})
