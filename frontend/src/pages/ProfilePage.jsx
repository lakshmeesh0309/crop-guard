import React, { useState, useEffect } from 'react'
import { User, Mail, MapPin, Tractor, Save, LogOut, Camera, Check } from 'lucide-react'
import { usersApi, notificationsApi } from '../api/index.js'
import { SectionCard, Alert, Spinner, PageSpinner } from '../components/ui/index.jsx'
import { useAuth } from '../context/AuthContext'
import { useNavigate } from 'react-router-dom'

const CROPS = ['Tomato', 'Potato', 'Chilli', 'Maize', 'Rice', 'Cotton', 'Groundnut', 'Grape', 'Apple']

export default function ProfilePage() {
  const { user, logout, updateUser } = useAuth()
  const navigate = useNavigate()
  const [form,    setForm]    = useState({ name:'', farm_name:'', location:'', crops:[] })
  const [stats,   setStats]   = useState(null)
  const [prefs,   setPrefs]   = useState({ weather_alerts: true, disease_alerts: true, scan_alerts: true, treatment_reminders: true })
  const [loading, setLoading] = useState(true)
  const [saving,  setSaving]  = useState(false)
  const [saved,   setSaved]   = useState(false)
  const [error,   setError]   = useState('')

  useEffect(() => {
    Promise.all([usersApi.getProfile(), usersApi.getStats(), notificationsApi.getPrefs().catch(() => null)])
      .then(([p, s, pr]) => {
        setForm({ name:p.name||'', farm_name:p.farm_name||'', location:p.location||'', crops:p.crops||[] })
        setStats(s)
        if (pr) setPrefs(pr)
      })
      .catch(e => setError(e.message))
      .finally(() => setLoading(false))
  }, [])

  const onChange    = e => { setForm(f=>({...f,[e.target.name]:e.target.value})); setSaved(false) }
  const toggleCrop  = c => { setForm(f=>({...f,crops:f.crops.includes(c)?f.crops.filter(x=>x!==c):[...f.crops,c]})); setSaved(false) }
  const togglePref  = k => { setPrefs(p=>({...p,[k]:!p[k]})); setSaved(false) }

  async function save(e) {
    e.preventDefault()
    setSaving(true); setError('')
    try {
      await Promise.all([
        usersApi.updateProfile(form),
        notificationsApi.savePrefs(prefs)
      ])
      updateUser({ name:form.name, farm_name:form.farm_name })
      setSaved(true)
      setTimeout(() => setSaved(false), 3000)
    } catch(err) { setError(err.message) }
    finally { setSaving(false) }
  }

  if (loading) return <PageSpinner/>

  const initials = form.name.split(' ').map(w=>w[0]).join('').slice(0,2).toUpperCase() || 'FK'

  return (
    <div className="max-w-2xl space-y-5 animate-fade-in">
      {/* Profile hero card */}
      <div className="relative overflow-hidden rounded-3xl bg-gradient-to-br from-brand-800 to-brand-600 p-6 text-white">
        <div className="flex items-center gap-5">
          <div className="relative">
            <div className="w-20 h-20 rounded-2xl bg-white/20 backdrop-blur flex items-center justify-center font-display text-3xl font-bold border-2 border-white/30">
              {initials}
            </div>
            <div className="absolute -bottom-1 -right-1 w-6 h-6 rounded-full bg-brand-400 border-2 border-white flex items-center justify-center">
              <Camera size={10} className="text-white"/>
            </div>
          </div>
          <div>
            <h2 className="font-display text-2xl font-bold">{form.name || 'Your Name'}</h2>
            <p className="text-brand-200 text-sm mt-0.5">{user?.email}</p>
            <p className="text-brand-300 text-xs mt-1">{form.farm_name || 'Your Farm'} · {form.location || 'Visakhapatnam'}</p>
          </div>
        </div>
        {/* Stats row */}
        <div className="grid grid-cols-4 gap-3 mt-5 pt-5 border-t border-white/20">
          {[
            { label:'Total Scans',     val: stats?.total_scans    ?? 0 },
            { label:'Scans Today',     val: stats?.scans_today    ?? 0 },
            { label:'Diseases Found',  val: stats?.diseases_found ?? 0 },
            { label:'Avg Confidence',  val: stats?.avg_confidence ? `${stats.avg_confidence}%` : '—' },
          ].map(s => (
            <div key={s.label} className="text-center">
              <div className="font-display text-xl font-bold">{s.val}</div>
              <div className="text-brand-300 text-[10px] mt-0.5">{s.label}</div>
            </div>
          ))}
        </div>
        <div className="absolute -right-8 -top-8 w-40 h-40 rounded-full bg-white/5 blur-2xl pointer-events-none"/>
      </div>

      {saved  && <Alert type="success" title="Profile saved!" message="Your changes have been saved successfully." onClose={()=>setSaved(false)}/>}
      {error  && <Alert type="danger"  message={error} onClose={()=>setError('')}/>}

      <form onSubmit={save} className="space-y-4">
        <SectionCard title="Personal Information">
          <div className="space-y-4">
            <div>
              <label className="block text-sm font-semibold text-slate-700 mb-2">Full name</label>
              <div className="relative">
                <User size={16} className="absolute left-4 top-1/2 -translate-y-1/2 text-slate-400"/>
                <input name="name" value={form.name} onChange={onChange} className="input pl-11" placeholder="Your full name"/>
              </div>
            </div>
            <div>
              <label className="block text-sm font-semibold text-slate-700 mb-2">Email address</label>
              <div className="relative">
                <Mail size={16} className="absolute left-4 top-1/2 -translate-y-1/2 text-slate-400"/>
                <input value={user?.email||''} disabled className="input pl-11 bg-slate-50 text-slate-400 cursor-not-allowed"/>
              </div>
              <p className="text-xs text-slate-400 mt-1.5">Email cannot be changed after registration.</p>
            </div>
          </div>
        </SectionCard>

        <SectionCard title="Farm Details">
          <div className="space-y-4">
            <div>
              <label className="block text-sm font-semibold text-slate-700 mb-2">Farm name</label>
              <div className="relative">
                <Tractor size={16} className="absolute left-4 top-1/2 -translate-y-1/2 text-slate-400"/>
                <input name="farm_name" value={form.farm_name} onChange={onChange} className="input pl-11" placeholder="e.g. Krishna Farms"/>
              </div>
            </div>
            <div>
              <label className="block text-sm font-semibold text-slate-700 mb-2">Location</label>
              <div className="relative">
                <MapPin size={16} className="absolute left-4 top-1/2 -translate-y-1/2 text-slate-400"/>
                <input name="location" value={form.location} onChange={onChange} className="input pl-11" placeholder="e.g. Visakhapatnam, Andhra Pradesh"/>
              </div>
            </div>
            <div>
              <label className="block text-sm font-semibold text-slate-700 mb-3">Crops you grow</label>
              <div className="flex flex-wrap gap-2">
                {CROPS.map(c => (
                  <button key={c} type="button" onClick={()=>toggleCrop(c)}
                    className={`flex items-center gap-1.5 text-sm px-3.5 py-1.5 rounded-full border-2 font-medium transition-all ${form.crops.includes(c)?'border-brand-500 bg-brand-50 text-brand-700':'border-slate-200 text-slate-500 hover:border-brand-300'}`}>
                    {form.crops.includes(c) && <Check size={12}/>}{c}
                  </button>
                ))}
              </div>
            </div>
          </div>
        </SectionCard>
 
        <SectionCard title="Notification Preferences" subtitle="Configure granular alert preferences">
          <div className="space-y-4">
            {[
              { key: 'weather_alerts', label: 'Weather Alerts', desc: 'Get warned when climate conditions favor crop fungal spreads.' },
              { key: 'disease_alerts', label: 'Disease Alerts', desc: 'Get alerts when high risk diseases are scanned.' },
              { key: 'scan_alerts', label: 'Scan Completed', desc: 'Get notified immediately upon scan report completion.' },
              { key: 'treatment_reminders', label: 'Treatment Reminders', desc: 'Get reminders about agronomist calendars.' }
            ].map(item => (
              <div key={item.key} className="flex items-start justify-between">
                <div>
                  <label className="text-sm font-semibold text-slate-700 block">{item.label}</label>
                  <span className="text-xs text-slate-400 leading-normal">{item.desc}</span>
                </div>
                <label className="relative inline-flex items-center cursor-pointer select-none">
                  <input 
                    type="checkbox" 
                    checked={prefs[item.key]} 
                    onChange={() => togglePref(item.key)}
                    className="sr-only peer"
                  />
                  <div className="w-9 h-5 bg-slate-205 peer-focus:outline-none rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-slate-350 after:border after:rounded-full after:h-4 after:w-4 after:transition-all peer-checked:bg-brand-600"></div>
                </label>
              </div>
            ))}
          </div>
        </SectionCard>

        <div className="flex gap-3">
          <button type="submit" disabled={saving}
            className="btn btn-primary gap-2 px-6 disabled:opacity-60">
            {saving ? <Spinner size="sm"/> : <Save size={15}/>}
            {saving ? 'Saving…' : 'Save Changes'}
          </button>
          <button type="button" onClick={() => { logout(); navigate('/login') }}
            className="btn btn-secondary gap-2 text-red-600 border-red-200 hover:bg-red-50">
            <LogOut size={15}/> Sign Out
          </button>
        </div>
      </form>
    </div>
  )
}
