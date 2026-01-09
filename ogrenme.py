import streamlit as st
import os
from docx import Document
import PyPDF2
import anthropic  # AI üçün

# --- SƏHİFƏ KONFİQURASİYASI ---
st.set_page_config(
    page_title="SMTS Legal Auditor",
    page_icon="⚖️",
    layout="wide"
)

# --- CSS İLƏ DİZAYN (React stilinə bənzətmək üçün) ---
st.markdown("""
    <style>
    .main {
        background-color: #f8f9fa;
    }
    .risk-box {
        padding: 20px;
        border-radius: 10px;
        margin-bottom: 15px;
        border-left: 5px solid;
    }
    .critical { border-color: #ff4b4b; background-color: #ffecec; }
    .high { border-color: #ffa500; background-color: #fff8e1; }
    .medium { border-color: #4b8bbe; background-color: #e8f4f8; }
    .stat-box {
        background-color: white;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.05);
        text-align: center;
    }
    </style>
""", unsafe_allow_html=True)

# --- RİSK BAZASI (Sizin React kodunuzdan köçürüldü) ---
RISK_DATABASE = {
    "ƏDV və Vergi Riskləri": {
        "color": "red",
        "keywords": ["ədv", "əlavə dəyər vergisi", "vergi tutulan", "vergi orqanı", "vergi öhdəliyi", 
                     "əvəzləşdirmə", "vergi ödəyicisi", "vergi tutulan əməliyyat", "vergi hesabatı"],
        "severity": "critical",
        "recommendation": "Vergi Məcəlləsinin 175-ci maddəsinə uyğunluğu yoxlayın. E-qaimə sisteminin tətbiqini nəzərdən keçirin."
    },
    "Maliyyə Zərəri və Cərimələr": {
        "color": "orange",
        "keywords": ["cərimə", "penya", "gecikmə faizi", "dəbbə pulu", "təzminat", "zərərin ödənilməsi", 
                     "maddi məsuliyyət", "kompensasiya", "iqtisadi sanksiya"],
        "severity": "high",
        "recommendation": "Cərimə məbləğlərinin mütənasiblik prinsipinə uyğunluğunu yoxlayın. Üst hədd (cap) tələb edin."
    },
    "Hüquqi Boşluq və Məhkəmə": {
        "color": "blue",
        "keywords": ["fors-major", "arbitraj", "məhkəmə", "mübahisələrin həlli", "yurisdiksiya", 
                     "müqaviləyə xitam", "tətbiq edilən qanun"],
        "severity": "high",
        "recommendation": "Mübahisələrin həlli mexanizmini aydınlaşdırın. Arbitraj yerini və dilini dəqiqləşdirin."
    },
    "Məxfilik və Təhlükəsizlik": {
        "color": "violet",
        "keywords": ["məxfilik", "kommersiya sirri", "məlumatın qorunması", "fərdi məlumat", "NDA", 
                     "konfidensiallıq", "kiber"],
        "severity": "medium",
        "recommendation": "Məlumat sızması halında məsuliyyəti məhdudlaşdırın. GDPR tələblərini yoxlayın."
    }
}

# --- FUNKSİYALAR ---

def read_file(uploaded_file):
    """Faylın növünə görə oxunması"""
    file_ext = os.path.splitext(uploaded_file.name)[1].lower()
    text = ""
    
    try:
        if file_ext == ".docx":
            doc = Document(uploaded_file)
            text = " ".join([para.text for para in doc.paragraphs])
        elif file_ext == ".pdf":
            reader = PyPDF2.PdfReader(uploaded_file)
            for page in reader.pages:
                text += page.extract_text()
        elif file_ext == ".txt":
            text = uploaded_file.read().decode("utf-8")
        else:
            return None, "Dəstəklənməyən format"
            
        return text, None
    except Exception as e:
        return None, str(e)

def analyze_risks(text):
    """Açar sözlərə görə risk analizi"""
    detected_risks = {}
    total_keywords = 0
    lower_text = text.lower()
    
    for category, data in RISK_DATABASE.items():
        found = [kw for kw in data["keywords"] if kw in lower_text]
        if found:
            detected_risks[category] = {
                **data,
                "found_keywords": found,
                "count": len(found)
            }
            total_keywords += len(found)
            
    return detected_risks, total_keywords

# --- UI (ARAYÜZ) HİSSƏSİ ---

# Yan Panel - API Key
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2240/2240728.png", width=80)
    st.title("Ayarlar")
    api_key = st.text_input("Anthropic API Key", type="password", help="AI analizi üçün açarı daxil edin")
    st.info("API açarı daxil edilməsə, yalnız açar söz analizi işləyəcək.")

# Başlıq
st.title("⚖️ SMTS Strateji Müqavilə Auditoru")
st.markdown("Bu sistem **Süni İntellekt** və **Hüquq Mühəndisliyi** prinsipləri əsasında işləyir.")

# Fayl Yükləmə
uploaded_file = st.file_uploader("Müqaviləni yükləyin (PDF, DOCX)", type=["pdf", "docx", "txt"])

if uploaded_file:
    with st.spinner("Sənəd oxunur və analiz edilir..."):
        # 1. Mətni oxu
        text_content, error = read_file(uploaded_file)
        
        if error:
            st.error(f"Xəta baş verdi: {error}")
        else:
            # 2. Risk Analizi et
            risks, total_count = analyze_risks(text_content)
            
            # 3. Statistika Blokları
            col1, col2, col3 = st.columns(3)
            col1.metric("📄 Sənəd Həcmi", f"{len(text_content)} simvol")
            col2.metric("🚩 Tapılan Risklər", f"{len(risks)} kateqoriya")
            col3.metric("🔍 Açar Sözlər", f"{total_count} ədəd")
            
            st.divider()

            # 4. AI Analizi (Əgər API Key varsa)
            if api_key:
                try:
                    client = anthropic.Anthropic(api_key=api_key)
                    prompt = f"""
                    Sən peşəkar hüquqşünassan. Bu müqavilə mətnini analiz et:
                    1. Ən kritik 3 riski qısa yaz.
                    2. ƏDV və vergi öhdəlikləri düzgündürmü?
                    3. Ümumi risk səviyyəsi (Aşağı/Orta/Yüksək) və səbəbi.
                    
                    Müqavilə mətni (ilk 5000 simvol):
                    {text_content[:5000]}
                    """
                    
                    message = client.messages.create(
                        model="claude-3-5-sonnet-20240620",
                        max_tokens=1000,
                        messages=[{"role": "user", "content": prompt}]
                    )
                    
                    st.subheader("🤖 Claude AI Ekspert Rəyi")
                    st.success(message.content[0].text)
                    
                except Exception as e:
                    st.warning(f"AI Analizi xətası: {e}")
            
            # 5. Risk Detalları (Sizin dizayna uyğun)
            st.subheader("📌 Detallı Risk Hesabatı")
            
            if not risks:
                st.success("✅ Təbriklər! Kritik açar sözlər tapılmadı.")
            
            for category, details in risks.items():
                # Rəng təyini
                sev_class = details['severity'] # critical, high, medium
                
                with st.expander(f"⚠️ {category} ({len(details['found_keywords'])} tapıntı)", expanded=True):
                    st.markdown(f"""
                    <div class="risk-box {sev_class}">
                        <b>Təhlükə dərəcəsi:</b> {details['severity'].upper()}<br>
                        <b>Aşkarlanan sözlər:</b> {', '.join(details['found_keywords'])}
                    </div>
                    """, unsafe_allow_html=True)
                    
                    st.info(f"💡 **TÖVSİYƏ:** {details['recommendation']}")
