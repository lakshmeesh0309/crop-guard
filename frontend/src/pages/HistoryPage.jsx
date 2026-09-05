// HistoryPage
import React, { useState, useEffect } from 'react'
import { Search, Filter, Trash2, RefreshCw, History, Eye } from 'lucide-react'
import { useNavigate } from 'react-router-dom'
import { scansApi } from '../api/index.js'
import { SectionCard, DataTable, PageSpinner, Alert, Badge } from '../components/ui/index.jsx'

const CROPS = ['All', 'Tomato', 'Potato', 'Chilli', 'Maize', 'Rice', 'Cotton', 'Groundnut', 'Grape', 'Apple']

export default function HistoryPage() {
  const navigate = useNavigate()
  const [scans,   setScans]   = useState([])
  const [loading, setLoading] = useState(true)
  const [search,  setSearch]  = useState('')
  const [crop,    setCrop]    = useState('All')
  const [error,   setError]   = useState('')

  async function load() {
    setLoading(true)
    try {
      const p = {}
      if (crop !== 'All') p.crop = crop
      setScans(await scansApi.list(p))
    } catch(e) { setError(e.message) }
    finally { setLoading(false) }
  }
  useEffect(() => { load() }, [crop])

  async function deleteScan(id) {
    if (!window.confirm('Delete this scan record?')) return
    try { await scansApi.delete(id); setScans(s => s.filter(x => x.id !== id)) }
    catch(e) { setError(e.message) }
  }

  const filtered = scans.filter(s =>
    s.disease.toLowerCase().includes(search.toLowerCase()) ||
    s.crop.toLowerCase().includes(search.toLowerCase()) ||
    (s.field_name||'').toLowerCase().includes(search.toLowerCase())
  )

  const COLS = [
    { key:'id',        label:'ID',      render:v=><span className="font-mono text-xs text-slate-400">#{String(v).slice(-4)}</span> },
    { key:'crop',      label:'Crop',    render:v=><span className="font-medium">{v}</span> },
    { key:'disease',   label:'Disease', render:v=>v==='Healthy'?<Badge label="Healthy" color="green"/>:['Rice Blast Disease','Chilli Leaf Curl Virus'].includes(v)?<Badge label={v} color="red"/>:<Badge label={v} color="amber"/> },
    { key:'confidence',label:'Conf.',   render:v=><span className="font-bold text-slate-700">{Math.round(v)}%</span> },
    { key:'field_name',label:'Field',   render:v=>v||<span className="text-slate-300">—</span> },
    { key:'created_at',label:'Date',    render:v=>v?new Date(v).toLocaleDateString('en-IN',{day:'numeric',month:'short',year:'2-digit'}):'—' },
    { key:'status',    label:'Status',  render:v=>({diseased:<Badge label="Diseased" color="red"/>,healthy:<Badge label="Healthy" color="green"/>,pending:<Badge label="Pending" color="amber"/>})[v] },
    { key:'id',        label:'',        render:(_,row)=>(
      <div className="flex gap-1 items-center">
        <button onClick={()=>navigate(`/scan?id=${row.id}`)} className="w-7 h-7 rounded-lg hover:bg-brand-50 flex items-center justify-center text-brand-500 hover:text-brand-700 transition-all" title="View Report"><Eye size={13}/></button>
        <button onClick={()=>deleteScan(row.id)} className="w-7 h-7 rounded-lg hover:bg-red-50 flex items-center justify-center text-slate-350 hover:text-red-500 transition-all" title="Delete"><Trash2 size={13}/></button>
      </div>
    ) },
  ]

  if (loading) return <PageSpinner/>

  return (
    <div className="space-y-4 animate-fade-in">
      {error && <Alert type="danger" message={error} onClose={()=>setError('')}/>}
      <SectionCard
        title="Detection History"
        subtitle={`${filtered.length} records found`}
        action={<button onClick={load} className="btn btn-secondary btn-sm gap-1.5"><RefreshCw size={12}/>Refresh</button>}>
        <div className="flex flex-wrap gap-3 mb-5">
          <div className="relative flex-1 min-w-[200px]">
            <Search size={15} className="absolute left-3.5 top-1/2 -translate-y-1/2 text-slate-400"/>
            <input value={search} onChange={e=>setSearch(e.target.value)} placeholder="Search disease, crop, field…" className="input pl-10 text-sm"/>
          </div>
          <div className="flex items-center gap-2 flex-wrap">
            <Filter size={14} className="text-slate-400"/>
            {CROPS.map(c=>(
              <button key={c} onClick={()=>setCrop(c)}
                className={`text-xs px-3.5 py-1.5 rounded-full font-semibold border-2 transition-all ${crop===c?'border-brand-500 bg-brand-50 text-brand-700':'border-slate-200 text-slate-500 hover:border-brand-300'}`}>{c}</button>
            ))}
          </div>
        </div>
        <DataTable columns={COLS} rows={filtered} emptyMessage="No scans found. Upload your first leaf!"/>
      </SectionCard>
    </div>
  )
}
