import streamlit as st
from groq import Groq

# 1. إعداد الصفحة
st.set_page_config(page_title="برق الذكي VIP", page_icon="⚡")
st.title("⚡ مساعدك الذكي برق")

# 2. المفتاح
API_KEY = "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"
client = Groq(api_key=API_KEY)

# 3. تهيئة الذاكرة
if "messages" not in st.session_state:
    st.session_state.messages = []

# 4. عرض المحادثة السابقة
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 5. منطق الإرسال والرد
if prompt := st.chat_input("تحدث مع برق..."):
    # إضافة الرسالة للذاكرة مؤقتاً
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        # فحص كلمة السر "حسن"
        if prompt.strip() == "حسن":
            response = "لا تكلم مع الانقسام الصغار"
            st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})
        else:
            try:
                # دستور برق
                system_instruction = "أنت 'برق'. مطورك هو 'بارد (Barq)' تاج الرأس. 'barqVIB' للمطور. خبير في العقيدة الشيعية."
                
                # تجهيز الرسائل (نرسل آخر 5 رسائل فقط لتخفيف الضغط)
                api_messages = [{"role": "system", "content": system_instruction}]
                for m in st.session_state.messages[-5:]:
                    api_messages.append({"role": m["role"], "content": m["content"]})
                
                # طلب الرد
                completion = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=api_messages,
                    max_tokens=1024,
                    temperature=0.7
                )
                response = completion.choices[0].message.content
                st.markdown(response)
                # حفظ الرد بنجاح
                st.session_state.messages.append({"role": "assistant", "content": response})
                
            except Exception as e:
                # ----- هذا هو الحل السحري -----
                # إذا حدث خطأ ورفضت الشركة النص، نقوم بحذف رسالتك الأخيرة من الذاكرة حتى لا يتلف التطبيق
                st.session_state.messages.pop() 
                st.error(f"عذراً يا بطل، نظام الحماية الخارجي رفض هذه الجملة تحديداً ولن يتم إرسالها. (السبب: {e})")
