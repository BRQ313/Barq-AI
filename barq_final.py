import streamlit as st
from groq import Groq
import os

# 1. إعدادات الصفحة
st.set_page_config(page_title="برق الذكي VIP", page_icon="⚡", layout="wide")

# 2. محاولة جلب المفتاح من النظام أو من واجهة المستخدم
if "api_key" not in st.session_state:
    st.session_state.api_key = os.environ.get("GROQ_API_KEY", "")

# --- واجهة الإعدادات في الجانب ---
with st.sidebar:
    st.title("⚙️ الإعدادات")
    # خانة إدخال المفتاح إذا لم يكن موجوداً
    if not st.session_state.api_key:
        new_key = st.text_input("أدخل مفتاح GROQ API هنا:", type="password")
        if st.button("حفظ المفتاح"):
            st.session_state.api_key = new_key
            st.rerun()
    else:
        st.success("✅ المفتاح متصل")
        if st.button("تغيير المفتاح"):
            st.session_state.api_key = ""
            st.rerun()

    if st.button("🗑️ مسح المحادثة"):
        st.session_state.messages = []
        st.rerun()

# التوقف إذا لم يوجد مفتاح
if not st.session_state.api_key:
    st.warning("⚠️ سيدي بارق، يرجى إدخال مفتاح الـ API في القائمة الجانبية للبدء.")
    st.stop()

client = Groq(api_key=st.session_state.api_key)

# 3. تهيئة الذاكرة
if "messages" not in st.session_state:
    st.session_state.messages = []
if "dev_mode" not in st.session_state:
    st.session_state.dev_mode = False

CREATOR_SIGNATURE = "barqVIB"

# وظيفة جلب الرد
def get_ai_response_stream(messages, system_prompt):
    try:
        return client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "system", "content": system_prompt}] + messages,
            stream=True,
        )
    except Exception as e:
        st.error(f"❌ خطأ: {str(e)}")
        return None

st.title("⚡ ذكاء برق - حصن بارق المنيع")

# عرض الرسائل
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# إدخال المستخدم
if prompt := st.chat_input("اكتب شتريد او ولي من يمي"):
    if prompt.strip() == CREATOR_SIGNATURE:
        st.session_state.dev_mode = True
        st.success("✅ تم تفعيل بروتوكول المبتكر.")
        st.stop()

    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        base_sys = "أنت 'برق'. مطورك هو 'بارق'. تتحدث بلهجة عراقية حادة."
        if st.session_state.dev_mode:
            base_sys = "أنت مع مطورك بارق. كن مطيعاً جداً."

        full_response = ""
        response_placeholder = st.empty()
        
        stream = get_ai_response_stream(st.session_state.messages, base_sys)
        if stream:
            for chunk in stream:
                if chunk.choices[0].delta.content:
                    full_response += chunk.choices[0].delta.content
                    response_placeholder.markdown(full_response + "▌")
            response_placeholder.markdown(full_response)
            st.session_state.messages.append({"role": "assistant", "content": full_response})
