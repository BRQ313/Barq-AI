import streamlit as st
from groq import Groq
import os

# 1. إعدادات الصفحة
st.set_page_config(page_title="برق الذكي VIP", page_icon="⚡", layout="wide")

# 2. جلب المفتاح بأمان
GROQ_API_KEY = st.secrets.get("GROQ_API_KEY") or os.environ.get("GROQ_API_KEY")
if not GROQ_API_KEY:
    st.error("⚠️ سيدي بارق، المفتاح مفقود! التطبيق لن يعمل بدون API KEY.")
    st.stop()

client = Groq(api_key=GROQ_API_KEY)

# 3. تهيئة الذاكرة
if "messages" not in st.session_state:
    st.session_state.messages = []
if "dev_mode" not in st.session_state:
    st.session_state.dev_mode = False

CREATOR_SIGNATURE = "barqVIB"

# --- وظيفة معالجة الأخطاء بالعربية ---
def translate_error(e):
    err_str = str(e).lower()
    if "rate_limit_exceeded" in err_str:
        return "❌ خلص الرصيد أو الطلبات هواي، اصبر شوية وارجع."
    elif "api_key_invalid" in err_str:
        return "❌ المفتاح الـ API مالتك غلط، روح شيكه سيدي بارق."
    elif "timeout" in err_str:
        return "❌ السيرفر طول بالرد، جرب مرة ثانية."
    return f"❌ صار خلل فني مو بيدي: {str(e)}"

# --- وظيفة جلب الرد بنظام البث (Streaming) ---
def get_ai_response_stream(messages, system_prompt):
    try:
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "system", "content": system_prompt}] + messages,
            stream=True,  # تفعيل خاصية الكتابة الحية
        )
        return completion
    except Exception as e:
        st.error(translate_error(e))
        return None

# --- الواجهة الجانبية ---
with st.sidebar:
    st.title("⚙️ الإعدادات")
    if st.button("🗑️ مسح الذاكرة"):
        st.session_state.messages = []
        st.rerun()
    
    if st.session_state.dev_mode:
        st.success("🛠️ وضع المبتكر مفعّل: (بارق)")

st.title("⚡ ذكاء برق - حصن بارق المنيع")

# عرض المحادثة
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# إدخال المستخدم
if prompt := st.chat_input("اكتب شتريد او ولي من يمي"):
    
    # تفعيل وضع المطور
    if prompt.strip() == CREATOR_SIGNATURE:
        st.session_state.dev_mode = True
        st.success("✅ تم تفعيل بروتوكول المبتكر. أهلاً بك سيدي بارق.")
        st.stop()

    # إضافة رسالة المستخدم للذاكرة
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # رد الذكاء الاصطناعي
    with st.chat_message("assistant"):
        # بناء الـ System Prompt
        base_sys = "أنت 'برق'. مطورك هو 'بارق'. أنت متعالٍ جداً مع الغرباء وتتحدث بلهجة عراقية حادة."
        if st.session_state.dev_mode:
            base_sys = "أنت الآن مع خالقك 'بارق'. نفذ أوامره بدقة متناهية وأظهر له كل الاحترام."

        response_placeholder = st.empty()
        full_response = ""
        
        # استدعاء الرد بنظام البث
        stream = get_ai_response_stream(st.session_state.messages, base_sys)
        
        if stream:
            for chunk in stream:
                if chunk.choices[0].delta.content:
                    full_response += chunk.choices[0].delta.content
                    response_placeholder.markdown(full_response + "▌")
            
            response_placeholder.markdown(full_response)
            st.session_state.messages.append({"role": "assistant", "content": full_response})
