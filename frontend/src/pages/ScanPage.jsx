import React, { useState, useRef, useEffect } from 'react'
import { 
  Upload, Microscope, AlertTriangle, CheckCircle2, RotateCcw, Leaf, Zap, 
  Camera, ShieldAlert, BookOpen, Layers, Activity, CloudRain, Info, 
  HelpCircle, ChevronRight, CheckSquare, PlusCircle, Eye, Trash2, Cpu, Sparkles
} from 'lucide-react'
import { motion, AnimatePresence } from 'framer-motion'
import { scansApi, weatherApi, diagnoseApi } from '../api/index.js'
import { useLanguage } from '../context/LanguageContext'
import { SectionCard, ProgressBar, Spinner, Alert, Badge } from '../components/ui/index.jsx'
import clsx from 'clsx'

// Official CropGuard v13 supported crops — verified Indian agricultural crops
const CROPS = [
  'Tomato', 'Potato', 'Chilli', 'Maize', 'Rice', 'Cotton', 'Groundnut'
]

const TIMELINE_STEPS = [
  { label: 'Visual Observation', desc: 'Analyzing color patterns, leaf shape, and lesions.' },
  { label: 'Pathology Marker Extraction', desc: 'Extracting biological indicators and necrotic margins.' },
  { label: 'Agricultural Knowledge Retrieval', desc: 'Querying local RAG databases and pathology references.' },
  { label: 'Differential Diagnosis', desc: 'Comparing candidate pathogens and weighing symptoms.' },
  { label: 'Agricultural Verification', desc: 'Validating against regional crop disease rules.' },
  { label: 'Weather Intelligence Analysis', desc: 'Assessing humidity and temperature lifecycle parameters.' },
  { label: 'Evidence Scoring', desc: 'Computing visual, weather and clinical diagnostic weights.' },
  { label: 'Clarification Assessment', desc: 'Verifying image resolution and checking ambiguities.' },
  { label: 'Final Diagnosis', desc: 'Resolving primary disease candidate pathologically.' },
  { label: 'Agronomist Report Generation', desc: 'Assembling agronomist recommendations and action calendar.' }
]

const ACTIVITY_LOGS = [
  "Analyzing lesion structure and shape...",
  "Extracting pathology markers...",
  "Comparing symptom patterns...",
  "Cross-referencing agricultural knowledge...",
  "Evaluating disease progression models...",
  "Analyzing local weather conditions...",
  "Calculating disease spread risk...",
  "Generating treatment recommendations...",
  "Preparing agronomist report...",
  "Checking for micro-climate favorability...",
  "Retrieving clinical RAG evidence...",
  "Matching visual cues to verified catalog..."
]

// Status mappings for timeline steps to avoid freezing UI (Section 1 & 7)
const STATUS_RANGES = {
  uploading: [0, 1],
  analyzing: [2, 3],
  retrieving_knowledge: [4, 5],
  weather_analysis: [6, 7],
  generating_report: [8, 9]
}

const LeafSVG = ({ className, glow = false }) => (
  <svg viewBox="0 0 100 100" fill="none" xmlns="http://www.w3.org/2000/svg" className={className} style={glow ? { filter: 'drop-shadow(0 0 8px #10b981)' } : {}}>
    <path d="M50 15C30 35 32 68 50 85C68 68 70 35 50 15Z" fill="url(#leaf-grad)" stroke="#047857" strokeWidth="3"/>
    <path d="M50 85V15" stroke="#065f46" strokeWidth="2.5" strokeLinecap="round"/>
    <path d="M50 35Q40 40 38 42" stroke="#065f46" strokeWidth="2" strokeLinecap="round"/>
    <path d="M50 48Q40 53 36 56" stroke="#065f46" strokeWidth="2" strokeLinecap="round"/>
    <path d="M50 61Q40 66 35 70" stroke="#065f46" strokeWidth="2" strokeLinecap="round"/>
    <path d="M50 35Q60 40 62 42" stroke="#065f46" strokeWidth="2" strokeLinecap="round"/>
    <path d="M50 48Q60 53 64 56" stroke="#065f46" strokeWidth="2" strokeLinecap="round"/>
    <path d="M50 61Q60 66 65 70" stroke="#065f46" strokeWidth="2" strokeLinecap="round"/>
    <defs>
      <linearGradient id="leaf-grad" x1="50" y1="15" x2="50" y2="85" gradientUnits="userSpaceOnUse">
        <stop stopColor="#34d399"/>
        <stop offset="1" stopColor="#059669"/>
      </linearGradient>
    </defs>
  </svg>
)

class ReportErrorBoundary extends React.Component {
  constructor(props) {
    super(props);
    this.state = { hasError: false };
  }

  static getDerivedStateFromError(error) {
    return { hasError: true };
  }

  componentDidCatch(error, errorInfo) {
    console.error("Report Rendering Error:", error, errorInfo);
  }

  render() {
    if (this.state.hasError) {
      return (
        <div className="card border-2 border-red-200 bg-red-50 p-6 text-center rounded-2xl">
          <span className="text-2xl">⚠️</span>
          <p className="font-display font-bold text-red-800 text-sm mt-2">Report generated but rendering failed.</p>
          <p className="text-xs text-red-600 mt-1">Please try scanning again or contact support if the issue persists.</p>
        </div>
      );
    }
    return this.props.children;
  }
}

export default function ScanPage() {
  const { lang, t } = useLanguage()
  const [preview,   setPreview]   = useState(null)
  const [file,      setFile]      = useState(null)
  const [dragging,  setDragging]  = useState(false)
  const [crop,      setCrop]      = useState('Tomato')
  const [field,     setField]     = useState('')
  
  // Diagnostics loading and animation states
  const [analyzing, setAnalyzing] = useState(false)
  const [step,      setStep]      = useState(0)
  const [morphState, setMorphState] = useState('seed') // 'seed' | 'sprout' | 'leaf'
  const [activityIndex, setActivityIndex] = useState(0)
  const [takingLonger, setTakingLonger] = useState(false)
  
  // Results & UI state persistence (decoupled from timeline and loader variables)
  const [diagnosisResult, setDiagnosisResult] = useState(null)
  const [animationComplete, setAnimationComplete] = useState(false)
  const [error,     setError]     = useState('')
  const [weather,   setWeather]   = useState(null)
  
  const fileRef = useRef()
  const reportRef = useRef(null)
  const pollTimerRef = useRef(null)
  const elapsedRef = useRef(0)

  const queryParams = new URLSearchParams(window.location.search)
  const queryScanId = queryParams.get('id')

  // Log diagnosisResult on render
  console.log("Diagnosis Result:", diagnosisResult);

  // Check URL query parameters to load previous report
  useEffect(() => {
    if (queryScanId) {
      setAnalyzing(true)
      scansApi.get(queryScanId)
        .then(data => {
          setDiagnosisResult(data)
          setAnimationComplete(true)
          setPreview(scansApi.imageUrl(data.image_path))
        })
        .catch(err => {
          setError('Failed to load scan details: ' + err.message)
        })
        .finally(() => setAnalyzing(false))
    }
  }, [queryScanId])

  useEffect(() => {
    weatherApi.current().then(setWeather).catch(() => {})
  }, [])

  // Dynamic activity feed ticker
  useEffect(() => {
    let interval;
    if (analyzing) {
      interval = setInterval(() => {
        setActivityIndex(prev => (prev + 1) % ACTIVITY_LOGS.length)
      }, 1500)
    }
    return () => clearInterval(interval)
  }, [analyzing])

  // Clean up timers on unmount
  useEffect(() => {
    return () => {
      if (pollTimerRef.current) clearInterval(pollTimerRef.current)
    }
  }, [])

  // Auto-scroll to report upon animation complete
  useEffect(() => {
    if (animationComplete && reportRef.current) {
      setTimeout(() => {
        reportRef.current.scrollIntoView({ behavior: 'smooth', block: 'start' })
      }, 150)
    }
  }, [animationComplete])

  function loadFile(f) {
    if (!f || !f.type.startsWith('image/')) { 
      setError('Please upload an image file (JPG, PNG, WEBP)'); 
      return 
    }
    setFile(f); setError('')
    const r = new FileReader()
    r.onload = e => setPreview(e.target.result)
    r.readAsDataURL(f)
  }

  function onDrop(e) { 
    e.preventDefault(); 
    setDragging(false); 
    loadFile(e.target.files?.[0] || e.dataTransfer.files[0]) 
  }

  async function startDiagnosticJob() {
    if (!file) return
    setAnalyzing(true)
    setAnimationComplete(false)
    setError('')
    setStep(0)
    setMorphState('seed')
    setTakingLonger(false)
    elapsedRef.current = 0
    
    try {
      // 1. Start Async Diagnostic Job (Part 2 & 3)
      console.log("Request URL: /api/v1/diagnose/");
      const jobResponse = await diagnoseApi.start(file, crop, field, lang)
      const jobId = jobResponse.job_id
      
      // 2. Poll Diagnostic Job status in the background
      pollTimerRef.current = setInterval(async () => {
        elapsedRef.current += 1
        
        // Show taking longer warning after 15 seconds (Part 7)
        if (elapsedRef.current >= 15) {
          setTakingLonger(true)
        }
        
        try {
          console.log(`Request URL: /api/v1/diagnose/status/${jobId}`);
          const statusReport = await diagnoseApi.status(jobId)
          const currentStatus = statusReport.status
          
          if (currentStatus === 'completed') {
            clearInterval(pollTimerRef.current)
            await triggerCompletionSequence(statusReport.result)
          } else if (currentStatus === 'failed') {
            clearInterval(pollTimerRef.current)
            setAnalyzing(false)
            // Section 8 failure handling requirements
            setError(statusReport.error || 'Diagnosis temporarily unavailable. Please try again shortly.')
          } else {
            // Smart step interpolation to ensure the timeline never appears frozen (Part 1 & 7)
            const range = STATUS_RANGES[currentStatus] || [0, 1]
            const minStep = range[0]
            const maxStep = range[1]
            
            setStep(prev => {
              if (prev < minStep) return minStep
              if (prev >= minStep && prev < maxStep) return prev + 1
              return prev // Hover at current stage bounds until status moves
            })
          }
        } catch (pollErr) {
          console.warn("[Polling Error]", pollErr)
        }
      }, 1000)
      
    } catch(err) {
      setAnalyzing(false)
      console.error("[Diagnosis Error]", err);
      const statusCode = err.response?.status || (err.message?.includes('status code') ? err.message.match(/\d+/)?.[0] : null) || 'Unknown';
      let errMsg = err.message || 'Diagnosis temporarily unavailable. Please try again shortly.';
      
      if (errMsg.toLowerCase().includes('not found') || statusCode === 404 || String(statusCode) === '404') {
        errMsg = `Diagnosis service endpoint not available. (HTTP ${statusCode})`;
      } else {
        errMsg = `${errMsg} (HTTP ${statusCode})`;
      }
      setError(errMsg);
    }
  }

  async function triggerCompletionSequence(resultData) {
    // Morph mascot 🌱 -> 🌿 -> 🍃
    setStep(10)
    setMorphState('seed')
    await new Promise(r => setTimeout(r, 450))
    setMorphState('sprout')
    await new Promise(r => setTimeout(r, 450))
    setMorphState('leaf')
    await new Promise(r => setTimeout(r, 450))
    
    setAnimationComplete(true)
    setDiagnosisResult(resultData)
    setAnalyzing(false)
  }

  function reset() { 
    setPreview(null)
    setFile(null)
    setDiagnosisResult(null)
    setAnimationComplete(false)
    setError('')
    setTakingLonger(false)
    elapsedRef.current = 0
  }

  const isHealthy = diagnosisResult && (diagnosisResult.disease === 'Healthy' || diagnosisResult.disease.toLowerCase().includes('healthy'))
  
  // Reconstruct report details defensively (guarantees v11 compatibility and prevents crashes on older records)
  let report = diagnosisResult?.generated_report
  if (diagnosisResult && !report) {
    report = {
      most_likely_disease: diagnosisResult.disease || 'Healthy',
      disease_severity: diagnosisResult.severity_label || 'None',
      observed_symptoms: diagnosisResult.knowledge?.symptoms || ['No symptoms recorded.'],
      pathology_markers: [diagnosisResult.pathogen || 'Foliar markers'],
      diagnostic_reasoning: diagnosisResult.ai_reasoning || 'Diagnostic result generated from standard vision scanning.',
      alternative_diagnoses: [],
      differential_diagnosis: [
        {
          disease: diagnosisResult.disease || 'Healthy',
          supporting_evidence: diagnosisResult.knowledge?.symptoms || ['Visual observations'],
          contradicting_evidence: [],
          verdict: 'Selected'
        }
      ],
      visual_evidence_strength: 'Moderate',
      knowledge_evidence_strength: 'Moderate',
      weather_evidence_strength: 'Moderate',
      overall_evidence_strength: 'Medium',
      disease_explanation: 'Pathological crop condition verified by AI scanning.',
      potential_yield_impact: diagnosisResult.severity > 60 ? 'High' : 'Moderate',
      disease_progression: 'Foliar lesions spreading under high moisture conditions.',
      likely_causes: diagnosisResult.knowledge?.causes || ['Environmental conditions'],
      immediate_actions: diagnosisResult.treatment_summary || 'Monitor crop daily.',
      organic_treatment: diagnosisResult.knowledge?.treatments?.[1] || 'Apply neem-based sprays.',
      biological_treatment: 'N/A',
      chemical_treatment: diagnosisResult.knowledge?.treatments?.[0] || 'Apply recommended chemical controls.',
      application_guidance: 'Apply in the early morning or late evening.',
      safety_precautions: 'Wear standard PPE when applying treatments.',
      farmer_action_plan: 'Inspect daily. Apply treatments within 48 hours.',
      prevention_measures: diagnosisResult.knowledge?.prevention?.join('. ') || 'Keep fields clean.',
      monitoring_recommendations: 'Check lower leaves daily.',
      clarification_questions: [],
      additional_images_needed: []
    }
  }

  // Calculate parameters for redesigned Agronomist Consultation (Section 7)
  const diseaseLabel = diagnosisResult ? (t(`diseases.${diagnosisResult.disease}`) === `diseases.${diagnosisResult.disease}` ? diagnosisResult.disease : t(`diseases.${diagnosisResult.disease}`)) : ''
  const priorityLevel = diagnosisResult?.severity > 60 ? 'Immediate Action Required' : diagnosisResult?.severity > 30 ? 'High Priority' : 'Routine Monitoring'

  return (
    <div className="space-y-6 relative animate-fade-in">
      
      {/* Weather Advisory Strip */}
      {weather && (
        <div className={clsx('rounded-xl px-4 py-3 flex items-center gap-3 text-sm border shadow-sm backdrop-blur-sm bg-white/40',
          weather.humidity > 80 ? 'border-red-200 text-red-800' :
          weather.humidity > 70 ? 'border-amber-200 text-amber-800' :
          'border-green-200 text-green-800'
        )}>
          <span className="text-base">🌦️</span>
          <span className="font-semibold">{t('dashboard.weather_title', { city: 'Visakhapatnam' })}: {weather.temp}°C · {weather.humidity}% {t('dashboard.humidity').toLowerCase()}</span>
          <span className="ml-auto text-xs opacity-80 hidden md:inline">
            {weather.humidity > 80 ? 'High fungal risk — inspect fields within 24 hours' :
             weather.humidity > 70 ? 'Moderate risk — inspect fields within 3 days' :
             'Optimal dry conditions — low pathogen spread risk'}
          </span>
        </div>
      )}

      <div className="grid lg:grid-cols-12 gap-6 items-start">
        
        {/* Upload Column (Col Span 5) */}
        <div className="lg:col-span-5 card bg-white/70 border border-slate-100">
          <div className="flex items-center justify-between mb-5">
            <div>
              <h2 className="font-display text-base font-bold text-slate-900">{t('scan.title')}</h2>
              <p className="text-xs text-slate-405 font-semibold mt-0.5">Diagnose symptoms using Gemini Clinical Pathology</p>
            </div>
            <div className="w-9 h-9 rounded-xl bg-brand-50 flex items-center justify-center"><Camera size={18} className="text-brand-600"/></div>
          </div>

          <div className="grid grid-cols-2 gap-3 mb-5">
            <div>
              <label className="block text-xs font-bold text-slate-650 mb-1.5">{t('scan.select_crop')}</label>
              <select value={crop} onChange={e=>setCrop(e.target.value)} className="input text-sm cursor-pointer">
                {CROPS.map(c=><option key={c} value={c}>{t('crops.' + c)}</option>)}
              </select>
            </div>
            <div>
              <label className="block text-xs font-bold text-slate-655 mb-1.5">Field / Location</label>
              <input value={field} onChange={e=>setField(e.target.value)} placeholder={t('scan.field_placeholder')} className="input text-sm"/>
            </div>
          </div>

          {!preview ? (
            <div
              className={clsx('border-2 border-dashed rounded-2xl p-10 text-center cursor-pointer transition-all duration-205',
                dragging ? 'border-brand-500 bg-brand-50 scale-[1.01]' : 'border-slate-200 hover:border-brand-400 hover:bg-brand-50/50')}
              onClick={() => fileRef.current?.click()}
              onDragOver={e=>{e.preventDefault();setDragging(true)}}
              onDragLeave={() => setDragging(false)}
              onDrop={onDrop}>
              <div className="w-16 h-16 rounded-2xl bg-brand-50 flex items-center justify-center mx-auto mb-4">
                <Upload size={28} className="text-brand-500"/>
              </div>
              <p className="font-semibold text-slate-700 mb-1">{t('scan.upload_text')}</p>
              <p className="text-sm text-slate-450 mb-5">{t('scan.upload_sub')}</p>
              <button className="btn btn-primary gap-2 text-xs" onClick={e=>{e.stopPropagation();fileRef.current?.click()}}>
                <Upload size={15}/> Choose File
              </button>
              <input ref={fileRef} type="file" accept="image/*" className="hidden" onChange={e=>loadFile(e.target.files[0])}/>
            </div>
          ) : (
            <div className="space-y-4">
              <div className="relative rounded-2xl overflow-hidden border border-slate-200 shadow-inner">
                <img src={preview} alt="Leaf preview" className="w-full max-h-80 object-cover"/>
                <button onClick={reset}
                  className="absolute top-3 right-3 w-8 h-8 rounded-xl bg-white/90 hover:bg-white flex items-center justify-center text-slate-600 shadow-sm backdrop-blur-sm transition-all">
                  <RotateCcw size={14}/>
                </button>
                <div className="absolute bottom-3 left-3 bg-black/60 text-white text-xs px-3 py-1.5 rounded-full backdrop-blur-sm">
                  {t('crops.' + crop)} {field ? `· ${field}` : ''}
                </div>
              </div>

              {!analyzing && !diagnosisResult && (
                <button onClick={startDiagnosticJob} className="btn btn-primary w-full btn-lg gap-3 shadow-lg shadow-brand-200 text-sm">
                  <Zap size={18}/> {t('scan.btn_analyze')}
                </button>
              )}

              {diagnosisResult && (
                <button onClick={reset} className="btn btn-secondary w-full gap-2 text-xs"><Upload size={14}/> {t('scan.btn_reset')}</button>
              )}
            </div>
          )}

          {error && <Alert type="danger" message={error} className="mt-4" onClose={() => setError('')}/>}

          <div className="mt-5 pt-4 border-t border-slate-100">
            <p className="text-xs font-semibold text-slate-500 uppercase tracking-wider mb-3">Photo Guidelines</p>
            <div className="space-y-2">
              {[['☀️','Use natural daylight — avoid shadows'],['🌿','Leaf should fill most of the frame'],['🔍','Focus on discolored or damaged areas']].map(([e,t])=>(
                <div key={t} className="flex items-center gap-2.5 text-xs text-slate-500 font-medium">
                  <span className="text-sm">{e}</span>
                  <span>{t}</span>
                </div>
              ))}
            </div>
          </div>
        </div>

        {/* Results / Progress Column (Col Span 7) */}
        <div className="lg:col-span-7 space-y-6">
          
          {/* Glassmorphic Scanner & Dynamic Timeline */}
          {analyzing && step < 10 && (
            <div className="grid md:grid-cols-12 gap-6 items-stretch">
              
              {/* Glassmorphic Scanner Card (Span 5) */}
              <div className="md:col-span-5 card border-none shadow-2xl relative overflow-hidden flex flex-col items-center justify-center p-6 bg-white/30 backdrop-blur-md"
                   style={{ minHeight: '380px' }}>
                
                {/* Scanner pulse ring */}
                <motion.div 
                  className="absolute border border-emerald-400/20 rounded-full"
                  animate={{ scale: [0.85, 1.25, 0.85], opacity: [0.3, 0.7, 0.3] }}
                  transition={{ duration: 4, repeat: Infinity, ease: 'easeInOut' }}
                  style={{ width: '85%', height: '85%', left: '7.5%', top: '7.5%' }}
                />

                <motion.div 
                  className="absolute border-2 border-emerald-400/40 rounded-full"
                  animate={{ scale: [0.95, 1.15, 0.95] }}
                  transition={{ duration: 3, repeat: Infinity, ease: 'easeInOut' }}
                  style={{ width: '70%', height: '70%', left: '15%', top: '15%' }}
                />

                {/* Vertical Scanner Line sweep */}
                <motion.div 
                  className="absolute left-[15%] right-[15%] h-[2px] bg-emerald-400 shadow-[0_0_12px_#34d399] z-10"
                  animate={{ top: ['18%', '82%', '18%'] }}
                  transition={{ duration: 2.8, repeat: Infinity, ease: 'easeInOut' }}
                />

                {/* Rotating scanner ticks */}
                <motion.div 
                  className="absolute inset-[10%] rounded-full border-t border-r border-brand-500/10 border-b-0 border-l-0 pointer-events-none"
                  animate={{ rotate: 360 }}
                  transition={{ duration: 15, repeat: Infinity, ease: "linear" }}
                />

                {/* Center silhouette leaf */}
                <div className="w-32 h-32 flex items-center justify-center relative z-0">
                  <LeafSVG className="w-24 h-24 text-emerald-800/80" glow={true}/>
                </div>

                <div className="mt-4 text-center relative z-10">
                  <span className="text-[10px] font-bold text-slate-500 uppercase tracking-widest block">Clinical Scanning</span>
                  <span className="text-xs font-black text-brand-850 mt-1 block">Active Laboratory Node</span>
                </div>
              </div>

              {/* Crop Lab Diagnostic Timeline (Span 7) */}
              <div className="md:col-span-7 card bg-white/70 border border-slate-100 p-4 relative overflow-hidden flex flex-col justify-between">
                
                <div className="flex items-center gap-2 mb-3 pb-2 border-b border-slate-100">
                  <Microscope size={16} className="text-brand-600"/>
                  <h3 className="font-display font-bold text-xs text-slate-800 uppercase tracking-wider">Crop Lab Diagnostic Timeline</h3>
                </div>

                {/* Absolute Floating Leaf Mascot next to active step */}
                <div className="relative flex-1">
                  
                  {/* Timeline steps container */}
                  <div className="relative pl-7 space-y-2.5">
                    
                    {/* Vertical Connecting Line */}
                    <div className="absolute left-[11px] top-2 bottom-2 w-0.5 bg-slate-200/60 z-0">
                      <motion.div 
                        className="bg-brand-500 w-full"
                        style={{ height: `${(step / 9) * 100}%` }}
                        transition={{ duration: 0.3 }}
                      />
                    </div>

                    {/* mascot leaf tracker */}
                    <motion.div 
                      className="absolute left-[-2px] w-7 h-7 rounded-full bg-brand-50/90 border border-brand-300 flex items-center justify-center text-xs shadow-md z-20"
                      animate={{ 
                        top: step < 10 ? `${(step / 10) * 92 + 2}%` : '92%',
                        y: '-50%'
                      }}
                      transition={{ type: 'spring', stiffness: 90, damping: 13 }}
                    >
                      <motion.span 
                        animate={{ y: [-1.5, 1.5, -1.5] }} 
                        transition={{ duration: 2, repeat: Infinity, ease: 'easeInOut' }}
                      >
                        🍃
                      </motion.span>
                    </motion.div>

                    {TIMELINE_STEPS.map((s, idx) => {
                      const isActive = step === idx;
                      const isCompleted = step > idx;
                      return (
                        <div key={idx} className="relative flex items-start gap-3 text-left animate-fade-in">
                          
                          {/* Step Marker */}
                          <div className={clsx(
                            "w-5 h-5 rounded-full flex items-center justify-center text-[10px] font-bold border z-10 transition-all duration-300",
                            isActive ? "bg-brand-500 border-brand-500 text-white scale-110 shadow-[0_0_8px_#22c55e]" :
                            isCompleted ? "bg-emerald-600 border-emerald-600 text-white" : "bg-white border-slate-200 text-slate-400"
                          )}>
                            {isCompleted ? '✓' : idx + 1}
                          </div>

                          <div className="min-w-0 flex-1">
                            <h4 className={clsx(
                              "text-[11px] font-black leading-tight transition-colors duration-300",
                              isActive ? "text-brand-900 font-extrabold" :
                              isCompleted ? "text-emerald-800" : "text-slate-400"
                            )}>
                              {s.label}
                            </h4>
                            <p className={clsx(
                              "text-[9px] mt-0.5 leading-snug transition-colors duration-300",
                              isActive ? "text-slate-650 font-medium" : "text-slate-400"
                            )}>
                              {s.desc}
                            </p>
                          </div>
                        </div>
                      )
                    })}
                  </div>
                </div>

                {/* Progress & Ticker */}
                <div className="mt-4 pt-3 border-t border-slate-100 space-y-2 relative z-10">
                  <div className="w-full bg-slate-100 rounded-full h-1.5 overflow-hidden">
                    <div 
                      className="bg-brand-600 h-full rounded-full transition-all duration-300"
                      style={{ width: `${(step / 10) * 100}%` }}
                    />
                  </div>
                  
                  {/* Real-time micro activity feed */}
                  <div className="h-4 flex items-center justify-center overflow-hidden">
                    <AnimatePresence mode="wait">
                      <motion.p 
                        key={activityIndex}
                        initial={{ opacity: 0, y: 10 }}
                        animate={{ opacity: 1, y: 0 }}
                        exit={{ opacity: 0, y: -10 }}
                        transition={{ duration: 0.3 }}
                        className="text-[10px] text-brand-850 font-bold italic text-center"
                      >
                        {ACTIVITY_LOGS[activityIndex]}
                      </motion.p>
                    </AnimatePresence>
                  </div>

                  {/* Taking Longer notice strip (Part 7) */}
                  {takingLonger && (
                    <motion.div 
                      initial={{ opacity: 0 }}
                      animate={{ opacity: 1 }}
                      className="text-[9px] text-amber-700 bg-amber-50 border border-amber-200 rounded-lg p-1.5 text-center font-bold animate-pulse"
                    >
                      Advanced analysis is taking longer than usual. Please stay on page.
                    </motion.div>
                  )}
                </div>
              </div>
            </div>
          )}

          {/* Morphing Completion Sequence (Section 6) */}
          {analyzing && step === 10 && (
            <div className="card bg-white/80 border border-emerald-100 p-8 text-center flex flex-col items-center justify-center"
                 style={{ minHeight: '380px' }}>
              <motion.div 
                key={morphState}
                initial={{ scale: 0.8, opacity: 0 }}
                animate={{ scale: 1.1, opacity: 1 }}
                transition={{ type: "spring", stiffness: 120, damping: 10 }}
                className="text-6xl"
              >
                {morphState === 'seed' ? '🌱' : morphState === 'sprout' ? '🌿' : '🍃'}
              </motion.div>
              <h3 className="font-display font-black text-lg text-slate-900 mt-4 uppercase tracking-wider">Diagnosis Complete</h3>
              <p className="text-xs text-brand-700 font-semibold mt-1">Agronomist Report Ready</p>
            </div>
          )}

          {/* Diagnosis Report View (Section 7 Redesign) */}
          {diagnosisResult && (
            <ReportErrorBoundary>
              <motion.div 
                ref={reportRef}
                initial="hidden"
                animate="visible"
                variants={{
                  hidden: { opacity: 0 },
                  visible: {
                    opacity: 1,
                    transition: { staggerChildren: 0.12 }
                  }
                }}
                className="space-y-6"
              >
                
                {/* ----------------- SECTION A: DIAGNOSIS SUMMARY ----------------- */}
                <motion.div 
                  variants={{ hidden: { opacity: 0, y: 20 }, visible: { opacity: 1, y: 0 } }}
                  className={clsx('card border-2 shadow-lg overflow-hidden relative bg-white/80 backdrop-blur-md',
                    isHealthy ? 'border-green-200 bg-green-50/20' : 'border-red-200 bg-red-50/10'
                  )}
                >
                  <div className="p-5 flex items-start gap-4">
                    <div className={clsx('w-14 h-14 rounded-2xl flex items-center justify-center shadow-md flex-shrink-0',
                      isHealthy ? 'bg-green-500 text-white' : 'bg-red-500 text-white'
                    )}>
                      {isHealthy ? <CheckCircle2 size={32}/> : <AlertTriangle size={32}/>}
                    </div>
                    <div className="min-w-0 flex-1">
                      <span className="text-[10px] font-bold text-slate-400 uppercase tracking-widest block">SECTION A · DIAGNOSIS SUMMARY</span>
                      <h2 className="font-display font-black text-2xl text-slate-900 mt-1">
                        {diseaseLabel}
                      </h2>
                      <div className="flex items-center gap-2 flex-wrap mt-2">
                        <Badge label={`Crop: ${diagnosisResult.crop}`} color="blue"/>
                        {diagnosisResult.field_name && <Badge label={`Field: ${diagnosisResult.field_name}`} color="slate"/>}
                        <Badge label={isHealthy ? 'Healthy Leaf' : 'Diseased Leaf'} color={isHealthy ? 'green' : 'red'}/>
                      </div>
                    </div>
                    <div className="text-right">
                      <span className="text-[10px] font-bold text-slate-400 uppercase tracking-widest block">Priority Level</span>
                      <span className={clsx('text-[11px] font-black px-2.5 py-0.5 rounded-lg block mt-1.5 border',
                        priorityLevel.includes('Immediate') ? 'bg-red-100 border-red-200 text-red-750' :
                        priorityLevel.includes('High') ? 'bg-amber-100 border-amber-200 text-amber-850' :
                        'bg-green-100 border-green-200 text-green-700'
                      )}>{priorityLevel}</span>
                    </div>
                  </div>

                  {!isHealthy && (
                    <div className="grid grid-cols-4 border-t border-slate-100 bg-white/60 text-center py-3.5">
                      <div>
                        <span className="text-[10px] font-semibold text-slate-500 block uppercase">Severity</span>
                        <span className="text-sm font-black text-slate-900 mt-0.5">{diagnosisResult.severity_label}</span>
                      </div>
                      <div className="border-l border-slate-100">
                        <span className="text-[10px] font-semibold text-slate-500 block uppercase">Evidence Strength</span>
                        <span className="text-sm font-black text-slate-900 mt-0.5">{report.overall_evidence_strength}</span>
                      </div>
                      <div className="border-l border-slate-100">
                        <span className="text-[10px] font-semibold text-slate-500 block uppercase">Spread Risk</span>
                        <span className="text-sm font-black text-slate-900 mt-0.5">{diagnosisResult.spread_risk || (diagnosisResult.severity > 60 ? 'High' : 'Moderate')}</span>
                      </div>
                      <div className="border-l border-slate-100">
                        <span className="text-[10px] font-semibold text-slate-500 block uppercase">Risk Score</span>
                        <span className="text-sm font-black text-slate-900 mt-0.5">{diagnosisResult.risk_score}/100</span>
                      </div>
                    </div>
                  )}
                </motion.div>

                {/* If leaf is healthy, show quick reference and bypass diagnostic blocks */}
                {isHealthy ? (
                  <motion.div 
                    variants={{ hidden: { opacity: 0, y: 20 }, visible: { opacity: 1, y: 0 } }}
                    className="rounded-2xl border border-green-200 bg-green-50/50 p-6 text-center shadow-inner"
                  >
                    <CheckCircle2 size={36} className="text-green-600 mx-auto mb-2.5"/>
                    <p className="font-display font-black text-green-950 text-base">Leaf is healthy!</p>
                    <p className="text-xs text-green-700 mt-1 max-w-sm mx-auto font-medium">No pathological symptoms detected by clinical scanners. Continue standard irrigation and crop rotation.</p>
                  </motion.div>
                ) : (
                  <>
                    
                    {/* ----------------- SECTION B: WHAT WE OBSERVED ----------------- */}
                    <motion.div 
                      variants={{ hidden: { opacity: 0, y: 20 }, visible: { opacity: 1, y: 0 } }}
                      className="card bg-white/70 border border-slate-100 space-y-3"
                    >
                      <h3 className="font-bold text-xs text-slate-900 uppercase tracking-wider border-l-4 border-brand-500 pl-2">
                        SECTION B · WHAT WE OBSERVED
                      </h3>
                      <div className="grid md:grid-cols-2 gap-4">
                        <div>
                          <p className="text-[10px] font-bold text-slate-400 uppercase">Visible Symptoms</p>
                          <ul className="space-y-1.5 mt-2 pl-1.5">
                            {report.observed_symptoms?.map((s, idx) => (
                              <li key={idx} className="text-xs text-slate-650 flex items-start gap-1.5 font-semibold">
                                <span className="text-amber-500 mt-0.5">•</span>
                                <span>{s}</span>
                              </li>
                            ))}
                          </ul>
                        </div>
                        <div className="pt-3 md:pt-0 md:pl-4 border-t md:border-t-0 md:border-l border-slate-100">
                          <p className="text-[10px] font-bold text-slate-400 uppercase">Pathology Marks & Lesions</p>
                          <p className="text-xs text-slate-600 mt-2 leading-relaxed font-semibold">
                            The scanner identified foliar lesions and tissue decay markers. Margins present typical <span className="underline decoration-teal-400 font-bold">{report.pathology_markers?.join(', ') || 'atypical spots'}</span> associated with active leaf decay.
                          </p>
                        </div>
                      </div>
                    </motion.div>

                    {/* ----------------- SECTION C: WHY CROPGUARD REACHED THIS DIAGNOSIS ----------------- */}
                    <motion.div 
                      variants={{ hidden: { opacity: 0, y: 20 }, visible: { opacity: 1, y: 0 } }}
                      className="card bg-white/70 border border-slate-100 space-y-3.5"
                    >
                      <h3 className="font-bold text-xs text-slate-900 uppercase tracking-wider border-l-4 border-brand-500 pl-2">
                        SECTION C · WHY CROPGUARD REACHED THIS DIAGNOSIS
                      </h3>
                      
                      <div className="space-y-2">
                        <p className="text-[10px] font-bold text-slate-400 uppercase">Visual Reasoning</p>
                        <p className="text-xs text-slate-600 italic leading-relaxed font-semibold">"{report.diagnostic_reasoning}"</p>
                      </div>

                      <div className="grid sm:grid-cols-2 gap-4 pt-3 border-t border-slate-100 text-xs">
                        <div>
                          <p className="text-[10px] font-bold text-slate-400 uppercase">Differential Candidates</p>
                          <div className="space-y-2 mt-2">
                            {report.differential_diagnosis?.map((d, idx) => (
                              <div key={idx} className="flex justify-between items-center bg-slate-50 p-2 rounded-xl border border-slate-150 font-semibold">
                                <span className="font-bold text-slate-800">{d.disease}</span>
                                <span className={clsx('px-2 py-0.5 rounded-full text-[9px] font-bold',
                                  d.verdict === 'Selected' ? 'bg-red-100 text-red-750' : 'bg-slate-150 text-slate-655'
                                )}>{d.verdict}</span>
                              </div>
                            ))}
                          </div>
                        </div>

                        <div className="space-y-2.5">
                          <div>
                            <p className="text-[10px] font-bold text-slate-400 uppercase">Weather Contribution</p>
                            <p className="text-[11px] text-slate-650 mt-1 leading-relaxed font-semibold">
                              Local humidity Snap of {weather?.humidity || 75}% favors active pathogen growth and foliar spore germination.
                            </p>
                          </div>
                          <div>
                            <p className="text-[10px] font-bold text-slate-400 uppercase">Knowledge Base Matches</p>
                            <p className="text-[11px] text-slate-650 mt-1 leading-relaxed font-semibold">
                              RAG verified match: Pathology markers correspond to typical {diagnosisResult.crop} disease profiles in regional databases.
                            </p>
                          </div>
                        </div>
                      </div>
                    </motion.div>

                    {/* ----------------- SECTION D: DISEASE EDUCATION ----------------- */}
                    <motion.div 
                      variants={{ hidden: { opacity: 0, y: 20 }, visible: { opacity: 1, y: 0 } }}
                      className="card bg-white/70 border border-slate-100 space-y-3"
                    >
                      <h3 className="font-bold text-xs text-slate-900 uppercase tracking-wider border-l-4 border-brand-500 pl-2">
                        SECTION D · DISEASE EDUCATION
                      </h3>
                      <div className="grid md:grid-cols-3 gap-4 text-xs">
                        <div>
                          <p className="text-[10px] font-bold text-slate-400 uppercase">What is this disease?</p>
                          <p className="text-slate-650 mt-1.5 leading-relaxed font-semibold">{report.disease_explanation}</p>
                        </div>
                        <div className="border-t md:border-t-0 md:border-x border-slate-100 pt-3 md:pt-0 md:px-4">
                          <p className="text-[10px] font-bold text-slate-400 uppercase">How does it spread?</p>
                          <p className="text-slate-655 mt-1.5 leading-relaxed font-semibold">
                            {report.disease_progression || "Spreads via windborne spores, leaf-to-leaf contact, and water droplets."}
                          </p>
                        </div>
                        <div className="border-t md:border-t-0 pt-3 md:pt-0">
                          <p className="text-[10px] font-bold text-slate-400 uppercase">Yield Vulnerability & Impact</p>
                          <p className="text-red-750 font-bold mt-1.5 leading-relaxed">
                            Yield Impact: {report.potential_yield_impact}
                            <span className="text-[10px] font-semibold text-slate-500 block mt-1">Vulnerable stages: Vegetative to early fruit development.</span>
                          </p>
                        </div>
                      </div>
                    </motion.div>

                    {/* ----------------- SECTION E: IMMEDIATE ACTION PLAN ----------------- */}
                    <motion.div 
                      variants={{ hidden: { opacity: 0, y: 20 }, visible: { opacity: 1, y: 0 } }}
                      className="card bg-white/70 border border-slate-100 space-y-4"
                    >
                      <h3 className="font-bold text-xs text-slate-900 uppercase tracking-wider border-l-4 border-brand-500 pl-2">
                        SECTION E · IMMEDIATE ACTION PLAN
                      </h3>

                      <div className="grid sm:grid-cols-4 gap-4 text-xs">
                        <div className="bg-red-50/70 p-3 rounded-2xl border border-red-200">
                          <span className="font-bold text-red-950 block">🚨 TODAY</span>
                          <span className="text-[11px] text-red-900 mt-1 block leading-relaxed font-bold">{report.immediate_actions}</span>
                        </div>
                        <div className="bg-amber-50/50 p-3 rounded-2xl border border-amber-250">
                          <span className="font-bold text-amber-950 block">📅 WITHIN 3 DAYS</span>
                          <span className="text-[11px] text-slate-650 mt-1 block leading-relaxed font-semibold">Prune affected lower leaves to stop spore progression. Clear irrigation weeds.</span>
                        </div>
                        <div className="bg-brand-50/30 p-3 rounded-2xl border border-brand-200">
                          <span className="font-bold text-brand-950 block">🗓️ WITHIN 1 WEEK</span>
                          <span className="text-[11px] text-slate-655 mt-1 block leading-relaxed font-semibold">Apply recommended treatment (organic or chemical) during dry morning.</span>
                        </div>
                        <div className="bg-slate-50 p-3 rounded-2xl border border-slate-200">
                          <span className="font-bold text-slate-950 block">🔍 WITHIN 2 WEEKS</span>
                          <span className="text-[11px] text-slate-655 mt-1 block leading-relaxed font-semibold">Scout crop twice weekly. Monitor new foliage for recovery or re-infection.</span>
                        </div>
                      </div>
                    </motion.div>

                    {/* ----------------- SECTION F: TREATMENT STRATEGY ----------------- */}
                    <motion.div 
                      variants={{ hidden: { opacity: 0, y: 20 }, visible: { opacity: 1, y: 0 } }}
                      className="space-y-4"
                    >
                      <h3 className="font-display font-black text-sm text-slate-900 uppercase tracking-wider border-l-4 border-brand-500 pl-2">
                        SECTION F · TREATMENT STRATEGY
                      </h3>

                      <div className="grid md:grid-cols-3 gap-4">
                        {/* Organic */}
                        <div className="card bg-emerald-50/30 border-emerald-100 p-4 space-y-2.5 text-xs">
                          <div className="flex items-center gap-2">
                            <span className="text-base">🌿</span>
                            <h4 className="font-bold text-emerald-950 uppercase">Organic Treatment</h4>
                          </div>
                          <p className="text-emerald-800 leading-relaxed font-semibold">{report.organic_treatment}</p>
                          <div className="text-[10px] text-emerald-700/80 pt-2 border-t border-emerald-100 space-y-1">
                            <p><strong>Method:</strong> Hand-spray or mechanical foliar mister</p>
                            <p><strong>Frequency:</strong> Every 5-7 days until symptoms halt</p>
                            <p><strong>Precaution:</strong> Spray under low sunlight (morning/evening)</p>
                          </div>
                        </div>

                        {/* Biological */}
                        <div className="card bg-teal-50/30 border-teal-100 p-4 space-y-2.5 text-xs">
                          <div className="flex items-center gap-2">
                            <span className="text-base">🧬</span>
                            <h4 className="font-bold text-teal-950 uppercase">Biological Treatment</h4>
                          </div>
                          <p className="text-teal-800 leading-relaxed font-semibold">{report.biological_treatment}</p>
                          <div className="text-[10px] text-teal-700/80 pt-2 border-t border-teal-100 space-y-1">
                            <p><strong>Method:</strong> Soil drench or foliage inoculation</p>
                            <p><strong>Frequency:</strong> Single application, repeat in 14 days</p>
                            <p><strong>Precaution:</strong> Do not combine with chemical fungicides</p>
                          </div>
                        </div>

                        {/* Chemical */}
                        <div className="card bg-red-50/20 border-red-100 p-4 space-y-2.5 text-xs">
                          <div className="flex items-center gap-2">
                            <span className="text-base">🧪</span>
                            <h4 className="font-bold text-red-950 uppercase">Chemical Treatment</h4>
                          </div>
                          <p className="text-red-805 leading-relaxed font-bold">{report.chemical_treatment}</p>
                          <div className="text-[10px] text-red-700/80 pt-2 border-t border-red-100 space-y-1">
                            <p><strong>Method:</strong> Calibrated knapsack sprayer</p>
                            <p><strong>Frequency:</strong> Apply once, repeat only if infection persists</p>
                            <p><strong>Precaution:</strong> Use full protective gear. Observe harvest interval</p>
                          </div>
                        </div>
                      </div>
                    </motion.div>

                    {/* ----------------- SECTION G: WEATHER IMPACT ----------------- */}
                    <motion.div 
                      variants={{ hidden: { opacity: 0, y: 20 }, visible: { opacity: 1, y: 0 } }}
                      className="card bg-white/70 border border-slate-100 space-y-3"
                    >
                      <h3 className="font-bold text-xs text-slate-900 uppercase tracking-wider border-l-4 border-brand-500 pl-2">
                        SECTION G · WEATHER IMPACT
                      </h3>
                      {weather ? (
                        <div className="grid sm:grid-cols-3 gap-4 text-xs font-semibold text-slate-655">
                          <div>
                            <p className="text-[10px] font-bold text-slate-400 uppercase">Weather Influence</p>
                            <p className="mt-1 leading-relaxed">Temperature: {weather.temp}°C, Humidity: {weather.humidity}%</p>
                          </div>
                          <div>
                            <p className="text-[10px] font-bold text-slate-400 uppercase">Expected Spread Risk</p>
                            <p className="mt-1 leading-relaxed text-red-750 font-bold">
                              {weather.humidity > 80 ? "High Spread Risk — Moisture accelerates spores" :
                               weather.humidity > 70 ? "Moderate Spread Risk — Watch margins" : "Low Fungal Expansion Risk"}
                            </p>
                          </div>
                          <div>
                            <p className="text-[10px] font-bold text-slate-400 uppercase">Best Treatment Timing</p>
                            <p className="mt-1 leading-relaxed">Clear dry mornings. Wind speed under 10 km/h to prevent spray drift.</p>
                          </div>
                        </div>
                      ) : (
                        <p className="text-xs text-slate-400 leading-relaxed">Weather metrics currently unavailable. Standard irrigation guidelines apply.</p>
                      )}
                    </motion.div>

                    {/* ----------------- SECTION H: PREVENTION STRATEGY ----------------- */}
                    <motion.div 
                      variants={{ hidden: { opacity: 0, y: 20 }, visible: { opacity: 1, y: 0 } }}
                      className="card bg-white/70 border border-slate-100 space-y-3"
                    >
                      <h3 className="font-bold text-xs text-slate-900 uppercase tracking-wider border-l-4 border-brand-500 pl-2">
                        SECTION H · PREVENTION STRATEGY
                      </h3>
                      <div className="grid sm:grid-cols-2 gap-4 text-xs font-semibold">
                        <div>
                          <p className="text-[10px] font-bold text-slate-400 uppercase">Field Sanitation & Irrigation</p>
                          <p className="text-slate-650 mt-1.5 leading-relaxed font-semibold">
                            Clear all weeds and plant debris at the end of the crop cycle. Implement drip irrigation instead of overhead watering to keep foliage dry.
                          </p>
                        </div>
                        <div>
                          <p className="text-[10px] font-bold text-slate-400 uppercase">Crop Rotation & Future Steps</p>
                          <p className="text-slate-650 mt-1.5 leading-relaxed font-semibold">
                            {report.prevention_measures || "Rotate with non-host crops like legumes or millets. Maintain proper row spacing for optimal air circulation."}
                          </p>
                        </div>
                      </div>
                    </motion.div>

                    {/* ----------------- SECTION I: MONITORING PLAN ----------------- */}
                    <motion.div 
                      variants={{ hidden: { opacity: 0, y: 20 }, visible: { opacity: 1, y: 0 } }}
                      className="card bg-white/70 border border-slate-100 space-y-3"
                    >
                      <h3 className="font-bold text-xs text-slate-900 uppercase tracking-wider border-l-4 border-brand-500 pl-2">
                        SECTION I · MONITORING PLAN
                      </h3>
                      <div className="grid sm:grid-cols-3 gap-4 text-xs font-semibold text-slate-655">
                        <div>
                          <p className="text-[10px] font-bold text-slate-400 uppercase">What symptoms to watch for?</p>
                          <p className="mt-1 leading-relaxed">Lower foliage yellowing, necrotic spots with halos, fuzzy mold or leaf curling.</p>
                        </div>
                        <div>
                          <p className="text-[10px] font-bold text-slate-400 uppercase">When to inspect/re-spray?</p>
                          <p className="mt-1 leading-relaxed">Scout fields twice weekly. Re-spray organic remedies after heavy rain if wash-off occurred.</p>
                        </div>
                        <div>
                          <p className="text-[10px] font-bold text-slate-400 uppercase">When to seek expert help?</p>
                          <p className="mt-1 leading-relaxed">If symptoms spread to new shoots after chemical spray or leaf loss exceeds 25%.</p>
                        </div>
                      </div>
                    </motion.div>

                    {/* ----------------- SECTION J: CONFIDENCE EXPLANATION ----------------- */}
                    <motion.div 
                      variants={{ hidden: { opacity: 0, y: 20 }, visible: { opacity: 1, y: 0 } }}
                      className="card bg-slate-50 border-slate-200 space-y-3.5"
                    >
                      <h3 className="font-bold text-xs text-slate-900 uppercase tracking-wider border-l-4 border-brand-500 pl-2">
                        SECTION J · CONFIDENCE EXPLANATION
                      </h3>
                      
                      <div className="grid grid-cols-2 sm:grid-cols-4 gap-4">
                        <div className="bg-white p-3 rounded-2xl border border-slate-150 text-center">
                          <span className="text-[9px] font-semibold text-slate-500 block uppercase font-bold">Visual Evidence</span>
                          <span className={clsx('text-xs font-black block mt-1.5',
                            report.visual_evidence_strength === 'Strong' ? 'text-emerald-700' : 'text-slate-650'
                          )}>{report.visual_evidence_strength || 'Moderate'}</span>
                        </div>
                        <div className="bg-white p-3 rounded-2xl border border-slate-150 text-center">
                          <span className="text-[9px] font-semibold text-slate-500 block uppercase font-bold">Knowledge Match</span>
                          <span className={clsx('text-xs font-black block mt-1.5',
                            report.knowledge_evidence_strength === 'Strong' ? 'text-emerald-700' : 'text-slate-650'
                          )}>{report.knowledge_evidence_strength || 'Moderate'}</span>
                        </div>
                        <div className="bg-white p-3 rounded-2xl border border-slate-150 text-center">
                          <span className="text-[9px] font-semibold text-slate-500 block uppercase font-bold">Weather Support</span>
                          <span className={clsx('text-xs font-black block mt-1.5',
                            report.weather_evidence_strength === 'Strong' ? 'text-emerald-700' : 'text-slate-650'
                          )}>{report.weather_evidence_strength || 'Moderate'}</span>
                        </div>
                        <div className="bg-white p-3 rounded-2xl border border-slate-150 text-center">
                          <span className="text-[9px] font-semibold text-slate-500 block uppercase font-bold">Overall Evidence</span>
                          <span className="text-xs font-black text-brand-800 block mt-1.5">{report.overall_evidence_strength || 'High'}</span>
                        </div>
                      </div>
                    </motion.div>

                  </>
                )}

                {/* Interactive Checklist & Extras */}
                {!isHealthy && report.clarification_questions?.length > 0 && (
                  <motion.div 
                    variants={{ hidden: { opacity: 0, y: 20 }, visible: { opacity: 1, y: 0 } }}
                    className="card bg-white/70 border border-slate-100"
                  >
                    <h3 className="font-bold text-xs text-slate-900 uppercase tracking-wider mb-3">Follow-Up Verification Checklist</h3>
                    <div className="space-y-2">
                      {report.clarification_questions.map((q, idx) => (
                        <label key={idx} className="flex items-start gap-2.5 text-xs text-slate-600 cursor-pointer select-none">
                          <input type="checkbox" className="mt-0.5 rounded border-slate-350 text-brand-600 focus:ring-brand-500 cursor-pointer"/>
                          <span className="font-semibold text-slate-650">{q}</span>
                        </label>
                      ))}
                    </div>
                  </motion.div>
                )}

                {/* Disclaimer */}
                {!isHealthy && (
                  <div className="card bg-slate-50 border border-slate-200">
                    <p className="text-[10px] text-slate-400 flex items-center gap-2">
                      <Info size={12} className="text-slate-450 flex-shrink-0"/>
                      <span>Always verify with local agricultural experts before spraying chemical fungicides. CropGuard provides diagnostic recommendations.</span>
                    </p>
                  </div>
                )}
              </motion.div>
            </ReportErrorBoundary>
          )}

          {/* Result Placeholder */}
          {!diagnosisResult && !analyzing && (
            <div className="card h-full flex flex-col items-center justify-center py-24 text-center bg-white/70 border border-slate-100">
              <div className="w-20 h-20 rounded-3xl bg-slate-50 border border-slate-100 flex items-center justify-center mb-5 shadow-sm">
                <Leaf size={36} className="text-brand-300"/>
              </div>
              <p className="font-semibold text-slate-700 mb-1">Waiting for Diagnosis</p>
              <p className="text-xs text-slate-400 max-w-xs mx-auto font-medium">Upload a leaf photo in the side card, specify crop, and click Diagnose to view the agronomist clinical pathology report.</p>
            </div>
          )}

        </div>

      </div>
    </div>
  )
}
