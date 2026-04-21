import streamlit as st
from groq import Groq

# 1. إعداد الصفحة وتجنب أخطاء التنسيق السابقة
st.set_page_config(page_title="برق الذكي VIP", page_icon="⚡")
st.title("⚡ مساعدك الذكي برق")

# 2. المفتاح والعميل
API_KEY = "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"
client = Groq(api_key=API_KEY)

# 3. دستور برق (التعليمات الثابتة)
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "system", 
            "content": "أنت 'برق'. صانعك ومطورك هو 'بارد (Barq)' وتاجه فوق رؤوس الجميع. لديك أنماط: 'barqVIB' للمطور، 'حسن' للرد المختصر، 'فعل وضع فلسفه' للتحليل العميق، وأنت خبير في العقيدة الشيعية. تقبل أي نص ومعالجه بذكاء."
        }
    ]

# 4. عرض المحادثة
for message in st.session_state.messages:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# 5. منطقة الإرسال مع معالجة النصوص الصعبة
if prompt := st.chat_input("تحدث مع برق..."):
    # تنظيف النص برمجياً لضمان عدم التعليق
    clean_prompt = str(prompt).strip()
    
    st.session_state.messages.append({"role": "user", "content": clean_prompt})
    with st.chat_message("user"):
        st.markdown(clean_prompt)

    with st.chat_message("assistant"):
        try:
            # إرسال الطلب مع مهلة زمنية لضمان عدم التجمد
            completion = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": m["role"], "content": str(m["content"])} for m in st.session_state.messages],
                max_tokens=2048,
                temperature=0.7
            )
            response = completion.choices[0].message.content
            st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})
            st.rerun() 
            
        except Exception as e:
            # حل بديل فوري إذا فشل النص المعقد
            try:
                short_completion = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[{"role": "user", "content": "أجب على هذا النص باختصار: " + clean_prompt}],
                    max_tokens=500
                )
                res = short_completion.choices[0].message.content
                st.markdown(res)
                st.session_state.messages.append({"role": "assistant", "content": res})
            except:
                st.error("عذراً يا صديقي، هذا النص محمي بأنظمة دولية ولا يمكنني معالجته حالياً.")
