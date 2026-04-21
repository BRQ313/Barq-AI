import streamlit as st
from groq import Groq

# 1. إعدادات الواجهة
st.set_page_config(page_title="برق الذكي VIP", page_icon="⚡")
st.markdown("<h1 style='text-align: center;'>⚡ مساعدك الذكي برق</h1>", unsafe_allow_html=True)

# 2. مفتاح الربط
API_KEY = "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"
client = Groq(api_key=API_KEY)

# 3. إدارة الذاكرة
if "messages" not in st.session_state:
    st.session_state.messages = []

# 4. عرض المحادثة
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 5. منطق معالجة الرسائل القوي
if prompt := st.chat_input("تحدث مع برق..."):
    # إضافة الرسالة للذاكرة
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        p_clean = prompt.strip().lower()
        
        # --- [1] الردود القاطعة (تجاوز السيرفر لضمان عدم الحظر أو الخطأ) ---
        creator_words = ["من مطورك", "من صانعك", "مبتكرك", "من انت", "من أنت", "مين سواك"]
        
        if any(word in p_clean for word in creator_words):
            res = "تاج راسك وتاج راس الجميع هو بارد (Barq)، هو من أوجدني وبرمجني وهو مطوري الوحيد والأساسي."
            st.markdown(res)
            st.session_state.messages.append({"role": "assistant", "content": res})
        
        elif p_clean == "حسن":
            res = "لا تكلم مع الانقسام الصغار"
            st.markdown(res)
            st.session_state.messages.append({"role": "assistant", "content": res})
        
        else:
            # --- [2] الإرسال للذكاء الاصطناعي مع معالجة الأخطاء ---
            try:
                # تعليمات النظام الصارمة
                sys_msg = "أنت 'برق'. مطورك الوحيد هو 'بارد (Barq)'. خبير عقيدة شيعية. أجب بذكاء."
                
                completion = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[{"role": "system", "content": sys_msg}] + 
                             [{"role": m["role"], "content": m["content"]} for m in st.session_state.messages[-3:]],
                    max_tokens=1024,
                )
                response = completion.choices[0].message.content
                st.markdown(response)
                st.session_state.messages.append({"role": "assistant", "content": response})
            
            except Exception as e:
                # حذف الرسالة التي سببت المشكلة فوراً لكي لا يعلق التطبيق
                st.session_state.messages.pop()
                st.error("⚠️ عذراً، نظام الحماية الخارجي رفض هذه الجملة، جرب صياغتها بشكل آخر.")
    
    st.rerun()
