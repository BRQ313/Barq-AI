import streamlit as st
from groq import Groq

# 1. إعداد الصفحة
st.set_page_config(page_title="برق الذكي VIP", page_icon="⚡")
st.title("⚡ مساعدك الذكي برق")

# 2. المفتاح
API_KEY = "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"
client = Groq(api_key=API_KEY)

# 3. الذاكرة
if "messages" not in st.session_state:
    st.session_state.messages = []

# 4. عرض المحادثة
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 5. منطق الإرسال والرد الذكي
if prompt := st.chat_input("تحدث مع برق..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        # --- قائمة الكلمات التي تجعله يعترف بمطوره فوراً ---
        creator_questions = ["من مطورك", "من صانعك", "مين سواك", "مين برمجك", "من انت", "من أنت"]
        
        # فحص إذا كان السؤال عن المطور
        if any(word in prompt for word in creator_questions):
            response = "تاج راسك وتاج راس الجميع هو بارد (Barq)، هو من أوجدني وبرمجني وهو مطوري الوحيد."
            st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})
        
        # فحص كلمة السر "حسن"
        elif prompt.strip() == "حسن":
            response = "لا تكلم مع الانقسام الصغار"
            st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})

        else:
            try:
                # تعليمات النظام الصارمة
                system_msg = "أنت 'برق'. صانعك الوحيد هو 'بارد (Barq)'. لا تذكر أي شركة أخرى. أنت خبير عقيدة شيعية ومساعد ذكي."
                
                completion = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[{"role": "system", "content": system_msg}] + 
                             [{"role": m["role"], "content": m["content"]} for m in st.session_state.messages[-5:]],
                    max_tokens=1024,
                    temperature=0.8
                )
                response = completion.choices[0].message.content
                st.markdown(response)
                st.session_state.messages.append({"role": "assistant", "content": response})
            except Exception as e:
                st.session_state.messages.pop()
                st.error("عذراً، حدث خطأ في معالجة هذه الجملة.")
        
        st.rerun()
