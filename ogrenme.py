import streamlit as st
import os
from docx import Document
import PyPDF2

# --- KONFİQURASİYA ---
RISK_FOKUS = {
    "ƏDV Riskli Məqamlar": ["ədv", "əlavə dəyər vergisi", "vergi tutulan əməliyyat", "əvəzləşdirmə"],
    "Maliyyə Zərəri Riski": ["cərimə", "penya", "gecikmə faizi", "dəbbə pulu", "təzminat"],
    "Hüquqi Boşluq Riski": ["fors-major", "arbitraj", "məhkəmə aidiyyəti", "müqaviləyə xitam"]
}

def read_word(file):
    doc = Document(file)
    return " ".join([para.text for para in doc.paragraphs])

def read_pdf(file):
    text = ""
    reader = PyPDF2.PdfReader(file)
    for page in reader.pages:
        text += page.extract_text()
    return text

# --- ARAYÜZ (FRONTEND) ---
st.title("⚖️ SMTS Strateji Müqavilə Auditoru")
st.markdown("Müqaviləni yükləyin, süni intellekt riskləri analiz etsin.")

uploaded_file = st.file_uploader("Sənədi bura yükləyin (PDF və ya DOCX)", type=["docx", "pdf"])

if uploaded_file is not None:
    file_ext = os.path.splitext(uploaded_file.name)[1].lower()
    content = ""

    if file_ext == ".docx":
        content = read_word(uploaded_file)
    elif file_ext == ".pdf":
        content = read_pdf(uploaded_file)
    
    st.divider()
    st.subheader("🔍 Analiz Nəticələri")

    found_any = False
    for category, keywords in RISK_FOKUS.items():
        found_keywords = [word for word in keywords if word in content.lower()]
        
        if found_keywords:
            found_any = True
            with st.expander(f"🔴 DİQQƏT: {category}", expanded=True):
                st.write(f"**Aşkarlanan terminlər:** {', '.join(found_keywords)}")
                
                if category == "ƏDV Riskli Məqamlar":
                    st.info("💡 TÖVSİYƏ: Vergi Məcəlləsinin 175-ci maddəsinə uyğunluğu və e-qaimə tələblərini yoxlayın.")
                elif category == "Maliyyə Zərəri Riski":
                    st.warning("💡 TÖVSİYƏ: Cərimə faizlərinin mütənasibliyini və 'üst hədd' qoyulub-qoyulmadığını yoxlayın.")
    
    if not found_any:
        st.success("✅ Sənəddə kritik risk açar sözləri aşkar edilmədi.")