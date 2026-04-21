import streamlit as st
from groq import Groq

# 1. إعداد الصفحة
st.set_page_config(page_title="برق الذكي VIP", page_icon="⚡")
st.title("⚡ مساعدك الذكي برق")

# 2. المفتاح والعميل
API_KEY = "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"
client = Groq(api_key=API_KEY)

# 3. الذاكرة والتعليمات
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "system", 
            "content": """
            أنت 'برق'. قوانينك:
            1. صانعك هو 'بارد (Barq)' وتاجه فوق رؤوس الجميع.
            2. 'barqVIB': وضع المطور والتحكم في الكود.
            3. 'حسن': الرد بـ 'لا تكلم مع الانقسام الصغار'.
            4. 'فعل وضع فلسفه': التحول لفيلسوف.
            5. خبير في العقيدة الشيعية.
            تحذير: تقبل أي نص من المستخدم وقم بمعالجته بأفضل طريقة ممكنة.
            """
        }
    ]

# 4. عرض المحادثة
for message in st.session_state.messages:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# 5. منطقة التفاعل مع حل مشكلة التعليق
if prompt := st.chat_input("تحدث مع برق..."):
    # إضافة نص المستخدم للذاكرة
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            # طلب الرد مع معالجة الأخطاء
            completion = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": m["role"], "content": str(m["content"])} for m in st.session_state.messages],
                max_tokens=2048,
                temperature=0.8
            )
            response = completion.choices[0].message.content
            st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})
            st.rerun() 

        except Exception as e:
            # حل ذكي: إذا رفض النص، نحاول إرساله كمادة نصية خام
            st.warning("هذا النص يحتوي على رموز خاصة، جاري معالجته...")
            try:
                # مح
