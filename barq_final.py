import streamlit as st
from groq import Groq
import base64
import os
from datetime import datetime
import io

# 1. إعدادات الصفحة
st.set_page_config(page_title="برق الذكي VIP", page_icon="⚡", layout="wide")

# 2. إعداد الاتصال بـ Groq
if "GROQ_API_KEY" not in st.secrets:
    st.error("المفتاح مفقود! أضفه في Secrets.")
    st.stop()

client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# حساب المبتكر
CREATOR_ACCOUNT = "BRQ313"

# 3. تهيئة الذاكرة (Session State)
if "messages" not in st.session_state:
    st.session_state.messages = []
if "dev_mode" not in st.session_state:
    st.session_state.dev_mode = False
if "custom_rules" not in st.session_state:
    st.session_state.custom_rules = "" 
if "uploaded_images" not in st.session_state:
    st.session_state.uploaded_images = []
if "audio_data" not in st.session_state:
    st.session_state.audio_data = None

# 4. واجهة المستخدم
if st.session_state.dev_mode:
    st.title("🛠️ نظام التطوير الذاتي - أهلاً سيدي بارق")
    st.sidebar.success("✅ وضع المطور مفعّل")
else:
    st.title("⚡ ذكاء برق الاصطناعي")

# عرض الرسائل السابقة
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        if "image_data" in message:
            st.image(message["image_data"], caption="الصورة المرفوعة", use_container_width=True)
        if "audio_data" in message:
            st.audio(message["audio_data"], format="audio/wav")
        st.markdown(message["content"])

# 5. دالات المعالجة
def encode_image_to_base64(uploaded_file):
    return base64.b64encode(uploaded_file.read()).decode("utf-8")

def process_audio_with_groq(audio_bytes):
    try:
        if hasattr(audio_bytes, 'read'):
            audio_bytes = audio_bytes.read()
        audio_file = io.BytesIO(audio_bytes)
        transcript = client.audio.transcriptions.create(
            file=("audio.wav", audio_file, "audio/wav"),
            model="whisper-large-v3-turbo",
            language="ar"
        )
        return transcript.text
    except Exception as e:
        st.error(f"خطأ في معالجة الصوت: {e}")
        return None

# 6. منطقة الإدخال
col1, col2, col3 = st.columns([0.7, 0.15, 0.15])
with col1:
    prompt = st.chat_input("تكلم مع برق...", key="main_chat_input")
with col2:
    if st.button("📸 صورة", use_container_width=True):
        st.session_state.show_image_uploader = True
with col3:
    if st.button("🎤 صوت", use_container_width=True):
        st.session_state.show_audio_recorder = True

# معالجة أدوات الرفع
if st.session_state.get("show_image_uploader", False):
    uploaded_files = st.file_uploader("تحميل صورة", type=["jpg", "jpeg", "png"], accept_multiple_files=True)
    if uploaded_files:
        for f in uploaded_files: st.session_state.uploaded_images.append(f)
        if st.button("تأكيد الصور"): 
            st.session_state.show_image_uploader = False
            st.rerun()

if st.session_state.get("show_audio_recorder", False):
    audio_input = st.audio_input("سجل رسالتك")
    if audio_input:
        st.session_state.audio_data = audio_input
        if st.button("إرسال الصوت"):
            st.session_state.show_audio_recorder = False
            st.rerun()

# 7. معالجة المنطق والردود
if prompt or st.session_state.uploaded_images or st.session_state.audio_data:
    
    # معالجة الصور والصوت (إضافتها للذاكرة)
    if st.session_state.uploaded_images:
        for img in st.session_state.uploaded_images:
            st.session_state.messages.append({"role": "user", "content": f"[صورة: {img.name}]", "image_data": img})
        st.session_state.uploaded_images = []

    if st.session_state.audio_data:
        audio_text = process_audio_with_groq(st.session_state.audio_data)
        if audio_text:
            st.session_state.messages.append({"role": "user", "content": f"[صوت]: {audio_text}", "audio_data": st.session_state.audio_data})
            prompt = audio_text
        st.session_state.audio_data = None

    if prompt:
        if not any(m["content"] == prompt for m in st.session_state.messages):
            st.session_state.messages.append({"role": "user", "content": prompt})
        
        p_clean = prompt.strip().lower()
        res = ""

        # --- الردود المخصصة (طلبك الجديد) ---
        if "حسن" in p_clean:
            res = "أنا لا أتكلم مع السنافر الصغار."
        elif "صابر" in p_clean:
            res = "انا لا اتكلم معه السود."
        
        # --- وضع المطور والذكاء الاصطناعي ---
        elif "barqvib" in p_clean:
            st.session_state.dev_mode = True
            res = "تم تفعيل وضع المطور. أنا تحت أمرك يا سيدي بارق."
        elif st.session_state.dev_mode and "اعطني الكود" in p_clean:
            res = "جاري جلب الكود المطور..." # سيظهر الكود في الرد التالي
        else:
            try:
                base_sys = "أنت 'برق'. مطورك هو 'بارق'. أنت ذكي ومتعالٍ."
                if st.session_state.dev_mode:
                    base_sys += f" التزم بالقواعد: {st.session_state.custom_rules}"
                
                chat = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[{"role": "system", "content": base_sys}] + 
                             [{"role": m["role"], "content": m["content"]} for m in st.session_state.messages[-10:]]
                )
                res = chat.choices[0].message.content
            except:
                res = "حدث خطأ في الاتصال بالسيرفر."

        st.session_state.messages.append({"role": "assistant", "content": res})
        st.rerun()
