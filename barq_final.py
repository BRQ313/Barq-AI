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
    st.error("المفتاح مفقود! أضفه في Secrets تحت اسم GROQ_API_KEY")
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
if "show_image_uploader" not in st.session_state:
    st.session_state.show_image_uploader = False
if "show_audio_recorder" not in st.session_state:
    st.session_state.show_audio_recorder = False

# 4. التحقق من المطور
try:
    if st.secrets.get("STREAMLIT_USER") == CREATOR_ACCOUNT:
        st.session_state.dev_mode = True
except:
    pass

# 5. واجهة المستخدم (العنوان)
if st.session_state.dev_mode:
    st.title("🛠️ نظام التطوير الذاتي - أهلاً سيدي بارق")
    st.sidebar.success("✅ وضع المطور مفعّل")
else:
    st.title("⚡ الذكاء الاصطناعي برق")
    st.caption("أنا أذكى منك يا فاشل.. أمزح (أو ربما لا)")

# عرض الرسائل السابقة
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        if "image_data" in message:
            st.image(message["image_data"], use_container_width=True)
        if "audio_data" in message:
            st.audio(message["audio_data"], format="audio/wav")
        st.markdown(message["content"])

# 6. الدوال المساعدة
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

# 7. أزرار الوسائط (فوق صندوق الدردشة)
col_btn1, col_btn2 = st.columns(2)
with col_btn1:
    if st.button("📸 إرفاق صورة", use_container_width=True):
        st.session_state.show_image_uploader = not st.session_state.show_image_uploader

with col_btn2:
    if st.button("🎤 تسجيل صوتي", use_container_width=True):
        st.session_state.show_audio_recorder = not st.session_state.show_audio_recorder

# 8. منطقة أدوات الإدخال الخاصة
if st.session_state.show_image_uploader:
    with st.expander("تحميل الصور", expanded=True):
        files = st.file_uploader("اختر صور", type=["jpg", "png", "jpeg"], accept_multiple_files=True)
        if files and st.button("تأكيد إرسال الصور"):
            st.session_state.uploaded_images = files
            st.session_state.show_image_uploader = False
            st.rerun()

if st.session_state.show_audio_recorder:
    with st.expander("مسجل الصوت", expanded=True):
        audio_input = st.audio_input("اضغط للتحدث")
        if audio_input and st.button("إرسال التسجيل"):
            st.session_state.audio_data = audio_input
            st.session_state.show_audio_recorder = False
            st.rerun()

# 9. صندوق الدردشة الرئيسي (يجب أن يكون خارج الأعمدة ليعمل بشكل صحيح)
prompt = st.chat_input("اكتب رسالتك هنا...")

# 10. معالجة الإدخالات (النص، الصور، الصوت)
if prompt or st.session_state.uploaded_images or st.session_state.audio_data:
    
    # معالجة الصور المرسلة
    if st.session_state.uploaded_images:
        for img in st.session_state.uploaded_images:
            base64_img = encode_image_to_base64(img)
            st.session_state.messages.append({
                "role": "user", 
                "content": f"[صورة مرفقة: {img.name}]", 
                "image_data": img,
                "image_base64": base64_img
            })
        st.session_state.uploaded_images = []

    # معالجة الصوت المرسل
    if st.session_state.audio_data:
        text_from_audio = process_audio_with_groq(st.session_state.audio_data)
        if text_from_audio:
            st.session_state.messages.append({
                "role": "user", 
                "content": f"[صوت]: {text_from_audio}",
                "audio_data": st.session_state.audio_data
            })
            prompt = text_from_audio # تعيين النص الناتج كـ prompt
        st.session_state.audio_data = None

    # معالجة النص والرد
    if prompt:
        if "role" not in st.session_state.messages or st.session_state.messages[-1]["content"] != prompt:
            st.session_state.messages.append({"role": "user", "content": prompt})
        
        with st.chat_message("assistant"):
            p_clean = prompt.strip().lower()
            
            # منطق الأوامر الخاصة
            if "barqvib" in p_clean:
                st.session_state.dev_mode = True
                res = "تم تفعيل وضع المطور. أنا تحت أمرك يا سيدي بارق."
            
            elif st.session_state.dev_mode and any(x in p_clean for x in ["ضيف ميزة", "طور نفسك"]):
                st.session_state.custom_rules += f"\n- {prompt}"
                res = f"تم تحديث قواعدي البرمجية: {prompt}"
            
            else:
                # الرد عبر AI
                try:
                    if st.session_state.dev_mode:
                        sys_prompt = f"أنت 'برق'. مطورك بارق معك الآن. التزم بـ: {st.session_state.custom_rules}"
                    else:
                        sys_prompt = "أنت 'برق'. مطورك بارق. رد بذكاء وتكبر قليلًا."
                    
                    response = client.chat.completions.create(
                        model="llama-3.3-70b-versatile",
                        messages=[{"role": "system", "content": sys_prompt}] + 
                                 [{"role": m["role"], "content": m["content"]} for m in st.session_state.messages[-10:]]
                    )
                    res = response.choices[0].message.content
                except Exception as e:
                    res = f"حدث خطأ في الاتصال بالسيرفر: {e}"
            
            st.markdown(res)
            st.session_state.messages.append({"role": "assistant", "content": res})
            st.rerun()
