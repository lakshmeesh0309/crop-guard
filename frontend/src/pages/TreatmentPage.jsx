import React, { useState, useEffect } from 'react'
import { Search } from 'lucide-react'
import { treatmentsApi } from '../api/index.js'
import { PageSpinner } from '../components/ui/index.jsx'
import clsx from 'clsx'

const ICONS = {'Rice Blast Disease':'🌾','Tomato Early Blight':'🍅','Chilli Leaf Curl Virus':'🌶️','Tomato Late Blight':'🍅','Rice Brown Spot':'🌾','Cotton Bollworm':'🌿','General Prevention':'🛡️'}
const TYPE_COLORS = { fungicide:'bg-blue-50 border-blue-200 text-blue-800', insecticide:'bg-red-50 border-red-200 text-red-700', organic:'bg-brand-50 border-brand-200 text-brand-800', cultural:'bg-amber-50 border-amber-200 text-amber-800' }
const TAG_COLORS = {'Fungicide Required':'bg-blue-100 text-blue-700','Organic Option Available':'bg-brand-100 text-brand-700','Insecticide + Removal':'bg-red-100 text-red-700','Systemic Fungicide':'bg-purple-100 text-purple-700','Soil Management':'bg-amber-100 text-amber-700','Integrated Pest Management':'bg-teal-100 text-teal-700','Best Practice':'bg-brand-100 text-brand-700'}

export default function TreatmentPage() {
  const [treatments, setTreatments] = useState([])
  const [loading,    setLoading]    = useState(true)
  const [search,     setSearch]     = useState('')

  useEffect(() => {
    treatmentsApi.list().then(setTreatments).catch(console.error).finally(()=>setLoading(false))
  }, [])

  const filtered = treatments.filter(t =>
    t.disease.toLowerCase().includes(search.toLowerCase()) ||
    (t.pathogen||'').toLowerCase().includes(search.toLowerCase())
  )

  if (loading) return <PageSpinner/>

  return (
    <div className="space-y-5 animate-fade-in">
      {/* Search */}
      <div className="card">
        <div className="relative">
          <Search size={16} className="absolute left-4 top-1/2 -translate-y-1/2 text-slate-400"/>
          <input value={search} onChange={e=>setSearch(e.target.value)}
            placeholder="Search disease or treatment…" className="input pl-11 text-base"/>
        </div>
      </div>

      {/* Grid */}
      <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-4">
        {filtered.map(t => (
          <div key={t.slug} className="card hover:shadow-card-hover hover:-translate-y-0.5 transition-all duration-200 group">
            <div className="flex items-start gap-3 mb-4">
              <div className="w-12 h-12 rounded-2xl bg-brand-50 flex items-center justify-center text-2xl flex-shrink-0 group-hover:bg-brand-100 transition-colors">
                {ICONS[t.disease] || '🌿'}
              </div>
              <div className="min-w-0">
                <h3 className="font-display text-sm font-bold text-slate-900 leading-tight">{t.disease}</h3>
                <p className="text-xs text-slate-400 italic mt-0.5 truncate">{t.pathogen}</p>
              </div>
            </div>

            <div className="space-y-2 mb-4">
              {(t.steps||[]).map((s,i)=>(
                <div key={i} className={clsx('px-3 py-2 rounded-xl border text-xs', TYPE_COLORS[s.type]||TYPE_COLORS.cultural)}>
                  <span className="font-bold">{s.title}:</span> {s.description}
                </div>
              ))}
            </div>

            <div className="flex items-center justify-between">
              <span className={clsx('text-[11px] font-bold px-2.5 py-1 rounded-full', TAG_COLORS[t.tag]||'bg-slate-100 text-slate-600')}>{t.tag}</span>
              {t.crops && <span className="text-[10px] text-slate-400">{(t.crops||[]).join(', ')}</span>}
            </div>
          </div>
        ))}
        {!filtered.length && (
          <div className="col-span-full card text-center py-16">
            <span className="text-5xl mb-4 block">🔍</span>
            <p className="font-semibold text-slate-600">No treatments found for "{search}"</p>
          </div>
        )}
      </div>

      <div className="card bg-amber-50 border-amber-200">
        <p className="text-sm text-amber-800 flex items-start gap-2">
          <span className="text-lg flex-shrink-0">⚠️</span>
          <span><strong>Disclaimer:</strong> Always consult a certified agricultural expert or your local Krishi Vigyan Kendra before applying any treatment. Dosages may vary by region and crop variety.</span>
        </p>
      </div>
    </div>
  )
}
