import streamlit as st
from groq import Groq

# 1. إعدادات واجهة التطبيق
st.set_page_config(page_title="برق الذكي", page_icon="⚡", layout="centered")

st.markdown("""
    <style>
    .stChatMessage { border-radius: 15px; margin-bottom: 10px; }
    </style>
    """, unsafe_allow_dict=True)

st.title("⚡ مساعدك الذكي برق")
st.caption("أنا برق، جاهز لمساعدتك في أي وقت!")

# 2. تفعيل مفتاح الربط مباشرة
# ملاحظة: تم وضع المفتاح هنا لضمان عمل التطبيق فوراً
API_KEY = "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"
client = Groq(api_key=API_KEY)

# 3. إدارة ذاكرة المحادثة (السياق)
if "messages" not in st.session_state:
    st.session_state.messages = []

# 4. عرض الرسائل السابقة من الذاكرة
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 5. استقبال وإرسال الرسائل
if prompt := st.chat_input("تحدث مع برق..."):
    # إضافة رسالة المستخدم للذاكرة وعرضها
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # طلب الرد من الذكاء الاصطناعي
    with st.chat_message("assistant"):
        try:
            # استخدام الموديل الأحدث llama-3.3-70b-versatile
            completion = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {"role": m["role"], "content": m["content"]}
                    for m in st.session_state.messages
                ],
                max_tokens=1024,
                temperature=0.7
            )
            
            response = completion.choices[0].message.content
            st.markdown(response)
            
            # حفظ رد الذكاء الاصطناعي في الذاكرة
            st.session_state.messages.append({"role": "assistant", "content": response})
            
        except Exception as e:
            # رسالة ذكية في حال حدوث ضغط على الشبكة
            st.error(f"عذراً يا صديقي، واجهت زحاماً في الطريق. أعد إرسال رسالتك. (الخطأ: {e})")
