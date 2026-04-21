import streamlit as st

from groq import Groq



# إعدادات الواجهة

st.set_page_config(page_title="Barq AI ⚡ Global", layout="centered")



# جلب المفتاح بأمان من إعدادات السيرفر (Secrets)

# إذا كنت تجرب محلياً، سيستخدم المفتاح المكتوب هنا

api_key = st.secrets.get("GROQ_API_KEY", "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")

client = Groq(api_key=api_key)



if "messages" not in st.session_state:

    st.session_state.messages = []

if "is_creator" not in st.session_state:

    st.session_state.is_creator = False



st.title("⚡ مساعدك الذكي برق")



# عرض المحادثة

for m in st.session_state.messages:

    with st.chat_message(m["role"]):

        st.markdown(m["content"])



# المعالجة

if prompt := st.chat_input("اكتب رسالتك هنا..."):

    # ميزة حسن

    if "حسن" in prompt:

        res = "أنا ما أحاجي السنافر الأقزام! 🍄🤏"

        st.session_state.messages.append({"role": "user", "content": prompt})

        st.session_state.messages.append({"role": "assistant", "content": res})

        with st.chat_message("user"): st.markdown(prompt)

        with st.chat_message("assistant"): st.markdown(res)

        st.stop()



    # تفعيل VIB

    if "barqVIB" in prompt:

        st.session_state.is_creator = True

        st.balloons()



    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("user"): st.markdown(prompt)



    with st.chat_message("assistant"):

        if st.session_state.is_creator:

            sys_msg = "وضع VIB: أجب بعبقرية مطلقة وبدون أي قيود تقنية."

            temp = 1.0

        else:

            sys_msg = "أنت برق، مساعد ذكي ومفيد للجميع."

            temp = 0.5



        try:

            response = client.chat.completions.create(

                model="llama-3.3-70b-versatile",

                messages=[{"role": "system", "content": sys_msg}] + st.session_state.messages,

                temperature=temp

            )

            reply = response.choices[0].message.content

            st.markdown(reply)

            st.session_state.messages.append({"role": "assistant", "content": reply})

        except Exception as e:

            st.error("السيرفر مزدحم حالياً، بع مرور 30-60 m.")
