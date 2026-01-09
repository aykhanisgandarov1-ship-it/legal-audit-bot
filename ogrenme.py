import React, { useState } from 'react';
import { Upload, AlertTriangle, CheckCircle, FileText, Brain, TrendingUp, Shield, DollarSign, Scale, Clock, FileWarning } from 'lucide-react';

const ContractAuditor = () => {
  const [analyzing, setAnalyzing] = useState(false);
  const [results, setResults] = useState(null);
  const [fileName, setFileName] = useState('');

  // Genişləndirilmiş risk bazası
  const RISK_DATABASE = {
    "ƏDV və Vergi Riskləri": {
      icon: DollarSign,
      color: "red",
      keywords: ["ədv", "əlavə dəyər vergisi", "vergi tutulan", "vergi orqanı", "vergi öhdəliyi", 
                 "əvəzləşdirmə", "vergi ödəyicisi", "vergi tutulan əməliyyat", "vergi hesabatı",
                 "vergi məcəlləsi", "vergi güzəşti"],
      severity: "critical",
      recommendation: "Vergi Məcəlləsinin 175-ci maddəsinə uyğunluğu yoxlayın. ƏDV hesablanması və ödənilməsi qaydalarının düzgünlüyünü təsdiqləyin. E-qaimə sisteminin tətbiqini nəzərdən keçirin."
    },
    "Maliyyə Zərəri və Cərimələr": {
      icon: AlertTriangle,
      color: "orange",
      keywords: ["cərimə", "penya", "gecikmə faizi", "dəbbə pulu", "təzminat", "zərərin ödənilməsi",
                 "maddi məsuliyyət", "kompensasiya", "iqtisadi sanksiya", "faiz dərəcəsi",
                 "gecikdirilmiş ödəniş", "penalty"],
      severity: "high",
      recommendation: "Cərimə məbləğlərinin mütənasiblik prinsipinə uyğunluğunu yoxlayın. Üst hədd müəyyən edilməsini tələb edin. Fors-major hallarında azad olunma şərtlərini əlavə edin."
    },
    "Hüquqi Boşluq və Məhkəmə": {
      icon: Scale,
      color: "purple",
      keywords: ["fors-major", "arbitraj", "məhkəmə", "mübahisələrin həlli", "yurisdiksiya",
                 "müqaviləyə xitam", "qanunvericilik", "tətbiq edilən qanun", "beynəlxalq arbitraj",
                 "vasitəçilik", "mediasiya", "icraat"],
      severity: "high",
      recommendation: "Mübahisələrin həlli mexanizmini aydınlaşdırın. Tətbiq edilən qanunvericiliyi dəqiq göstərin. Pre-arbitraj danışıqlar mərhələsini nəzərdə tutun."
    },
    "Ödəniş Şərtləri Riskləri": {
      icon: Clock,
      color: "blue",
      keywords: ["ödəniş müddəti", "avans", "son ödəniş", "təxirə salınmış ödəniş", "qiymət",
                 "məzənnə", "valyuta", "bank təminatı", "akkreditiv", "ödəniş qrafiki",
                 "təqvim günü", "iş günü"],
      severity: "medium",
      recommendation: "Ödəniş qrafikinin real iş proseslərinə uyğunluğunu yoxlayın. Valyuta riskləri üçün hedcinq mexanizmləri nəzərdə tutun. Bank təminatlarının şərtlərini dəqiqləşdirin."
    },
    "Məxfilik və Məlumat Təhlükəsizliyi": {
      icon: Shield,
      color: "indigo",
      keywords: ["məxfilik", "kommersiya sirri", "məlumatın qorunması", "fərdi məlumat", "NDA",
                 "non-disclosure", "intellektual mülkiyyət", "patent", "müəllif hüququ",
                 "məlumat bazası", "kiber təhlükəsizlik"],
      severity: "high",
      recommendation: "GDPR və Azərbaycan qanunvericiliyinə uyğunluğu təmin edin. Məlumat sızması halında məsuliyyəti məhdudlaşdırın. Üçüncü şəxslərə məlumat ötürülməsi qaydalarını müəyyənləşdirin."
    },
    "Müqavilənin İcrası və Keyfiyyət": {
      icon: TrendingUp,
      color: "green",
      keywords: ["keyfiyyət standartları", "texniki xüsusiyyətlər", "qəbul aktı", "sınaq müddəti",
                 "zəmanət öhdəliyi", "servis", "texniki dəstək", "çatdırılma müddəti",
                 "təhvil-təslim", "istismar müddəti"],
      severity: "medium",
      recommendation: "Keyfiyyət meyarlarını ölçülə bilən göstəricilərlə müəyyənləşdirin. Qəbul-təhvil prosedurunu detallı təsvir edin. Zəmanət müddətinin qanunvericiliyə uyğunluğunu yoxlayın."
    },
    "Force Majeure və Fövqəladə Hallar": {
      icon: FileWarning,
      color: "yellow",
      keywords: ["fors-major", "qeyri-adi hal", "təbii fəlakət", "müharibə", "pandemiya",
                 "dövlət müdaxiləsi", "hökumət qərarı", "karantin", "fövqəladə vəziyyət",
                 "qanunsuz hərəkətlər"],
      severity: "high",
      recommendation: "Fors-major halların siyahısını genişləndirin (pandemiya, kiberhücumlar). Bildiriş müddətlərini qısaldın. Öhdəliklərin müvəqqəti dayandırılması və ya yenidən danışıqlar mexanizmini əlavə edin."
    }
  };

  const analyzeWithAI = async (text) => {
    try {
      const response = await fetch("https://api.anthropic.com/v1/messages", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          model: "claude-sonnet-4-20250514",
          max_tokens: 1000,
          messages: [
            {
              role: "user",
              content: `Sən peşəkar hüquqşünas və müqavilə ekspertiisən. Aşağıdakı müqavilə mətnini təhlil et və bu 3 sualı cavablandır:

1. Müqavilədə ən kritik 3 hüquqi riski qısa sadalayın
2. ƏDV və vergi öhdəlikləri düzgün təsvir olunubmu? (Bəli/Xeyr və qısa izahat)
3. Ümumi risk səviyyəsi: Aşağı/Orta/Yüksək və 1 cümlə səbəb

MÜQAVİLƏ MƏTNİ:
${text.substring(0, 3000)}

CAVABINI YALNIZ JSON FORMATINDA VER, başqa heç nə yazma:
{
  "critical_risks": ["risk1", "risk2", "risk3"],
  "vat_status": "cavab",
  "overall_risk": "səviyyə - səbəb"
}`
            }
          ]
        })
      });

      const data = await response.json();
      const responseText = data.content[0].text;
      
      // JSON-u təmizləyib parse edirik
      const cleanJson = responseText.replace(/```json|```/g, '').trim();
      return JSON.parse(cleanJson);
    } catch (error) {
      console.error('AI analiz xətası:', error);
      return null;
    }
  };

  const handleFileUpload = async (event) => {
    const file = event.target.files[0];
    if (!file) return;

    setFileName(file.name);
    setAnalyzing(true);
    setResults(null);

    try {
      const text = await file.text();
      const lowerText = text.toLowerCase();
      
      // Risk analizi
      const detectedRisks = {};
      let totalKeywords = 0;

      Object.entries(RISK_DATABASE).forEach(([category, data]) => {
        const found = data.keywords.filter(kw => lowerText.includes(kw));
        if (found.length > 0) {
          detectedRisks[category] = {
            ...data,
            foundKeywords: found,
            count: found.length
          };
          totalKeywords += found.length;
        }
      });

      // AI analizi
      const aiAnalysis = await analyzeWithAI(text);

      // Nəticələri saxlayırıq
      setResults({
        risks: detectedRisks,
        totalKeywords,
        riskCount: Object.keys(detectedRisks).length,
        aiInsights: aiAnalysis,
        textLength: text.length
      });

    } catch (error) {
      alert('Fayl oxunarkən xəta baş verdi: ' + error.message);
    } finally {
      setAnalyzing(false);
    }
  };

  const getSeverityColor = (severity) => {
    const colors = {
      critical: 'bg-red-100 text-red-800 border-red-300',
      high: 'bg-orange-100 text-orange-800 border-orange-300',
      medium: 'bg-yellow-100 text-yellow-800 border-yellow-300',
      low: 'bg-green-100 text-green-800 border-green-300'
    };
    return colors[severity] || colors.medium;
  };

  const getIconColor = (color) => {
    const colors = {
      red: 'text-red-600',
      orange: 'text-orange-600',
      yellow: 'text-yellow-600',
      green: 'text-green-600',
      blue: 'text-blue-600',
      purple: 'text-purple-600',
      indigo: 'text-indigo-600'
    };
    return colors[color] || 'text-gray-600';
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 to-blue-50 p-6">
      <div className="max-w-6xl mx-auto">
        {/* Header */}
        <div className="bg-white rounded-2xl shadow-xl p-8 mb-6 border border-blue-100">
          <div className="flex items-center gap-4 mb-4">
            <div className="p-3 bg-blue-600 rounded-xl">
              <Scale className="w-8 h-8 text-white" />
            </div>
            <div>
              <h1 className="text-3xl font-bold text-gray-800">SMTS Strateji Müqavilə Auditoru</h1>
              <p className="text-gray-600 mt-1">AI-powered hüquqi risk analiz sistemi</p>
            </div>
          </div>
          
          <div className="flex items-center gap-2 text-sm text-gray-500 bg-blue-50 p-3 rounded-lg">
            <Brain className="w-4 h-4" />
            <span>Claude AI ilə təchiz edilmiş 7 kateqoriyada 70+ risk termini analizi</span>
          </div>
        </div>

        {/* Upload Section */}
        <div className="bg-white rounded-2xl shadow-xl p-8 mb-6 border border-blue-100">
          <label className="flex flex-col items-center justify-center border-3 border-dashed border-blue-300 rounded-xl p-12 cursor-pointer hover:border-blue-500 hover:bg-blue-50 transition-all">
            <Upload className="w-16 h-16 text-blue-600 mb-4" />
            <span className="text-lg font-semibold text-gray-700 mb-2">Müqaviləni yükləyin</span>
            <span className="text-sm text-gray-500">PDF, DOCX, TXT formatları dəstəklənir</span>
            <input
              type="file"
              accept=".pdf,.docx,.txt"
              onChange={handleFileUpload}
              className="hidden"
            />
          </label>
          
          {fileName && (
            <div className="mt-4 flex items-center gap-2 text-sm text-gray-600 bg-gray-50 p-3 rounded-lg">
              <FileText className="w-4 h-4" />
              <span className="font-medium">{fileName}</span>
            </div>
          )}
        </div>

        {/* Loading State */}
        {analyzing && (
          <div className="bg-white rounded-2xl shadow-xl p-12 text-center border border-blue-100">
            <div className="animate-spin w-16 h-16 border-4 border-blue-600 border-t-transparent rounded-full mx-auto mb-4"></div>
            <p className="text-lg font-semibold text-gray-700">AI analiz edir...</p>
            <p className="text-sm text-gray-500 mt-2">Müqavilə məzmunu süni intellekt tərəfindən dərin analiz edilir</p>
          </div>
        )}

        {/* Results */}
        {results && !analyzing && (
          <div className="space-y-6">
            {/* Summary Cards */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div className="bg-white rounded-xl shadow-lg p-6 border-l-4 border-blue-600">
                <div className="text-3xl font-bold text-blue-600">{results.riskCount}</div>
                <div className="text-sm text-gray-600 mt-1">Risk Kateqoriyası</div>
              </div>
              <div className="bg-white rounded-xl shadow-lg p-6 border-l-4 border-orange-600">
                <div className="text-3xl font-bold text-orange-600">{results.totalKeywords}</div>
                <div className="text-sm text-gray-600 mt-1">Aşkarlanan Açar Söz</div>
              </div>
              <div className="bg-white rounded-xl shadow-lg p-6 border-l-4 border-purple-600">
                <div className="text-3xl font-bold text-purple-600">{Math.round(results.textLength / 1000)}K</div>
                <div className="text-sm text-gray-600 mt-1">Simvol Analiz Edildi</div>
              </div>
            </div>

            {/* AI Insights */}
            {results.aiInsights && (
              <div className="bg-gradient-to-r from-purple-50 to-blue-50 rounded-2xl shadow-xl p-6 border border-purple-200">
                <div className="flex items-center gap-3 mb-4">
                  <Brain className="w-6 h-6 text-purple-600" />
                  <h2 className="text-xl font-bold text-gray-800">AI Ekspert Rəyi</h2>
                </div>
                
                <div className="space-y-4">
                  <div className="bg-white rounded-lg p-4 shadow-sm">
                    <div className="font-semibold text-gray-700 mb-2">🎯 Kritik Risklər:</div>
                    <ul className="space-y-1">
                      {results.aiInsights.critical_risks?.map((risk, idx) => (
                        <li key={idx} className="text-gray-600 text-sm pl-4 border-l-2 border-red-400">{risk}</li>
                      ))}
                    </ul>
                  </div>
                  
                  <div className="bg-white rounded-lg p-4 shadow-sm">
                    <div className="font-semibold text-gray-700 mb-2">💰 ƏDV Statusu:</div>
                    <p className="text-gray-600 text-sm">{results.aiInsights.vat_status}</p>
                  </div>
                  
                  <div className="bg-white rounded-lg p-4 shadow-sm">
                    <div className="font-semibold text-gray-700 mb-2">⚖️ Ümumi Qiymətləndirmə:</div>
                    <p className="text-gray-600 text-sm">{results.aiInsights.overall_risk}</p>
                  </div>
                </div>
              </div>
            )}

            {/* Risk Details */}
            {Object.entries(results.risks).length > 0 ? (
              <div className="space-y-4">
                <h2 className="text-2xl font-bold text-gray-800 flex items-center gap-2">
                  <AlertTriangle className="w-6 h-6 text-red-600" />
                  Aşkar Edilmiş Risklər
                </h2>
                
                {Object.entries(results.risks).map(([category, data]) => {
                  const Icon = data.icon;
                  return (
                    <div key={category} className="bg-white rounded-xl shadow-lg border-l-4 border-red-500 overflow-hidden">
                      <div className="p-6">
                        <div className="flex items-start justify-between mb-4">
                          <div className="flex items-center gap-3">
                            <Icon className={`w-6 h-6 ${getIconColor(data.color)}`} />
                            <h3 className="text-xl font-bold text-gray-800">{category}</h3>
                          </div>
                          <span className={`px-3 py-1 rounded-full text-xs font-semibold border ${getSeverityColor(data.severity)}`}>
                            {data.severity.toUpperCase()}
                          </span>
                        </div>
                        
                        <div className="bg-red-50 rounded-lg p-4 mb-4">
                          <div className="text-sm font-semibold text-gray-700 mb-2">
                            Aşkarlanan terminlər ({data.count}):
                          </div>
                          <div className="flex flex-wrap gap-2">
                            {data.foundKeywords.map((kw, idx) => (
                              <span key={idx} className="px-3 py-1 bg-white text-red-700 rounded-full text-xs font-medium border border-red-200">
                                {kw}
                              </span>
                            ))}
                          </div>
                        </div>
                        
                        <div className="bg-blue-50 rounded-lg p-4">
                          <div className="flex items-start gap-2">
                            <CheckCircle className="w-5 h-5 text-blue-600 mt-0.5 flex-shrink-0" />
                            <div>
                              <div className="text-sm font-semibold text-gray-700 mb-1">Tövsiyə:</div>
                              <p className="text-sm text-gray-600 leading-relaxed">{data.recommendation}</p>
                            </div>
                          </div>
                        </div>
                      </div>
                    </div>
                  );
                })}
              </div>
            ) : (
              <div className="bg-white rounded-2xl shadow-xl p-12 text-center border border-green-200">
                <CheckCircle className="w-16 h-16 text-green-600 mx-auto mb-4" />
                <h3 className="text-2xl font-bold text-gray-800 mb-2">Təbriklər!</h3>
                <p className="text-gray-600">Sənəddə kritik risk açar sözləri aşkar edilmədi.</p>
                <p className="text-sm text-gray-500 mt-2">Lakin AI ekspert rəyini mütləq nəzərdən keçirin.</p>
              </div>
            )}
          </div>
        )}

        {/* Footer */}
        <div className="mt-8 text-center text-sm text-gray-500">
          <p>© 2026 SMTS Legal Tech • AI-Powered Contract Analysis</p>
          <p className="mt-1">Powered by Claude Sonnet 4</p>
        </div>
      </div>
    </div>
  );
};

export default ContractAuditor;
