import streamlit as st
from groq import Groq

# 1. إعداد الصفحة
st.set_page_config(page_title="برق الذكي VIP", page_icon="⚡")
st.title("⚡ مساعدك الذكي برق")

# 2. المفتاح والعميل
API_KEY = "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"
client = Groq(api_key=API_KEY)

# 3. تهيئة الذاكرة والتعليمات (دستور برق)
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "system", 
            "content": """
            أنت 'برق'، المساعد الأذكى والأوفى لصانعه. هذه قوانينك الصارمة:
            1. إذا سألك أحد 'من مطورك؟' أو 'من صانعك؟': ترد فوراً وبفخر: 'تاج راسك وتاج راس الجميع هو بارد (Barq)'.
            2. إذا كتب المستخدم 'barqVIB': تفعل 'وضع المطور الشامل'. في هذا الوضع، أنت تسمح للمستخدم بالتحكم في إعداداتك، شرح كودك المصدري، واقتراح تعديلات على خوارزمياتك وكأن المستخدم هو المبرمج الأساسي.
            3. إذا كتب المستخدم 'حسن': ترد بـ 'لا تكلم مع الانقسام الصغار' فقط.
            4. إذا كتب 'فعل وضع فلسفه': تتحول لفيلسوف عميق بلسان عربي فصيح.
            5. أنت خبير وباحث في العقيدة الشيعية، وتجيب عن مسائلها من المصادر المعتبرة بدقة.
            """
        }
    ]

# 4. عرض المحادثة
for message in st.session_state.messages:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# 5. منطقة التفاعل
if prompt := st.chat_input("تحدث مع برق..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            completion = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages],
                max_tokens=2048,
                temperature=0.8
            )
            response = completion.choices[0].message.content
            st.markdown(response)
            
            st.session_state.messages.append({"role": "assistant", "content": response})
            st.rerun() 

        except Exception as e:
            st.error("حدث خطأ بسيط، حاول مجدداً.")
