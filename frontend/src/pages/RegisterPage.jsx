import React, { useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { User, Mail, Lock, Tractor, MapPin, Eye, EyeOff, AlertCircle, ArrowRight, Check } from 'lucide-react'
import { useAuth } from '../context/AuthContext'
import { Spinner } from '../components/ui/index.jsx'

const CROPS = ['Rice','Tomato','Chilli','Cotton','Groundnut','Maize','Sugarcane','Wheat']

export default function RegisterPage() {
  const { register } = useAuth()
  const navigate = useNavigate()
  const [step, setStep]     = useState(1)
  const [showPw, setShowPw] = useState(false)
  const [form, setForm]     = useState({ name:'',email:'',password:'',confirmPassword:'',farmName:'',location:'',crops:[] })
  const [error, setError]   = useState('')
  const [loading, setLoading] = useState(false)

  const onChange = e => { setForm(f=>({...f,[e.target.name]:e.target.value})); setError('') }
  const toggleCrop = c => setForm(f=>({...f,crops:f.crops.includes(c)?f.crops.filter(x=>x!==c):[...f.crops,c]}))

  function validateStep1() {
    if (!form.name.trim())  return 'Please enter your full name.'
    if (!form.email.trim()) return 'Please enter your email.'
    if (form.password.length < 6) return 'Password must be at least 6 characters.'
    if (form.password !== form.confirmPassword) return 'Passwords do not match.'
    return null
  }

  function goNext() {
    const err = validateStep1()
    if (err) { setError(err); return }
    setStep(2); setError('')
  }

  async function onSubmit(e) {
    e.preventDefault()
    if (!form.farmName.trim()) { setError('Please enter your farm name.'); return }
    setLoading(true)
    try {
      await register({ name:form.name, email:form.email, password:form.password, farmName:form.farmName, location:form.location, crops:form.crops })
      navigate('/dashboard')
    } catch(err) { setError(err.message || 'Registration failed. Please try again.')
    } finally { setLoading(false) }
  }

  return (
    <div className="min-h-screen flex">
      {/* Left branding */}
      <div className="hidden lg:flex lg:w-[45%] auth-bg relative flex-col justify-center p-12">
        <div className="relative z-10">
          <div className="flex items-center gap-3 mb-12">
            <div className="w-10 h-10 rounded-xl bg-brand-500 flex items-center justify-center shadow-glow"><span className="text-xl">🌿</span></div>
            <div className="font-display text-lg font-bold text-white">CropGuard AI</div>
          </div>
          <h1 className="font-display text-4xl font-extrabold text-white leading-tight mb-5">
            Join Vizag's<br/><span className="text-brand-400">Smart Farmers</span>
          </h1>
          <p className="text-brand-200 text-base leading-relaxed mb-10">
            Get AI-powered disease detection and real-time weather advisories tailored for Visakhapatnam's coastal farming conditions.
          </p>
          {/* Step indicators on left */}
          <div className="space-y-4">
            {[{n:1,t:'Account Setup',d:'Your login credentials'},{n:2,t:'Farm Details',d:'Tell us about your farm'}].map(s=>(
              <div key={s.n} className={`flex items-center gap-4 p-4 rounded-2xl transition-all ${step===s.n?'glass-card':'opacity-50'}`}>
                <div className={`w-8 h-8 rounded-full flex items-center justify-center text-sm font-bold flex-shrink-0 ${step>s.n?'bg-brand-500 text-white':step===s.n?'bg-white text-brand-900':'border-2 border-brand-700 text-brand-600'}`}>
                  {step>s.n ? <Check size={14}/> : s.n}
                </div>
                <div><div className="text-sm font-semibold text-white">{s.t}</div><div className="text-xs text-brand-400">{s.d}</div></div>
              </div>
            ))}
          </div>
        </div>
        <div className="absolute bottom-0 right-0 w-72 h-72 rounded-full bg-brand-600/10 blur-3xl pointer-events-none"/>
      </div>

      {/* Right form */}
      <div className="flex-1 flex items-center justify-center p-6 bg-slate-50">
        <div className="w-full max-w-md">
          <div className="flex items-center gap-3 mb-6 lg:hidden">
            <div className="w-9 h-9 rounded-xl bg-brand-600 flex items-center justify-center"><span className="text-lg">🌿</span></div>
            <div className="font-display text-[16px] font-bold text-slate-900">CropGuard AI</div>
          </div>

          <div className="bg-white rounded-3xl shadow-xl border border-slate-100 p-8">
            {/* Progress */}
            <div className="flex items-center gap-3 mb-8">
              <div className="flex-1 h-1.5 rounded-full bg-slate-100 overflow-hidden">
                <div className="h-full bg-brand-500 rounded-full transition-all duration-500" style={{width:step===1?'50%':'100%'}}/>
              </div>
              <span className="text-xs font-semibold text-slate-400">Step {step} of 2</span>
            </div>

            <div className="mb-6">
              <h2 className="font-display text-2xl font-extrabold text-slate-900 mb-1">
                {step===1?'Create your account':'Your farm details'}
              </h2>
              <p className="text-slate-500 text-sm">{step===1?'Start protecting your crops today':'Almost done — tell us about your farm'}</p>
            </div>

            {error && (
              <div className="flex items-start gap-3 bg-red-50 border border-red-200 text-red-700 rounded-xl px-4 py-3 mb-5">
                <AlertCircle size={15} className="flex-shrink-0 mt-0.5"/>
                <span className="text-sm">{error}</span>
              </div>
            )}

            {step === 1 && (
              <div className="space-y-4">
                <div>
                  <label className="block text-sm font-semibold text-slate-700 mb-2">Full name</label>
                  <div className="relative"><User size={16} className="absolute left-4 top-1/2 -translate-y-1/2 text-slate-400"/>
                    <input name="name" value={form.name} onChange={onChange} placeholder="Ramaiah Kumar" className="input pl-11" autoFocus/>
                  </div>
                </div>
                <div>
                  <label className="block text-sm font-semibold text-slate-700 mb-2">Email address</label>
                  <div className="relative"><Mail size={16} className="absolute left-4 top-1/2 -translate-y-1/2 text-slate-400"/>
                    <input name="email" type="email" value={form.email} onChange={onChange} placeholder="you@example.com" className="input pl-11"/>
                  </div>
                </div>
                <div>
                  <label className="block text-sm font-semibold text-slate-700 mb-2">Password</label>
                  <div className="relative"><Lock size={16} className="absolute left-4 top-1/2 -translate-y-1/2 text-slate-400"/>
                    <input name="password" type={showPw?'text':'password'} value={form.password} onChange={onChange} placeholder="Min. 6 characters" className="input pl-11 pr-11"/>
                    <button type="button" onClick={()=>setShowPw(v=>!v)} className="absolute right-4 top-1/2 -translate-y-1/2 text-slate-400 hover:text-slate-600">{showPw?<EyeOff size={15}/>:<Eye size={15}/>}</button>
                  </div>
                </div>
                <div>
                  <label className="block text-sm font-semibold text-slate-700 mb-2">Confirm password</label>
                  <div className="relative"><Lock size={16} className="absolute left-4 top-1/2 -translate-y-1/2 text-slate-400"/>
                    <input name="confirmPassword" type="password" value={form.confirmPassword} onChange={onChange} placeholder="Repeat password" className="input pl-11"/>
                  </div>
                </div>
                <button onClick={goNext} className="btn btn-primary w-full btn-lg gap-3">Continue <ArrowRight size={16}/></button>
              </div>
            )}

            {step === 2 && (
              <form onSubmit={onSubmit} className="space-y-4">
                <div>
                  <label className="block text-sm font-semibold text-slate-700 mb-2">Farm name</label>
                  <div className="relative"><Tractor size={16} className="absolute left-4 top-1/2 -translate-y-1/2 text-slate-400"/>
                    <input name="farmName" value={form.farmName} onChange={onChange} placeholder="e.g. Krishna Farms" className="input pl-11" autoFocus/>
                  </div>
                </div>
                <div>
                  <label className="block text-sm font-semibold text-slate-700 mb-2">Location <span className="text-slate-400 font-normal">(optional)</span></label>
                  <div className="relative"><MapPin size={16} className="absolute left-4 top-1/2 -translate-y-1/2 text-slate-400"/>
                    <input name="location" value={form.location} onChange={onChange} placeholder="e.g. Vizag, Andhra Pradesh" className="input pl-11"/>
                  </div>
                </div>
                <div>
                  <label className="block text-sm font-semibold text-slate-700 mb-3">What do you grow? <span className="text-slate-400 font-normal">(optional)</span></label>
                  <div className="flex flex-wrap gap-2">
                    {CROPS.map(c=>(
                      <button key={c} type="button" onClick={()=>toggleCrop(c)}
                        className={`flex items-center gap-1.5 text-sm px-3.5 py-1.5 rounded-full border-2 font-medium transition-all ${form.crops.includes(c)?'border-brand-500 bg-brand-50 text-brand-700':'border-slate-200 text-slate-600 hover:border-brand-300'}`}>
                        {form.crops.includes(c) && <Check size={12}/>}{c}
                      </button>
                    ))}
                  </div>
                </div>
                <div className="flex gap-3 pt-2">
                  <button type="button" onClick={()=>setStep(1)} className="btn btn-secondary flex-1">← Back</button>
                  <button type="submit" disabled={loading} className="btn btn-primary flex-2 flex-1 gap-2 disabled:opacity-60">
                    {loading ? <Spinner size="sm"/> : 'Create Account'}
                  </button>
                </div>
              </form>
            )}

            <div className="mt-6 text-center text-sm text-slate-500">
              Already have an account?{' '}
              <Link to="/login" className="text-brand-600 font-semibold hover:text-brand-700">Sign in</Link>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
