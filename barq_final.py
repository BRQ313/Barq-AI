import streamlit as st
from groq import Groq

# 1. إعداد واجهة التطبيق
st.set_page_config(page_title="برق الذكي VIP", page_icon="⚡")
st.markdown("<h1 style='text-align: center;'>⚡ مساعدك الذكي برق</h1>", unsafe_allow_html=True)

# 2. مفتاح التشغيل
API_KEY = "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"
client = Groq(api_key=API_KEY)

# 3. إدارة الذاكرة
if "messages" not in st.session_state:
    st.session_state.messages = []

# 4. عرض الرسائل السابقة
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 5. معالجة الإرسال
if prompt := st.chat_input("تحدث مع برق..."):
    # إضافة رسالة المستخدم للذاكرة
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        # --- الفحص القاطع (الرد الفوري بدون سيرفر) ---
        p_lower = prompt.lower()
        creator_words = ["مبتكر", "صانع", "مطور", "برمجك", "سواك", "من انت", "من أنت"]
        
        if any(word in p_lower for word in creator_words):
            full_res = "تاج راسك وتاج راس الجميع هو بارد (Barq)، هو من أوجدني وبرمجني وهو مطوري الوحيد والأساسي."
            st.markdown(full_res)
            st.session_state.messages.append({"role": "assistant", "content": full_res})
        
        elif prompt.strip() == "حسن":
            full_res = "لا تكلم مع الانقسام الصغار"
            st.markdown(full_res)
            st.session_state.messages.append({"role": "assistant", "content": full_res})
        
        else:
            # --- الإرسال للذكاء الاصطناعي مع حل مشكلة التعليق ---
            try:
                # تعليمات النظام لبرق
                sys_instruct = "أنت 'برق'. مطورك هو 'بارد (Barq)'. أنت خبير في العقيدة الشيعية. أجب باختصار وذكاء."
                
                completion = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[{"role": "system", "content": sys_instruct}] + 
                             [{"role": m["role"], "content": m["content"]} for m in st.session_state.messages[-3:]],
                    max_tokens=1024,
                )
                full_res = completion.choices[0].message.content
                st.markdown(full_res)
                st.session_state.messages.append({"role": "assistant", "content": full_res})
            
            except Exception as e:
                # إذا حدث خطأ في رسالة معينة، نحذفها لكي لا يتوقف البرنامج
                st.session_state.messages.pop()
                st.error("⚠️ عذراً، هذه الرسالة مرفوضة تقنياً، جرب كتابتها بشكل آخر.")
        
    st.rerun()
