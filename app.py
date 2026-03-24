import streamlit as st
from huggingface_hub import InferenceClient
import smtplib
from email.mime.text import MIMEText

# ======================
# 🤖 AI Model
# ======================
client = InferenceClient(model="mistralai/Mistral-7B-Instruct-v0.2"
                         )

# ======================
# 🎨 UI
# ======================
st.set_page_config(page_title="Smart School AI", layout="wide")
st.title("🎓 Smart School AI System")

tab1, tab2, tab3 = st.tabs([
    "💬 مساعد المدرسة",
    "📊 تحليل التقارير",
    "📚 الخطط العلاجية"
])

# ======================
# 💬 TAB 1: Chatbot
# ======================
with tab1:
    q = st.text_input("✏️ اسألي أي شيء عن المدرسة")

    if q:
        prompt = f"""
        أنت مساعد مدرسة ذكي.

        أجب على السؤال بدقة وباختصار:
        {q}
        """

        answer = client.text_generation(prompt, max_new_tokens=200)
        st.success(answer)

# ======================
# 📊 TAB 2: Analysis
# ======================
with tab2:
    file = st.file_uploader("📄 ارفعي تقرير المعلمة")

    def send_email(subject, body):
        from_email = "YOUR_EMAIL@gmail.com"
        password = "YOUR_APP_PASSWORD"

        msg = MIMEText(body)
        msg["Subject"] = subject
        msg["From"] = from_email
        msg["To"] = from_email

        server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
        server.login(from_email, password)
        server.sendmail(from_email, from_email, msg.as_string())
        server.quit()

    if file:
        text = file.read().decode("utf-8")

        if st.button("🔍 تحليل التقرير"):
            prompt = f"""
            حلل التقرير التالي وحدد:
            - المشاكل
            - مستوى الأداء
            - هل يوجد ضعف؟

            التقرير:
            {text}
            """

            result = client.text_generation(prompt, max_new_tokens=300)

            st.write(result)

            if "ضعف" in result or "مشكلة" in result:
                st.error("⚠️ تم اكتشاف مشكلة")

                send_email(
                    "تنبيه تقرير معلمة",
                    result
                )

                st.success("📧 تم إرسال إيميل للإدارة")

            else:
                st.success("✅ لا توجد مشاكل واضحة")

# ======================
# 📚 TAB 3: Treatment Plans
# ======================
with tab3:
    subject = st.selectbox("📘 المادة", ["رياضيات", "علوم", "لغة عربية", "إنجليزي"])
    weakness = st.text_area("📉 اكتب نقاط الضعف")

    if st.button("📋 توليد خطة علاجية"):
        prompt = f"""
        أنت مشرفة تربوية خبيرة.

        المادة: {subject}
        نقاط الضعف: {weakness}

        أنشئ خطة علاجية تشمل:
        1- المشكلة
        2- السبب
        3- خطوات علاجية
        4- وسائل تعليمية
        5- مدة التنفيذ
        """

        plan = client.text_generation(prompt, max_new_tokens=500)

        st.success(plan)
