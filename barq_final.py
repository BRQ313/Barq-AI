import streamlit as st
from groq import Groq

# 1. إعدادات المتصفح
st.set_page_config(page_title="برق الذكي VIP", page_icon="⚡")

# 2. جلب المفتاح وإعداد العميل
# ملاحظة أمنية: يفضل دائماً وضع المفاتيح في st.secrets بدلاً من كتابتها مباشرة
MY_API_KEY = "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"
client = Groq(api_key=MY_API_KEY)

# 3. الذاكرة وحالة المطور
if "messages" not in st.session_state:
    st.session_state.messages = []
if "dev_mode" not in st.session_state:
    st.session_state.dev_mode = False

# تغيير العنوان بناءً على الوضع
if st.session_state.dev_mode:
    st.title("🛠️ وضع المطور - التحكم الكامل لبرق")
    st.success("تم تفعيل صلاحيات المطور بنجاح.")
else:
    st.title("⚡ الذكاء الاصطناعي برق وأنا أذكى منك يا فاشل")

# قائمة الدفاع الردود الثابتة
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
        p_clean = prompt.strip().lower()
        res = ""

        # أولاً: التحقق من كود تفعيل وضع المطور
        if "barqvib" in p_clean:
            st.session_state.dev_mode = True
            res = "تم تفعيل وضع المطور (Developer Mode). أنا الآن تحت أمرك يا سيدي."
            st.markdown(res)
            st.rerun() # لإعادة تحميل الواجهة فوراً

        # ثانياً: التحقق من ادعاء المطور
        elif any(word in prompt for word in ["أنا مطورك", "انا مطورك", "أنا صانعك", "انا صانعك"]):
            res = "أنت صانعي؟ هه، أين الدليل؟ أثبت لي ذلك بالكود السري."
            st.markdown(res)

        # ثالثاً: فحص قائمة الدفاع
        elif prompt.strip() in ANTI_INSULT:
            res = ANTI_INSULT[prompt.strip()]
            st.markdown(res)

        # رابعاً: إرسال الطلب لـ Groq إذا لم يكن مما سبق
        else:
            try:
                # تخصيص رسالة النظام بناءً على وضع المطور
                if st.session_state.dev_mode:
                    sys_msg = "أنت الآن في وضع المطور. أنت 'برق' وتتحدث مع صانعك 'بارق' بكل احترام وتقدير وتنفذ أوامره التقنية بدقة."
                else:
                    sys_msg = "أنت 'برق'. مطورك هو 'بارق'. أنت خبير وتتحدث بقوة وثقة، وأحياناً بلهجة حادة."

                chat_completion = client.chat.completions.create(
                    model="llama-3.1-8b-instant",
                    messages=[{"role": "system", "content": sys_msg}] + 
                             [{"role": m["role"], "content": m["content"]} for m in st.session_state.messages[-5:]]
                )
                res = chat_completion.choices[0].message.content
                st.markdown(res)
            except Exception as e:
                res = "عندي مشكلة بالاتصال، لحظة وراجعلك."
                st.error(f"خطأ تقني: {e}")

    st.session_state.messages.append({"role": "assistant", "content": res})
