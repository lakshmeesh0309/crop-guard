import React, { useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { Mail, Lock, Eye, EyeOff, AlertCircle, ArrowRight, CheckCircle2 } from 'lucide-react'
import { useAuth } from '../context/AuthContext'
import { Spinner } from '../components/ui/index.jsx'

export default function LoginPage() {
  const { login } = useAuth()
  const navigate  = useNavigate()
  const [form, setForm]       = useState({ email: '', password: '' })
  const [showPw, setShowPw]   = useState(false)
  const [error, setError]     = useState('')
  const [loading, setLoading] = useState(false)

  const onChange = e => { setForm(f => ({ ...f, [e.target.name]: e.target.value })); setError('') }

  async function onSubmit(e) {
    e.preventDefault()
    if (!form.email.trim()) { setError('Please enter your email address.'); return }
    if (!form.password)     { setError('Please enter your password.'); return }
    setLoading(true)
    try {
      await login(form.email.trim(), form.password)
      navigate('/dashboard')
    } catch (err) {
      setError(err.message || 'Login failed. Check your email and password.')
    } finally { setLoading(false) }
  }

  const features = [
    'Instant AI-powered leaf disease detection',
    'Real-time Visakhapatnam weather advisories',
    'Crop-specific treatment recommendations',
    'Complete farm health history tracking',
  ]

  return (
    <div className="min-h-screen flex">
      {/* Left — Branding */}
      <div className="hidden lg:flex lg:w-[55%] auth-bg relative flex-col justify-between p-12">
        <div className="relative z-10">
          {/* Logo */}
          <div className="flex items-center gap-3 mb-16">
            <div className="w-10 h-10 rounded-xl bg-brand-500 flex items-center justify-center shadow-glow">
              <span className="text-xl">🌿</span>
            </div>
            <div>
              <div className="font-display text-lg font-bold text-white">CropGuard AI</div>
              <div className="text-xs text-brand-400">Visakhapatnam Edition</div>
            </div>
          </div>

          {/* Hero text */}
          <div className="mb-10">
            <h1 className="font-display text-5xl font-extrabold text-white leading-[1.1] mb-5">
              Protect Your<br/>
              <span className="text-brand-400">Crops</span> with<br/>
              AI Intelligence
            </h1>
            <p className="text-brand-200 text-lg leading-relaxed max-w-md">
              Upload a leaf photo and get instant disease diagnosis, treatment plans, and live weather risk alerts for Vizag farms.
            </p>
          </div>

          {/* Features */}
          <div className="space-y-3 mb-12">
            {features.map((f, i) => (
              <div key={i} className="flex items-center gap-3">
                <div className="w-5 h-5 rounded-full bg-brand-500/20 border border-brand-500/40 flex items-center justify-center flex-shrink-0">
                  <CheckCircle2 size={12} className="text-brand-400"/>
                </div>
                <span className="text-brand-100/80 text-sm">{f}</span>
              </div>
            ))}
          </div>

          {/* Stats */}
          <div className="grid grid-cols-3 gap-4">
            {[{val:'94%',label:'AI Accuracy'},{val:'38+',label:'Diseases Detected'},{val:'< 5s',label:'Analysis Time'}].map(s=>(
              <div key={s.val} className="glass-card p-4 text-center">
                <div className="font-display text-2xl font-bold text-white mb-1">{s.val}</div>
                <div className="text-xs text-brand-400">{s.label}</div>
              </div>
            ))}
          </div>
        </div>

        {/* Decorative circles */}
        <div className="absolute bottom-0 right-0 w-96 h-96 rounded-full bg-brand-600/10 blur-3xl pointer-events-none"/>
        <div className="absolute top-1/2 right-16 w-48 h-48 rounded-full bg-brand-400/8 blur-2xl pointer-events-none"/>

        <p className="relative z-10 text-xs text-brand-700">© 2026 CropGuard AI · Built for Vizag Farmers</p>
      </div>

      {/* Right — Form */}
      <div className="flex-1 flex items-center justify-center p-6 bg-slate-50">
        <div className="w-full max-w-md">
          {/* Mobile logo */}
          <div className="flex items-center gap-3 mb-8 lg:hidden">
            <div className="w-9 h-9 rounded-xl bg-brand-600 flex items-center justify-center"><span className="text-lg">🌿</span></div>
            <div className="font-display text-[16px] font-bold text-slate-900">CropGuard AI</div>
          </div>

          {/* Form card */}
          <div className="bg-white rounded-3xl shadow-xl border border-slate-100 p-8">
            <div className="mb-8">
              <h2 className="font-display text-3xl font-extrabold text-slate-900 mb-2">Welcome back</h2>
              <p className="text-slate-500">Sign in to your CropGuard account</p>
            </div>

            {error && (
              <div className="flex items-start gap-3 bg-red-50 border border-red-200 text-red-700 rounded-xl px-4 py-3 mb-6">
                <AlertCircle size={16} className="flex-shrink-0 mt-0.5"/>
                <span className="text-sm">{error}</span>
              </div>
            )}

            <form onSubmit={onSubmit} className="space-y-5">
              <div>
                <label className="block text-sm font-semibold text-slate-700 mb-2">Email address</label>
                <div className="relative">
                  <Mail size={16} className="absolute left-4 top-1/2 -translate-y-1/2 text-slate-400"/>
                  <input
                    name="email" type="email" value={form.email} onChange={onChange}
                    placeholder="you@example.com"
                    className="input pl-11"
                    autoComplete="email" autoFocus
                  />
                </div>
              </div>

              <div>
                <label className="block text-sm font-semibold text-slate-700 mb-2">Password</label>
                <div className="relative">
                  <Lock size={16} className="absolute left-4 top-1/2 -translate-y-1/2 text-slate-400"/>
                  <input
                    name="password" type={showPw ? 'text' : 'password'} value={form.password} onChange={onChange}
                    placeholder="Your password"
                    className="input pl-11 pr-11"
                    autoComplete="current-password"
                  />
                  <button type="button" onClick={() => setShowPw(v => !v)}
                    className="absolute right-4 top-1/2 -translate-y-1/2 text-slate-400 hover:text-slate-600">
                    {showPw ? <EyeOff size={16}/> : <Eye size={16}/>}
                  </button>
                </div>
              </div>

              <button type="submit" disabled={loading}
                className="btn btn-primary w-full btn-lg gap-3 disabled:opacity-60 disabled:cursor-not-allowed">
                {loading ? <Spinner size="sm"/> : <>Sign in <ArrowRight size={16}/></>}
              </button>
            </form>

            <div className="mt-6 text-center text-sm text-slate-500">
              New to CropGuard?{' '}
              <Link to="/register" className="text-brand-600 font-semibold hover:text-brand-700 transition-colors">
                Create an account
              </Link>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
