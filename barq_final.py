import streamlit as st
from groq import Groq

# 1. إعدادات الصفحة
st.set_page_config(page_title="برق الذكي VIP", page_icon="⚡", layout="wide")

# 2. إعداد الاتصال بـ Groq
if "GROQ_API_KEY" not in st.secrets:
    st.error("المفتاح مفقود! أضفه في Secrets.")
    st.stop()

client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# حساب المبتكر (المطور الأساسي)
CREATOR_ACCOUNT = "BRQ313"

# 3. تهيئة الذاكرة (Session State)
if "messages" not in st.session_state:
    st.session_state.messages = []
if "dev_mode" not in st.session_state:
    st.session_state.dev_mode = False
if "custom_rules" not in st.session_state:
    st.session_state.custom_rules = "" # مخزن الميزات الجديدة

# 4. التحقق التلقائي: تفعيل وضع المطور للمبتكر
try:
    current_user = st.session_state.get("user_info", {}).get("username", "")
    # إذا كان المستخدم هو المبتكر، فعّل وضع المطور تلقائياً
    if current_user == CREATOR_ACCOUNT or st.secrets.get("STREAMLIT_USER") == CREATOR_ACCOUNT:
        st.session_state.dev_mode = True
except:
    pass

# 5. واجهة المستخدم
if st.session_state.dev_mode:
    st.title("🛠️ نظام التطوير الذاتي - أهلاً سيدي بارق")
    st.sidebar.success("✅ وضع المطور مفعّل تلقائياً")
    if st.session_state.custom_rules:
        st.sidebar.info(f"الميزات المضافة حالياً: {st.session_state.custom_rules}")
else:
    st.title("⚡  الذكاء الاصطناعي برق وانا ايضن اذكا منك يا فاشل يا ابو طكعه")

# عرض الرسائل السابقة
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 6. منطقة الإدخال (مع حل مشكلة الفراغات والإرسال المزدوج)
if prompt := st.chat_input("اكتب شتريد اولي من يمي", key="main_chat_input"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        p_clean = prompt.strip().lower()
        res = ""

        # --- المنطق البرمجي (الأولويات) ---

        # أولاً: تفعيل وضع المطور (كلمة السر)
        if "barqvib" in p_clean:
            st.session_state.dev_mode = True
            res = "تم تفعيل بروتوكول المطور. أنا الآن تحت أمرك يا سيدي، سأقوم بتطوير منطقي بناءً على توجيهاتك."
            st.markdown(res)
            st.session_state.messages.append({"role": "assistant", "content": res})
            st.rerun()

        # ثانياً: ميزة "طور نفسك" أو "ضيف ميزة" (تعمل فقط في وضع المطور)
        elif st.session_state.dev_mode and any(word in p_clean for word in ["ضيف ميزة", "طور نفسك", "عدل سلوكك"]):
            st.session_state.custom_rules += f"\n- {prompt}"
            res = f"تم تحديث نظامي الداخلي بنجاح. الميزة الجديدة مضافة الآن: {prompt}"
            st.success(res)

        # ثالثاً: طلب الكود المحدث (إذا طلبت منه كود التعديل)
        elif st.session_state.dev_mode and "اعطني الكود" in p_clean:
            sys_msg = "أنت مهندس برمجيات محترف. قم بكتابة الكود الكامل لملف streamlit الحالي مع إضافة كافة التحسينات التي طلبها المطور."
            try:
                response = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[{"role": "system", "content": sys_msg}] + st.session_state.messages
                )
                res = response.choices[0].message.content
                st.code(res, language="python") # عرض الكود في مربع خاص للنسخ
            except Exception as e:
                st.error(f"فشل جلب الكود: {e}")

        # رابعاً: الرد العام (الذكاء الاصطناعي)
        else:
            try:
                # تشكيل الشخصية بناءً على الوضع والميزات المضافة
                if st.session_state.dev_mode:
                    base_sys = f"أنت 'برق'. المطور 'بارق' يتحدث معك. التزم بهذه القواعد المضافة: {st.session_state.custom_rules}"
                else:
                    base_sys = "أنت 'برق'. مطورك هو 'بارق'. أنت ذكي، متعالٍ قليلاً، ولا تحب التفاهة."

                chat_completion = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[{"role": "system", "content": base_sys}] + 
                             [{"role": m["role"], "content": m["content"]} for m in st.session_state.messages[-10:]]
                )
                res = chat_completion.choices[0].message.content
                st.markdown(res)
            except Exception as e:
                st.error(f"خطأ في السيرفر: {e}")
                res = "حدث خطأ أثناء محاولة الرد."

        st.session_state.messages.append({"role": "assistant", "content": res})
