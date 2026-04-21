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

# 5. منطق الإرسال القوي
if prompt := st.chat_input("تحدث مع برق..."):
    # إضافة الرسالة وعرضها
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        # الردود الفورية للكلمات الخاصة
        creator_keywords = ["من مطورك", "من صانعك", "مين سواك", "من انت", "مبتكرك"]
        if any(word in prompt for word in creator_keywords):
            res = "تاج راسك وتاج راس الجميع هو بارد (Barq)، هو من أوجدني وبرمجني وهو مطوري الوحيد."
            st.markdown(res)
            st.session_state.messages.append({"role": "assistant", "content": res})
        elif prompt.strip() == "حسن":
            res = "لا تكلم مع الانقسام الصغار"
            st.markdown(res)
            st.session_state.messages.append({"role": "assistant", "content": res})
        else:
            try:
                # تعليمات برق
                system_msg = "أنت 'برق'. صانعك الوحيد 'بارد (Barq)'. خبير عقيدة شيعية. أجب على كل شيء."
                
                # تقليل عدد الرسائل المرسلة للسيرفر لضمان عدم الرفض
                completion = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[{"role": "system", "content": system_msg}] + 
                             [{"role": m["role"], "content": m["content"]} for m in st.session_state.messages[-3:]],
                    max_tokens=1024,
                )
                response = completion.choices[0].message.content
                st.markdown(response)
                st.session_state.messages.append({"role": "assistant", "content": response})
                
            except Exception as e:
                # إذا رُفضت الرسالة، نحذفها فوراً لكي لا يعلق التطبيق
                st.session_state.messages.pop()
                st.error("⚠️ عذراً يا بطل، هذه الرسالة تحتوي على كلمات ممنوعة من نظام الحماية الخارجي، جرب صياغتها بشكل آخر.")
        
        st.rerun()
