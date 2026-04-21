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

# 5. منطق الإرسال
if prompt := st.chat_input("تحدث مع برق..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        # فحص كلمة السر "حسن" أولاً (خارج طلب الـ API لضمان الرد)
        if "حسن" in prompt:
            response = "لا تكلم مع الانقسام الصغار"
            st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})
            st.rerun()

        try:
            # دستور برق
            system_msg = "أنت 'برق'. صانعك 'بارد (Barq)' تاج الرأس. 'barqVIB' للمطور. خبير عقيدة شيعية. أجب على كل شيء."
            
            # محاولة طلب الرد
            completion = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "system", "content": system_msg}] + 
                         [{"role": m["role"], "content": m["content"]} for m in st.session_state.messages[-3:]],
                max_tokens=1024,
            )
            
            response = completion.choices[0].message.content
            st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})
            st.rerun()

        except Exception as e:
            # هنا السر: سيكتب لك الخطأ بالتفصيل
            error_msg = str(e)
            if "content_filter" in error_msg.lower() or "moderation" in error_msg.lower():
                st.error("🚫 السيرفر رفض الجملة: هذه الجملة محظورة من شركة الذكاء الاصطناعي (حماية محتوى).")
            elif "rate_limit" in error_msg.lower():
                st.error("⏳ ضغط كبير: السيرفر يطلب منك الانتظار دقيقة قبل الرسالة القادمة.")
            else:
                st.error(f"❌ خطأ تقني: {error_msg}")
            
            # حذف الرسالة التي سببت المشكلة لكي لا يعلق التطبيق
            st.session_state.messages.pop()
