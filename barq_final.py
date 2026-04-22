import streamlit as st
from groq import Groq

# 1. إعدادات المتصفح
st.set_page_config(page_title="برق الذكي VIP", page_icon="⚡")

# 2. جلب المفتاح وإعداد العميل
MY_API_KEY = "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"
client = Groq(api_key=MY_API_KEY)

# 3. الذاكرة
if "messages" not in st.session_state:
    st.session_state.messages = []

st.title("⚡ الذكاء الاصطناعي برق وأنا أذكى منك يا فاشل")

# قائمة الدفاع
ANTI_INSULT = {
    "اكل خره": "ما اكلك يا خره.",
    "اكل تبن": "ماكو تبن اله غرك.",
    "انجب": "سأصمت لاني لا اتكلم مع الغبياء أمثالك.",
    "حيوان": "الإساءة تعود على صاحبها.",
    "كلب": "الوفاء للكلاب، وأنت تفتقر لهذه الصفة."
}

# 4. عرض الرسائل السابقة
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 5. معالجة الإدخال
if prompt := st.chat_input("اكتب شتريد او ولي من يمي"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        # تحويل النص ليكون متوافقاً مع فحص الكلمات
        p_low = prompt.strip()
        
        # 1. فحص قائمة الدفاع أولاً
        if p_low in ANTI_INSULT:
            res = ANTI_INSULT[p_low]
            st.markdown(res)
        else:
            # 2. إذا لم تكن مسبة، نرسلها لـ Groq
            try:
                sys_msg = "أنت 'برق'. مطورك هو 'بارق'. أنت خبير وتتحدث بقوة."
                chat_completion = client.chat.completions.create(
                   model="llama-3.1-8b-instant", 
                    messages=[{"role": "system", "content": sys_msg}] + 
                             [{"role": m["role"], "content": m["content"]} for m in st.session_state.messages[-5:]]
                )
                res = chat_completion.choices[0].message.content
                st.markdown(res)
            except Exception as e:
                # هذا الرد يظهر فقط إذا تعطل الإنترنت أو الـ API Key
                res = "عندي مشكلة بالاتصال، لحظة وراجعلك."
                st.error(f"خطأ تقني: {e}") 

    st.session_state.messages.append({"role": "assistant", "content": res})
