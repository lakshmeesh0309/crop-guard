// WeatherPage.jsx
import React, { useState, useEffect } from 'react'
import { Droplets, Wind, ThermometerSun, CloudRain, AlertTriangle, MapPin, RefreshCw } from 'lucide-react'
import { weatherApi } from '../api/index.js'
import { SectionCard, DataTable, PageSpinner, Badge } from '../components/ui/index.jsx'

export function WeatherPage() {
  const [current,  setCurrent]  = useState(null)
  const [forecast, setForecast] = useState([])
  const [advisory, setAdvisory] = useState(null)
  const [loading,  setLoading]  = useState(true)
  const [time,     setTime]     = useState(new Date())

  useEffect(()=>{ const t=setInterval(()=>setTime(new Date()),60000); return ()=>clearInterval(t) },[])
  useEffect(()=>{
    Promise.all([weatherApi.current(),weatherApi.forecast(),weatherApi.advisory()])
      .then(([c,f,a])=>{setCurrent(c);setForecast(f);setAdvisory(a)})
      .catch(console.error).finally(()=>setLoading(false))
  },[])

  if (loading) return <PageSpinner/>

  const RISK_PILL = r => ({High:<Badge label="High Risk" color="red"/>,Medium:<Badge label="Medium Risk" color="amber"/>,Low:<Badge label="Low Risk" color="green"/>}[r]||<Badge label={r}/>)
  const COLS=[{key:'day',label:'Day',render:v=><span className="font-semibold text-slate-700">{v}</span>},{key:'temp_max',label:'Temp',render:v=>`${v}°C`},{key:'humidity',label:'Humidity',render:v=>`${v}%`},{key:'rain',label:'Rain',render:v=>`${v} mm`},{key:'disease_risk',label:'Disease Risk',render:v=>RISK_PILL(v)}]

  return (
    <div className="space-y-5 animate-fade-in">
      {/* Hero weather card */}
      <div className="relative overflow-hidden rounded-3xl bg-gradient-to-br from-slate-800 to-slate-900 text-white p-6">
        <div className="relative z-10 grid sm:grid-cols-3 gap-6">
          <div>
            <div className="flex items-center gap-2 text-slate-400 text-sm mb-2">
              <MapPin size={13}/> {current?.location || 'Visakhapatnam'}
            </div>
            <div className="font-display text-6xl font-extrabold mb-1">{current?.temp ?? 31}°C</div>
            <div className="text-slate-300 text-lg mb-3">{current?.description || 'Partly Cloudy'}</div>
            <div className="flex gap-4">
              <div className="flex items-center gap-1.5 text-sm text-slate-400"><Droplets size={14}/>{current?.humidity??82}%</div>
              <div className="flex items-center gap-1.5 text-sm text-slate-400"><Wind size={14}/>{current?.wind_speed??14} km/h</div>
            </div>
          </div>

          <div className="sm:col-span-2 bg-amber-500/15 rounded-2xl p-4 border border-amber-500/20">
            <div className="flex items-start gap-3">
              <AlertTriangle size={18} className="text-amber-400 flex-shrink-0 mt-0.5"/>
              <div>
                <p className="font-bold text-amber-300 mb-1">Disease Advisory — {advisory?.overall_risk||'Medium'} Risk</p>
                <p className="text-amber-200/80 text-sm leading-relaxed">{advisory?.summary||'Monitor your crops closely.'}</p>
              </div>
            </div>
            <div className="grid grid-cols-3 gap-2 mt-4">
              {[{l:'Fungal Risk',v:current?.disease_risk||'Medium'},{l:'Bacterial Risk',v:'Medium'},{l:'Pest Risk',v:'Low'}].map(r=>(
                <div key={r.l} className={`rounded-xl p-2.5 text-center text-xs ${r.v==='High'?'bg-red-500/20 text-red-300':r.v==='Medium'?'bg-amber-500/20 text-amber-300':'bg-green-500/20 text-green-300'}`}>
                  <div className="font-bold">{r.v}</div><div className="opacity-70 mt-0.5">{r.l}</div>
                </div>
              ))}
            </div>
          </div>
        </div>
        <div className="absolute -right-10 -bottom-10 w-48 h-48 rounded-full bg-white/5 blur-2xl"/>
      </div>

      {/* Stats */}
      <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
        {[{icon:ThermometerSun,label:'Feels Like',val:`${current?.feels_like??34}°C`,color:'text-red-500'},{icon:Droplets,label:'Humidity',val:`${current?.humidity??82}%`,color:'text-blue-500'},{icon:CloudRain,label:'Rain (1h)',val:`${current?.rain_1h??0} mm`,color:'text-teal-500'},{icon:Wind,label:'Wind',val:`${current?.wind_speed??14} km/h`,color:'text-slate-500'}].map(s=>(
          <div key={s.label} className="card text-center">
            <s.icon size={22} className={`${s.color} mx-auto mb-2`}/>
            <div className="font-display text-xl font-bold text-slate-900">{s.val}</div>
            <div className="text-xs text-slate-400 mt-0.5">{s.label}</div>
          </div>
        ))}
      </div>

      <SectionCard title="7-Day Forecast" subtitle="Visakhapatnam disease risk outlook">
        <DataTable columns={COLS} rows={forecast}/>
      </SectionCard>

      {advisory?.advisories?.length>0 && (
        <SectionCard title="Crop Advisory" subtitle="Specific recommendations for your crops">
          <div className="grid sm:grid-cols-2 gap-3">
            {advisory.advisories.map(a=>(
              <div key={a.crop} className="flex items-start gap-3 p-4 rounded-xl bg-slate-50 border border-slate-100">
                <div className="w-10 h-10 rounded-xl bg-brand-100 flex items-center justify-center font-bold text-brand-700 flex-shrink-0">{a.crop[0]}</div>
                <div>
                  <div className="flex items-center gap-2 mb-1">
                    <span className="font-semibold text-slate-800 text-sm">{a.crop}</span>
                    <Badge label={a.alert} color={a.alert.includes('High')?'red':a.alert.includes('Medium')?'amber':'green'}/>
                  </div>
                  <p className="text-xs text-slate-500 leading-relaxed">{a.message}</p>
                </div>
              </div>
            ))}
          </div>
        </SectionCard>
      )}
    </div>
  )
}
export default WeatherPage
