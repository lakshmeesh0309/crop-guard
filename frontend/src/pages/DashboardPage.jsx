import React, { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { Scan, Bug, TrendingUp, Leaf, ArrowRight, AlertTriangle, Zap, Shield } from 'lucide-react'
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, Cell, AreaChart, Area } from 'recharts'
import { useAuth } from '../context/AuthContext'
import { analyticsApi, scansApi, weatherApi } from '../api/index.js'
import { StatCard, SectionCard, DataTable, ProgressBar, PageSpinner, Badge } from '../components/ui/index.jsx'

const getDPill = d => {
  if (d === 'Healthy') return <Badge label="Healthy" color="green"/>
  if (['Rice Blast Disease','Chilli Leaf Curl Virus','Tomato Late Blight'].includes(d)) return <Badge label={d} color="red"/>
  return <Badge label={d} color="amber"/>
}
const getSPill = s => ({ diseased:<Badge label="Diseased" color="red"/>, healthy:<Badge label="Healthy" color="green"/>, pending:<Badge label="Pending" color="amber"/> }[s] || <Badge label={s}/>)

export default function DashboardPage() {
  const { user }   = useAuth()
  const navigate   = useNavigate()
  const [stats,    setStats]   = useState(null)
  const [scans,    setScans]   = useState([])
  const [weather,  setWeather] = useState(null)
  const [loading,  setLoading] = useState(true)

  const COLS = [
    { key:'id',        label:'ID',      render:v=><span className="font-mono text-xs text-slate-400">#{String(v).slice(-4)}</span> },
    { key:'crop',      label:'Crop',    render:v=><span className="font-medium text-slate-700">{v}</span> },
    { key:'disease',   label:'Disease', render:v=>getDPill(v) },
    { key:'confidence',label:'Conf.',   render:v=><span className="font-semibold text-slate-700">{Math.round(v)}%</span> },
    { key:'field_name',label:'Field',   render:v=>v||<span className="text-slate-300">—</span> },
    { key:'created_at',label:'Date',    render:v=>v?new Date(v).toLocaleDateString('en-IN',{day:'numeric',month:'short'}):'—' },
    { key:'status',    label:'Status',  render:v=>getSPill(v) },
    { key:'id',        label:'',        render:(id)=>(
      <button onClick={()=>navigate(`/scan?id=${id}`)} className="w-7 h-7 rounded-lg hover:bg-brand-50 flex items-center justify-center text-brand-500 hover:text-brand-700 transition-all" title="View Report">
        <ArrowRight size={13}/>
      </button>
    ) },
  ]

  useEffect(() => {
    Promise.all([analyticsApi.dashboard(), scansApi.list({ limit: 5 }), weatherApi.current().catch(() => null)])
      .then(([s, sc, w]) => { setStats(s); setScans(sc); setWeather(w) })
      .catch(console.error)
      .finally(() => setLoading(false))
  }, [])

  const firstName = (user?.name || 'Farmer').split(' ')[0]

  if (loading) return <PageSpinner/>

  const weekData  = stats ? Object.entries(stats.week_counts || {}).map(([day,n])=>({day,n})) : []
  const cropRisk  = stats ? Object.entries(stats.crop_risk  || {}).sort((a,b)=>b[1]-a[1]).slice(0,5) : []

  return (
    <div className="space-y-6 animate-fade-in">
      {/* Hero greeting */}
      <div className="relative overflow-hidden bg-gradient-to-r from-brand-800 to-brand-600 rounded-3xl p-6 text-white">
        <div className="relative z-10 flex items-center justify-between">
          <div>
            <p className="text-brand-300 text-sm font-medium mb-1">Good morning 👋</p>
            <h2 className="font-display text-2xl font-bold">{firstName}</h2>
            <p className="text-brand-200 text-sm mt-1">{user?.farm_name || 'Your Farm'} · Visakhapatnam</p>
          </div>
          <button onClick={() => navigate('/scan')}
            className="btn bg-white text-brand-700 hover:bg-brand-50 shadow-lg gap-2 px-5 py-2.5 flex-shrink-0">
            <Scan size={16}/> Scan Leaf
          </button>
        </div>
        <div className="absolute right-0 bottom-0 w-48 h-48 rounded-full bg-white/5 -mr-10 -mb-10"/>
        <div className="absolute right-20 top-0 w-24 h-24 rounded-full bg-white/5 -mt-6"/>
      </div>

      {/* Alert */}
      <div className="flex items-start gap-3 bg-amber-50 border border-amber-200 rounded-2xl p-4">
        <div className="w-8 h-8 rounded-xl bg-amber-100 flex items-center justify-center flex-shrink-0">
          <AlertTriangle size={15} className="text-amber-600"/>
        </div>
        <div className="flex-1">
          <p className="text-sm font-semibold text-amber-900">High Disease Risk in Vizag Today</p>
          <p className="text-xs text-amber-700 mt-0.5">Coastal humidity creates conditions for Rice Blast and Blight. Inspect your crops now.</p>
        </div>
        <button onClick={() => navigate('/weather')} className="text-xs text-amber-700 font-semibold whitespace-nowrap hover:text-amber-900 flex items-center gap-1">
          Details <ArrowRight size={11}/>
        </button>
      </div>

      {/* Stats grid */}
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-4 stagger">
        <StatCard label="Scans Today"    value={stats?.scans_today    ?? 0} sub="Leaf scans performed"   icon={Scan}       color="brand"  trend={12}/>
        <StatCard label="Diseases Found" value={stats?.diseases_found ?? 0} sub="Requiring attention"    icon={Bug}        color="red"    trend={-5}/>
        <StatCard label="AI Confidence"  value={`${stats?.avg_confidence ?? 0}%`} sub="Average accuracy" icon={TrendingUp} color="teal"   trend={3}/>
        <StatCard label="Healthy Scans"  value={stats?.healthy_count  ?? 0} sub="No disease detected"    icon={Shield}     color="brand"  trend={8}/>
      </div>

      {/* Weather Risk Card */}
      {weather && (
        <div className={`rounded-2xl p-4 border ${
          weather.humidity > 80 ? 'bg-red-50 border-red-200' :
          weather.humidity > 70 ? 'bg-amber-50 border-amber-200' :
          'bg-blue-50 border-blue-200'
        }`}>
          <div className="flex items-center justify-between mb-2">
            <span className="text-xs font-bold text-slate-500 uppercase tracking-widest">Vizag Conditions</span>
            <span className="text-lg">{"\uD83C\uDF21\uFE0F"}</span>
          </div>
          <div className="flex gap-6">
            <div>
              <p className="text-2xl font-bold text-slate-800">{weather.temp}{"\u00B0"}C</p>
              <p className="text-xs text-slate-500">Temperature</p>
            </div>
            <div>
              <p className="text-2xl font-bold text-slate-800">{weather.humidity}%</p>
              <p className="text-xs text-slate-500">Humidity</p>
            </div>
            <div>
              <p className="text-2xl font-bold text-slate-800">{weather.wind_speed || 0} km/h</p>
              <p className="text-xs text-slate-500">Wind</p>
            </div>
          </div>
          <div className={`mt-3 text-xs font-semibold px-2 py-1 rounded-lg inline-block ${
            weather.humidity > 80 ? 'bg-red-100 text-red-700' :
            weather.humidity > 70 ? 'bg-amber-100 text-amber-700' :
            'bg-green-100 text-green-700'
          }`}>
            {weather.humidity > 80 ? '\uD83D\uDD34 High Disease Risk Today' :
             weather.humidity > 70 ? '\uD83D\uDFE1 Moderate Risk \u2014 Monitor Crops' :
             '\uD83D\uDFE2 Low Risk \u2014 Good Conditions'}
          </div>
        </div>
      )}



      {/* Main content */}
      <div className="grid lg:grid-cols-3 gap-5">
        {/* Recent scans */}
        <div className="lg:col-span-2">
          <SectionCard title="Recent Detections" subtitle="Your latest leaf scans"
            action={
              <button onClick={() => navigate('/history')}
                className="btn btn-ghost btn-sm text-brand-600 hover:text-brand-700 gap-1">
                View all <ArrowRight size={12}/>
              </button>
            }>
            {scans.length > 0
              ? <DataTable columns={COLS} rows={scans} emptyMessage="No scans yet — upload your first leaf!"/>
              : (
                <div className="text-center py-12">
                  <div className="w-16 h-16 rounded-2xl bg-brand-50 flex items-center justify-center mx-auto mb-4">
                    <Leaf size={28} className="text-brand-400"/>
                  </div>
                  <p className="font-semibold text-slate-700 mb-1">No scans yet</p>
                  <p className="text-sm text-slate-400 mb-4">Upload your first leaf photo to get started</p>
                  <button onClick={() => navigate('/scan')} className="btn btn-primary gap-2">
                    <Scan size={15}/> Scan Now
                  </button>
                </div>
              )
            }
          </SectionCard>
        </div>

        {/* Right column */}
        <div className="space-y-5">
          {/* Risk chart */}
          <SectionCard title="Disease Risk" subtitle="By crop type">
            {cropRisk.length > 0 ? (
              <div className="space-y-3">
                {cropRisk.map(([crop, risk]) => (
                  <div key={crop}>
                    <div className="flex justify-between text-sm mb-1.5">
                      <span className="font-medium text-slate-700">{crop}</span>
                      <span className={`text-xs font-semibold ${risk>60?'text-red-600':risk>40?'text-amber-600':'text-brand-600'}`}>{risk}%</span>
                    </div>
                    <ProgressBar value={risk}
                      color={risk>60?'bg-red-400':risk>40?'bg-amber-400':'bg-brand-500'}/>
                  </div>
                ))}
              </div>
            ) : (
              <p className="text-sm text-slate-400 text-center py-4">Scan crops to see risk data</p>
            )}
          </SectionCard>

          {/* Weekly activity */}
          <SectionCard title="Weekly Activity" subtitle="Scans per day">
            {weekData.some(d=>d.n>0) ? (
              <ResponsiveContainer width="100%" height={100}>
                <BarChart data={weekData} barSize={20}>
                  <XAxis dataKey="day" tick={{fontSize:11,fill:'#94a3b8'}} axisLine={false} tickLine={false}/>
                  <YAxis hide/>
                  <Tooltip contentStyle={{background:'#0f172a',border:'none',borderRadius:12,color:'#e2e8f0',fontSize:12}} cursor={{fill:'#f1f5f9'}}/>
                  <Bar dataKey="n" radius={[6,6,0,0]}>
                    {weekData.map((_, i) => <Cell key={i} fill={_.n>0?'#16a34a':'#e2e8f0'}/>)}
                  </Bar>
                </BarChart>
              </ResponsiveContainer>
            ) : (
              <p className="text-sm text-slate-400 text-center py-4">No activity this week</p>
            )}
          </SectionCard>
        </div>
      </div>

      {/* Quick actions */}
      <div>
        <h3 className="font-display text-sm font-bold text-slate-500 uppercase tracking-wider mb-3">Quick Actions</h3>
        <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
          {[
            { label:'Scan Leaf',       icon:'🔬', path:'/scan',      bg:'bg-brand-600', text:'text-white' },
            { label:'View History',    icon:'📋', path:'/history',   bg:'bg-white',     text:'text-slate-700' },
            { label:'Treatments',      icon:'💊', path:'/treatment', bg:'bg-white',     text:'text-slate-700' },
            { label:'Weather Vizag',   icon:'🌤', path:'/weather',   bg:'bg-white',     text:'text-slate-700' },
          ].map(a => (
            <button key={a.label} onClick={() => navigate(a.path)}
              className={`flex items-center gap-3 p-4 rounded-2xl text-sm font-semibold transition-all hover:scale-[1.02] active:scale-[0.98] shadow-sm hover:shadow-md border border-slate-100 ${a.bg} ${a.text}`}>
              <span className="text-xl">{a.icon}</span> {a.label}
            </button>
          ))}
        </div>
      </div>
    </div>
  )
}
