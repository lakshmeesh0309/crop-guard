import React, { useState, useRef } from 'react'
import {
  FlaskConical, Upload, RotateCcw, AlertTriangle,
  ThumbsUp, ThumbsDown, CheckCircle2, Cpu, Zap,
  Info, ChevronDown, ChevronRight, Microscope, Target,
  ListChecks, Brain, Lightbulb, XCircle
} from 'lucide-react'
import { motion, AnimatePresence } from 'framer-motion'
import { scansApi } from '../api/index.js'
import api from '../api/index.js'
import { useLanguage } from '../context/LanguageContext'
import clsx from 'clsx'

// ── Experimental crops (NOT in official diagnosis) ────────────────────────
const RESEARCH_CROPS = [
  'Apple', 'Grape', 'Cherry', 'Peach', 'Orange',
  'Raspberry', 'Blueberry', 'Strawberry', 'Squash', 'Soybean'
]

// ── SHA-256 hash for feedback deduplication ───────────────────────────────
async function fileHash(file) {
  try {
    const buf = await file.arrayBuffer()
    const hashBuf = await window.crypto.subtle.digest('SHA-256', buf)
    return Array.from(new Uint8Array(hashBuf)).map(b => b.toString(16).padStart(2, '0')).join('')
  } catch {
    return `hash-${Date.now()}`
  }
}

// ── Confidence bar colour ─────────────────────────────────────────────────
function confColor(pct) {
  if (pct >= 35) return 'bg-purple-500'
  if (pct >= 20) return 'bg-indigo-400'
  return 'bg-slate-300'
}

// ── Section card wrapper ──────────────────────────────────────────────────
function ReportSection({ icon: Icon, title, accent = 'purple', children }) {
  const accents = {
    purple: 'border-purple-500 text-purple-700',
    amber:  'border-amber-500  text-amber-700',
    green:  'border-green-500  text-green-700',
    red:    'border-red-400    text-red-700',
    blue:   'border-blue-500   text-blue-700',
  }
  return (
    <div className="card bg-white/80 border border-slate-100 space-y-3">
      <h3 className={clsx('font-bold text-xs uppercase tracking-wider border-l-4 pl-2 flex items-center gap-1.5', accents[accent])}>
        <Icon size={12} />
        {title}
      </h3>
      {children}
    </div>
  )
}

export default function ResearchPage() {
  const { t, lang } = useLanguage()
  const [file, setFile]             = useState(null)
  const [preview, setPreview]       = useState(null)
  const [crop, setCrop]             = useState('Apple')
  const [dragging, setDragging]     = useState(false)
  const [analyzing, setAnalyzing]   = useState(false)
  const [result, setResult]         = useState(null)
  const [error, setError]           = useState('')
  const [feedback, setFeedback]     = useState(null)
  const [feedbackSent, setFeedbackSent]   = useState(false)
  const [feedbackLoading, setFeedbackLoading] = useState(false)
  const fileRef = useRef()

  function loadFile(f) {
    if (!f?.type?.startsWith('image/')) { setError('Please upload a valid image file.'); return }
    setFile(f); setError(''); setResult(null); setFeedback(null); setFeedbackSent(false)
    const r = new FileReader()
    r.onload = e => setPreview(e.target.result)
    r.readAsDataURL(f)
  }

  function onDrop(e) {
    e.preventDefault(); setDragging(false)
    loadFile(e.dataTransfer?.files?.[0] || e.target.files?.[0])
  }

  async function runResearch() {
    if (!file) return
    setAnalyzing(true); setError(''); setResult(null); setFeedback(null); setFeedbackSent(false)
    try {
      const data = await scansApi.research(file, crop, lang)
      console.log('Research Result:', data)
      console.log('top_predictions:', data.top_predictions)
      console.log('selected_candidate:', data.selected_candidate)
      console.log('visual_reasoning:', data.visual_reasoning)
      console.log('experimental_notes:', data.experimental_notes)
      console.log('next_steps:', data.next_steps)
      console.log('_debug:', data._debug)

      if (!data || (!data.top_predictions?.length && !data.top5?.length)) {
        setError('Research output could not be generated. Please try again.')
        return
      }
      setResult(data)
    } catch (err) {
      console.error('[Research Error]', err)
      setError(err.message || 'Experimental analysis failed. Please try again.')
    } finally {
      setAnalyzing(false)
    }
  }

  async function submitFeedback(choice) {
    if (feedbackSent || !result) return
    setFeedbackLoading(true); setFeedback(choice)
    try {
      const hash = await fileHash(file)
      await api.post('/research-feedback/', {
        crop,
        image_hash: hash,
        mobilenet_predictions: result.top_predictions || result.mobilenet_top5 || [],
        groq_conclusion: result.selected_candidate || '',
        feedback: choice
      })
      setFeedbackSent(true)
    } catch (err) {
      console.warn('[Feedback Error]', err)
      setFeedbackSent(true)
    } finally {
      setFeedbackLoading(false)
    }
  }

  function reset() {
    setFile(null); setPreview(null); setResult(null)
    setError(''); setFeedback(null); setFeedbackSent(false)
  }

  // Resolve keys with fallbacks for both new and legacy backends
  const topPreds        = result?.top_predictions   || result?.top5              || []
  const selected        = result?.selected_candidate || result?.mobilenet_prediction || topPreds[0]?.disease || ''
  const rejected        = result?.rejected_candidates || topPreds.slice(1).map(p => p.disease) || []
  const confidence      = result?.research_confidence || (topPreds[0] ? `${topPreds[0].confidence}%` : '—')
  const visualReasoning = result?.visual_reasoning   || result?.groq_interpretation || ''
  const expNotes        = result?.experimental_notes || ''
  const nextSteps       = result?.next_steps         || ''
  const debugInfo       = result?._debug             || {}

  return (
    <div className="space-y-5 animate-fade-in">

      {/* ── Experimental Banner ────────────────────────────────────────────── */}
      <div className="rounded-2xl border-2 border-amber-300 bg-gradient-to-r from-amber-50 to-orange-50 p-4 flex items-start gap-3">
        <AlertTriangle size={20} className="text-amber-600 flex-shrink-0 mt-0.5" />
        <div>
          <div className="flex items-center gap-2 flex-wrap">
            <span className="font-display font-black text-amber-900 text-sm">AI Research Lab</span>
            <span className="px-2 py-0.5 rounded-full bg-amber-200 text-amber-800 text-[10px] font-black uppercase tracking-wider">Experimental</span>
            <span className="px-2 py-0.5 rounded-full bg-orange-200 text-orange-800 text-[10px] font-black uppercase tracking-wider">Not for Field Use</span>
          </div>
          <p className="text-xs text-amber-800 mt-1 font-semibold leading-relaxed">
            This pipeline uses <strong>MobileNet v3</strong> for image recognition and <strong>Groq LLaMA</strong> for experimental reasoning.
            Results are <strong>not</strong> clinically verified and must not be used for treatment decisions.
          </p>
        </div>
      </div>

      <div className="grid lg:grid-cols-12 gap-6 items-start">

        {/* ── Upload Panel ───────────────────────────────────────────────────── */}
        <div className="lg:col-span-4 space-y-4">
          <div className="card bg-white/80 border border-slate-100 space-y-4">
            <div className="flex items-center justify-between">
              <div>
                <h3 className="font-display font-bold text-sm text-slate-900">Research Analysis</h3>
                <p className="text-[11px] text-slate-400 mt-0.5">MobileNet + Groq Experimental Pipeline</p>
              </div>
              <Cpu size={18} className="text-purple-500" />
            </div>

            {/* Crop selector */}
            <div>
              <label className="block text-xs font-bold text-slate-600 mb-1.5">Experimental Crop</label>
              <select value={crop} onChange={e => setCrop(e.target.value)} className="input text-sm cursor-pointer">
                {RESEARCH_CROPS.map(c => <option key={c} value={c}>{c}</option>)}
              </select>
            </div>

            {/* Drop zone */}
            {!preview ? (
              <div
                className={clsx(
                  'border-2 border-dashed rounded-2xl p-6 text-center cursor-pointer transition-all',
                  dragging ? 'border-purple-500 bg-purple-50 scale-[1.01]' : 'border-slate-200 hover:border-purple-400 hover:bg-purple-50/40'
                )}
                onClick={() => fileRef.current?.click()}
                onDragOver={e => { e.preventDefault(); setDragging(true) }}
                onDragLeave={() => setDragging(false)}
                onDrop={onDrop}
              >
                <div className="w-12 h-12 rounded-2xl bg-purple-50 flex items-center justify-center mx-auto mb-3">
                  <Upload size={22} className="text-purple-400" />
                </div>
                <p className="font-semibold text-slate-700 mb-1 text-sm">Upload leaf image</p>
                <p className="text-xs text-slate-400 mb-3">JPG, PNG, WEBP · Max 10MB</p>
                <button className="text-xs font-bold bg-purple-50 border border-purple-200 text-purple-700 hover:bg-purple-100 rounded-xl px-4 py-2 transition-all">
                  Choose File
                </button>
                <input ref={fileRef} type="file" accept="image/*" className="hidden" onChange={e => loadFile(e.target.files[0])} />
              </div>
            ) : (
              <div className="space-y-3">
                <div className="relative rounded-2xl overflow-hidden border border-slate-200">
                  <img src={preview} alt="Research leaf" className="w-full max-h-60 object-cover" />
                  <button onClick={reset} className="absolute top-2 right-2 w-7 h-7 rounded-lg bg-white/90 shadow flex items-center justify-center">
                    <RotateCcw size={12} className="text-slate-600" />
                  </button>
                  <div className="absolute bottom-2 left-2 bg-black/60 text-white text-[10px] px-2 py-0.5 rounded-full font-bold">
                    {crop} · Research
                  </div>
                </div>
                {!analyzing && !result && (
                  <button onClick={runResearch} className="w-full py-3 rounded-xl font-bold text-sm flex items-center justify-center gap-2 bg-gradient-to-r from-purple-600 to-indigo-600 text-white hover:from-purple-700 hover:to-indigo-700 shadow-md transition-all">
                    <Zap size={15} /> Run Experimental Analysis
                  </button>
                )}
                {result && (
                  <button onClick={reset} className="btn btn-secondary w-full text-xs gap-2">
                    <Upload size={12}/> Analyze Another
                  </button>
                )}
              </div>
            )}

            {/* Analyzing spinner */}
            {analyzing && (
              <div className="flex flex-col items-center gap-3 py-4">
                <div className="w-10 h-10 rounded-full animate-spin" style={{ border: '3px solid #e9d5ff', borderTopColor: '#9333ea' }} />
                <div className="text-center space-y-1">
                  <p className="text-xs font-bold text-purple-700 animate-pulse">Running MobileNet...</p>
                  <p className="text-[10px] text-slate-400">Then Groq experimental reasoning</p>
                </div>
              </div>
            )}

            {/* Error */}
            {error && (
              <div className="rounded-xl border border-red-200 bg-red-50 p-3 flex items-start gap-2">
                <XCircle size={14} className="text-red-500 flex-shrink-0 mt-0.5" />
                <p className="text-xs text-red-700 font-semibold">{error}</p>
              </div>
            )}

            {/* Isolation note */}
            <div className="pt-2 border-t border-slate-100 flex items-start gap-1.5">
              <Info size={10} className="text-slate-400 flex-shrink-0 mt-0.5" />
              <p className="text-[10px] text-slate-400 font-medium leading-relaxed">
                Results from this lab <strong>never influence</strong> official CropGuard diagnoses, treatment recommendations, or evidence scoring.
              </p>
            </div>
          </div>
        </div>

        {/* ── Results Panel ──────────────────────────────────────────────────── */}
        <div className="lg:col-span-8 space-y-4">
          <AnimatePresence mode="wait">
            {!result && !analyzing && (
              <motion.div
                key="empty"
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                exit={{ opacity: 0 }}
                className="card h-full flex flex-col items-center justify-center py-20 text-center bg-white/70 border border-slate-100"
              >
                <div className="w-20 h-20 rounded-3xl bg-purple-50 border border-purple-100 flex items-center justify-center mb-4">
                  <FlaskConical size={36} className="text-purple-200" />
                </div>
                <p className="font-semibold text-slate-700 mb-1">Research Lab Ready</p>
                <p className="text-xs text-slate-400 max-w-xs font-medium leading-relaxed">
                  Select an experimental crop, upload a leaf image, and run the MobileNet + Groq experimental pipeline.
                </p>
              </motion.div>
            )}

            {result && (
              <motion.div
                key="result"
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.45 }}
                className="space-y-4"
              >

                {/* ── 1. Result Header ──────────────────────────────── */}
                <div className="card bg-gradient-to-br from-purple-50 to-indigo-50 border border-purple-200 shadow-sm">
                  <div className="flex items-start gap-4">
                    <div className="w-12 h-12 rounded-2xl bg-purple-600 text-white flex items-center justify-center flex-shrink-0 shadow">
                      <FlaskConical size={22} />
                    </div>
                    <div className="flex-1 min-w-0">
                      <span className="text-[10px] font-black text-purple-400 uppercase tracking-widest block">
                        EXPERIMENTAL RESULT · NOT FOR FIELD USE
                      </span>
                      <h2 className="font-display font-black text-xl text-slate-900 mt-0.5 leading-tight">
                        {selected || 'Analysis Complete'}
                      </h2>
                      <div className="flex flex-wrap gap-2 mt-2">
                        <span className="text-[10px] font-bold bg-purple-100 text-purple-700 border border-purple-200 px-2 py-0.5 rounded-full">
                          Crop: {crop}
                        </span>
                        <span className="text-[10px] font-bold bg-indigo-100 text-indigo-700 border border-indigo-200 px-2 py-0.5 rounded-full">
                          Research Confidence: {confidence}
                        </span>
                        {debugInfo.mobilenet_loaded === false && (
                          <span className="text-[10px] font-bold bg-amber-100 text-amber-700 border border-amber-200 px-2 py-0.5 rounded-full">
                            ⚠ Demo Mode
                          </span>
                        )}
                      </div>
                    </div>
                  </div>
                </div>

                {/* ── 2. Top-5 Predictions ──────────────────────────── */}
                <ReportSection icon={Target} title="MobileNet Top-5 Predictions" accent="purple">
                  {topPreds.length > 0 ? (
                    <div className="space-y-2.5">
                      {topPreds.slice(0, 5).map((p, idx) => {
                        const pct = typeof p.confidence === 'number' ? p.confidence : parseFloat(p.confidence) || 0
                        return (
                          <div key={idx} className="flex items-center gap-3">
                            <span className={clsx(
                              'text-[10px] font-black w-4 flex-shrink-0',
                              idx === 0 ? 'text-purple-600' : 'text-slate-400'
                            )}>#{idx + 1}</span>
                            <div className="flex-1 min-w-0">
                              <div className="flex items-center justify-between mb-1">
                                <span className={clsx(
                                  'text-xs font-bold truncate',
                                  idx === 0 ? 'text-slate-900' : 'text-slate-600'
                                )}>{p.disease}</span>
                                <span className={clsx(
                                  'text-[10px] font-black ml-2 flex-shrink-0',
                                  idx === 0 ? 'text-purple-700' : 'text-slate-500'
                                )}>{pct.toFixed(1)}%</span>
                              </div>
                              <div className="h-1.5 bg-slate-100 rounded-full overflow-hidden">
                                <div
                                  className={clsx('h-full rounded-full transition-all duration-700', confColor(pct))}
                                  style={{ width: `${Math.min(100, pct)}%` }}
                                />
                              </div>
                            </div>
                            {idx === 0 && (
                              <span className="text-[9px] font-black bg-purple-600 text-white px-1.5 py-0.5 rounded-full flex-shrink-0">TOP</span>
                            )}
                          </div>
                        )
                      })}
                    </div>
                  ) : (
                    <p className="text-xs text-red-600 font-semibold">Experimental model unavailable — no predictions returned.</p>
                  )}

                  {debugInfo.mobilenet_error && (
                    <p className="text-[10px] text-amber-600 font-semibold mt-1 flex items-center gap-1">
                      <AlertTriangle size={10} /> {debugInfo.mobilenet_error}
                    </p>
                  )}
                </ReportSection>

                {/* ── 3. Selected Candidate ─────────────────────────── */}
                <ReportSection icon={Microscope} title="Selected Candidate" accent="blue">
                  <div className="flex items-center gap-3 p-3 rounded-xl bg-blue-50/60 border border-blue-100">
                    <div className="w-10 h-10 rounded-xl bg-blue-600 text-white flex items-center justify-center flex-shrink-0">
                      <Microscope size={18} />
                    </div>
                    <div>
                      <p className="font-display font-black text-base text-slate-900 leading-tight">{selected}</p>
                      <p className="text-[10px] text-blue-600 font-bold mt-0.5">Research Confidence: {confidence}</p>
                    </div>
                  </div>
                  {rejected.length > 0 && (
                    <div className="mt-2">
                      <p className="text-[10px] font-bold text-slate-400 uppercase mb-1.5">Rejected Candidates</p>
                      <div className="flex flex-wrap gap-1.5">
                        {rejected.slice(0, 5).map((d, i) => (
                          <span key={i} className="text-[10px] font-semibold bg-slate-100 border border-slate-200 text-slate-500 px-2 py-0.5 rounded-full flex items-center gap-1">
                            <XCircle size={9} /> {d}
                          </span>
                        ))}
                      </div>
                    </div>
                  )}
                </ReportSection>

                {/* ── 4. Groq Visual Reasoning ──────────────────────── */}
                <ReportSection icon={Brain} title="Groq Experimental Reasoning" accent="purple">
                  <div className="bg-purple-50/40 rounded-xl p-3 border border-purple-100 space-y-2">
                    <div className="flex items-center gap-1.5">
                      <span className="px-1.5 py-0.5 rounded bg-purple-200 text-purple-800 text-[9px] font-black uppercase tracking-wider">
                        Experimental Analysis
                      </span>
                    </div>
                    {visualReasoning ? (
                      <p className="text-xs text-slate-700 italic leading-relaxed font-semibold">
                        "{visualReasoning}"
                      </p>
                    ) : (
                      <p className="text-xs text-amber-700 font-semibold">Experimental reasoning unavailable.</p>
                    )}
                  </div>
                  {debugInfo.groq_error && (
                    <p className="text-[10px] text-amber-600 font-semibold flex items-center gap-1 mt-1">
                      <AlertTriangle size={10} /> Groq: {debugInfo.groq_error}
                    </p>
                  )}
                </ReportSection>

                {/* ── 5. Experimental Notes ─────────────────────────── */}
                {expNotes && (
                  <ReportSection icon={Lightbulb} title="Experimental Observations" accent="amber">
                    <p className="text-xs text-slate-600 leading-relaxed font-medium">{expNotes}</p>
                  </ReportSection>
                )}

                {/* ── 6. Next Steps ────────────────────────────────── */}
                {nextSteps && (
                  <ReportSection icon={ListChecks} title="Suggested Next Steps" accent="green">
                    <div className="space-y-1.5">
                      {nextSteps.split('\n').filter(Boolean).map((step, i) => (
                        <div key={i} className="flex items-start gap-2 text-xs text-slate-600 font-medium">
                          <ChevronRight size={12} className="text-green-500 flex-shrink-0 mt-0.5" />
                          <span>{step.replace(/^\d+\.\s*/, '')}</span>
                        </div>
                      ))}
                    </div>
                  </ReportSection>
                )}

                {/* ── 7. Disclaimer ────────────────────────────────── */}
                <div className="rounded-xl border border-amber-200 bg-amber-50/60 p-3">
                  <p className="text-[10px] text-amber-700 font-semibold leading-relaxed flex items-start gap-1.5">
                    <AlertTriangle size={11} className="flex-shrink-0 mt-0.5" />
                    This is an <strong>experimental result</strong> for research purposes only.
                    Do not apply treatments based on this analysis.
                    Use the official <strong>Scan Leaf</strong> feature for verified Gemini Vision diagnosis.
                  </p>
                </div>

                {/* ── 8. Feedback ──────────────────────────────────── */}
                <div className="card bg-white/80 border border-slate-100">
                  <h3 className="font-bold text-xs text-slate-900 uppercase tracking-wider mb-3">
                    Was this experimental analysis useful?
                  </h3>
                  {!feedbackSent ? (
                    <div className="flex items-center gap-3">
                      <button
                        onClick={() => submitFeedback('helpful')}
                        disabled={feedbackLoading}
                        className={clsx(
                          'flex items-center gap-2 px-4 py-2 rounded-xl text-xs font-black border transition-all',
                          feedback === 'helpful'
                            ? 'bg-green-100 border-green-400 text-green-800 scale-105'
                            : 'bg-white border-slate-200 text-slate-600 hover:bg-green-50 hover:border-green-300 hover:text-green-700'
                        )}
                      >
                        <ThumbsUp size={13} /> Helpful
                      </button>
                      <button
                        onClick={() => submitFeedback('not_helpful')}
                        disabled={feedbackLoading}
                        className={clsx(
                          'flex items-center gap-2 px-4 py-2 rounded-xl text-xs font-black border transition-all',
                          feedback === 'not_helpful'
                            ? 'bg-red-100 border-red-400 text-red-800 scale-105'
                            : 'bg-white border-slate-200 text-slate-600 hover:bg-red-50 hover:border-red-300 hover:text-red-700'
                        )}
                      >
                        <ThumbsDown size={13} /> Not Helpful
                      </button>
                      {feedbackLoading && (
                        <span className="text-[10px] text-slate-400 font-semibold animate-pulse">Saving...</span>
                      )}
                    </div>
                  ) : (
                    <motion.div
                      initial={{ opacity: 0, scale: 0.95 }}
                      animate={{ opacity: 1, scale: 1 }}
                      className="flex items-center gap-2 text-green-700"
                    >
                      <CheckCircle2 size={15} />
                      <span className="text-xs font-bold">
                        Thank you! Your feedback helps improve CropGuard's research accuracy.
                      </span>
                    </motion.div>
                  )}
                  <p className="text-[10px] text-slate-400 mt-2 font-medium">
                    Feedback is stored anonymously to improve model performance. It is never shared externally.
                  </p>
                </div>

              </motion.div>
            )}
          </AnimatePresence>
        </div>
      </div>
    </div>
  )
}
