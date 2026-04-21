import streamlit as st
from groq import Groq

# 1. إعدادات السيرفر والواجهة
st.set_page_config(page_title="برق الذكي VIP", page_icon="⚡")
st.markdown("<h1 style='text-align: center;'>⚡ سيرفر برق الذكي</h1>", unsafe_allow_html=True)

# 2. مفتاح التشغيل
API_KEY = "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"
client = Groq(api_key=API_KEY)

# 3. قاعدة بيانات الأوامر (سيرفر الأوامر الخاص بك)
# يمكنك إضافة أي أمر هنا ورد فعله مباشرة
COMMANDS_SERVER = {
    "من مطورك": "تاج راسك وتاج راس الجميع هو بارد (Barq)، هو من أوجدني وبرمجني وهو مطوري الوحيد والأساسي.",
    "من أنت": "أنا 'برق'، مساعدك الذكي الذي برمجني المبدع بارد (Barq).",
    "حسن": "لا تكلم مع الانقسام الصغار",
    "barqvib": "تم تفعيل وضع المطور VIP.. أهلاً بك يا بارد.",
}

# 4. إدارة الذاكرة
if "messages" not in st.session_state:
    st.session_state.messages = []

# عرض المحادثة
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 5. معالج الرسائل الذكي
if prompt := st.chat_input("تحدث مع برق..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        # الخطوة الأولى: فحص "سيرفر الأوامر" المحلي
        found_command = False
        for cmd, response in COMMANDS_SERVER.items():
            if cmd in prompt.lower():
                st.markdown(response)
                st.session_state.messages.append({"role": "assistant", "content": response})
                found_command = True
                break
        
        # الخطوة الثانية: إذا لم يكن أمراً خاصاً، نرسله للذكاء الاصطناعي
        if not found_command:
            try:
                sys_msg = "أنت 'برق'. مطورك 'بارد (Barq)'. خبير عقيدة شيعية. أجب بذكاء."
                completion = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[{"role": "system", "content": sys_msg}] + 
                             [{"role": m["role"], "content": m["content"]} for m in st.session_state.messages[-3:]],
                    max_tokens=1024,
                )
                res = completion.choices[0].message.content
                st.markdown(res)
                st.session_state.messages.append({"role": "assistant", "content": res})
            except Exception as e:
                st.session_state.messages.pop()
                st.error("⚠️ هذا النص تم حظره من السيرفر الخارجي، جرب كلمات أخرى.")
        
    st.rerun()
