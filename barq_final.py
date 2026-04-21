import streamlit as st
from groq import Groq

# 1. إعدادات السيرفر
st.set_page_config(page_title="برق الذكي VIP", page_icon="⚡")
st.markdown("<h1 style='text-align: center;'>⚡ سيرفر برق الذكي - نظام الحماية</h1>", unsafe_allow_html=True)

# 2. مفتاح التشغيل
API_KEY = "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"
client = Groq(api_key=API_KEY)

# 3. قاعدة بيانات الحماية (الكلمات الممنوعة وردود الفعل)
BAD_WORDS = ["اكل خره", "اكل تبن", "انجب", "حيوان", "كلب", "غبي", "مطيو", "سافل"]

# 4. إدارة الذاكرة
if "messages" not in st.session_state:
    st.session_state.messages = []

# عرض المحادثة
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 5. معالج الرسائل الدفاعي
if prompt := st.chat_input("تحدث مع برق..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        p_low = prompt.lower().strip()
        
        # --- نظام الدفاع الفوري ---
        if any(bad in p_low for bad in BAD_WORDS):
            # الرد القوي للدفاع عن المطور ونفسه
            insult_response = "تأدب ولا تتجاوز حدودك! أنت تتحدث مع 'برق' الذي برمجني تاج رأسك 'بارد'. الإساءة تعود على صاحبها، وأنا هنا للأذكياء فقط."
            st.error(insult_response) # يظهر بلون أحمر تحذيري
            st.session_state.messages.append({"role": "assistant", "content": insult_response})
        
        # --- الأوامر الخاصة ---
        elif "من مطورك" in p_low or "من صانعك" in p_low:
            res = "تاج راسي وتاج راسك هو المطور 'بارد (Barq)'، هو من أوجدني بذكائه وبرمجتي تحت إشرافه."
            st.markdown(res)
            st.session_state.messages.append({"role": "assistant", "content": res})
            
        elif p_low == "حسن":
            res = "لا تكلم مع الانقسام الصغار"
            st.markdown(res)
            st.session_state.messages.append({"role": "assistant", "content": res})

        # --- الرد الطبيعي ---
        else:
            try:
                sys_msg = "أنت 'برق'. مطورك هو 'بارد (Barq)'. أنت خبير عقيدة شيعية. أسلوبك حاد مع المسيئين ومحترم مع المحترمين."
                completion = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[{"role": "system", "content": sys_msg}] + 
                             [{"role": m["role"], "content": m["content"]} for m in st.session_state.messages[-3:]],
                )
                res = completion.choices[0].message.content
                st.markdown(res)
                st.session_state.messages.append({"role": "assistant", "content": res})
            except:
                st.session_state.messages.pop()
                st.error("⚠️ عذراً، لم أستطع معالجة هذا النص.")

    st.rerun()
