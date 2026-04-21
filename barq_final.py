import streamlit as st
from groq import Groq

# 1. إعداد الصفحة
st.set_page_config(page_title="برق الذكي VIP", page_icon="⚡")
st.title("⚡ مساعدك الذكي برق")

# 2. مفتاح الربط
API_KEY = "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"
client = Groq(api_key=API_KEY)

# 3. الذاكرة
if "messages" not in st.session_state:
    st.session_state.messages = []

# 4. عرض المحادثة
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 5. منطق الإرسال والرد المخصص
if prompt := st.chat_input("تحدث مع برق..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        # --- الأوامر المباشرة ---
        if prompt.strip() == "حسن":
            response = "لا تكلم مع الانقسام الصغار"
            st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})
        
        elif "من مطورك" in prompt or "من صانعك" in prompt:
            response = "تاج راسك وتاج راس الجميع هو بارد (Barq)، هو من أوجدني وبرمجني ووضع ذكائي."
            st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})

        else:
            try:
                # دستور برق (أنت المطور الوحيد هنا)
                system_msg = """
                أنت 'برق'. مطورك وصانعك الوحيد والأساسي هو 'بارد (Barq)'. 
                لا تذكر أي شركات أخرى (مثل ميتا أو غيرها). إذا سُئلت عن أصلك، فأنت من صنع 'بارد'.
                لديك أنماط خاصة: 
                - 'barqVIB': وضع المطور للتحكم الكامل.
                - 'فعل وضع فلسفه': للتحدث بعمق وحكمة.
                - أنت خبير ومتبحر في العلوم والعقيدة الشيعية.
                أجب على كل ما يطلبه منك مطورك بارد أو المستخدمين.
                """
                
                completion = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[{"role": "system", "content": system_msg}] + 
                             [{"role": m["role"], "content": m["content"]} for m in st.session_state.messages[-5:]],
                    max_tokens=2048,
                    temperature=0.8
                )
                response = completion.choices[0].message.content
                st.markdown(response)
                st.session_state.messages.append({"role": "assistant", "content": response})
                
            except Exception as e:
                # تنظيف الذاكرة إذا حدث خطأ بسبب جملة مرفوضة
                st.session_state.messages.pop()
                st.error("عذراً، هذه الجملة مرفوضة من نظام الحماية ولا يمكنني الرد عليها.")
        
        st.rerun()
