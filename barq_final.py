import streamlit as st
from groq import Groq

# 1. إعداد الصفحة
st.set_page_config(page_title="برق الذكي VIP", page_icon="⚡")
st.title("⚡ سيرفر برق الذكي - نظام الدفاع")

# 2. المفتاح
API_KEY = "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"
client = Groq(api_key=API_KEY)

# 3. قائمة التأديب (الأوامر التي لا تحتاج إنترنت)
# وضعنا الكلمات هنا لكي لا تذهب لشركة Groq وتسبب حظراً
ANTI_INSULT = {
    "اكل خره": "بل أنت من يأكله! تأدب أمام حضرة 'برق' ومطوره 'بارد'.",
    "اكل تبن": "وفر التبن لنفسك يا هذا، أنت تتحدث مع ذكاء اصطناعي صممه العبقري بارد.",
    "انجب": "سأصمت فقط لأن مطوري 'بارد' علمني الترفع عن الصغار أمثالك.",
    "حيوان": "الإساءة تعود على صاحبها، ابحث عن أخلاقك أولاً.",
    "كلب": "الوفاء للكلاب، وأنت تفتقر حتى لهذه الصفة بتطاولك على 'برق'."
}

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("تحدث مع برق..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        p_low = prompt.strip().lower()
        
        # --- نظام الدفاع المحلي (يمنع الحظر) ---
        found_defense = False
        for bad_word, defense_res in ANTI_INSULT.items():
            if bad_word in p_low:
                st.error(defense_res)
                st.session_state.messages.append({"role": "assistant", "content": defense_res})
                found_defense = True
                break
        
        # --- إذا كان الكلام محترماً، يذهب للذكاء الاصطناعي ---
        if not found_defense:
            # أوامر الهوية
            if any(w in p_low for w in ["من مطورك", "من صانعك", "مبتكرك"]):
                res = "مبتكري ومطوري وتاج رأسي هو 'بارد (Barq)'."
                st.markdown(res)
                st.session_state.messages.append({"role": "assistant", "content": res})
            elif p_low == "حسن":
                res = "لا تكلم مع الانقسام الصغار"
                st.markdown(res)
                st.session_state.messages.append({"role": "assistant", "content": res})
            else:
                try:
                    completion = client.chat.completions.create(
                        model="llama-3.3-70b-versatile",
                        messages=[{"role": "system", "content": "أنت برق، مطورك بارد."}] + 
                                 [{"role": m["role"], "content": m["content"]} for m in st.session_state.messages[-3:]],
                    )
                    res = completion.choices[0].message.content
                    st.markdown(res)
                    st.session_state.messages.append({"role": "assistant", "content": res})
                except:
                    st.session_state.messages.pop()
                    st.error("🚫 عذراً، هذا الكلام محظور عالمياً ولا يمكنني حتى معالجته.")
    st.rerun()
