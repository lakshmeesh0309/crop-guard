import React, { useState, useEffect, useRef, useCallback } from 'react'
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, Cell, PieChart, Pie, AreaChart, Area, Legend } from 'recharts'
import { adminApi } from '../api/index.js'

const TABS = ['Overview', 'Users', 'All Scans', 'Model']
const CHART_COLORS = ['#22c55e','#16a34a','#15803d','#166534','#14532d']

function StatCard({ label, value, icon, color='green' }) {
  const bg = { green:'bg-brand-50', blue:'bg-blue-50', red:'bg-red-50', amber:'bg-amber-50' }[color] || 'bg-brand-50'
  const text = { green:'text-brand-700', blue:'text-blue-700', red:'text-red-700', amber:'text-amber-700' }[color] || 'text-brand-700'
  return (
    <div className={`${bg} rounded-2xl p-5 border border-slate-100`}>
      <div className="flex items-center justify-between mb-2">
        <span className="text-2xl">{icon}</span>
        <span className={`text-[11px] font-semibold uppercase tracking-wider ${text}`}>{label}</span>
      </div>
      <div className="text-3xl font-bold text-slate-900">{value ?? '—'}</div>
    </div>
  )
}

function RoleBadge({ role }) {
  if (role === 'admin') return <span className="px-2 py-0.5 rounded-full text-[11px] font-bold bg-green-100 text-green-700">Admin</span>
  return <span className="px-2 py-0.5 rounded-full text-[11px] font-bold bg-slate-100 text-slate-600">Farmer</span>
}

function StatusBadge({ status }) {
  if (status === 'healthy') return <span className="px-2 py-0.5 rounded-full text-[11px] font-bold bg-green-100 text-green-700">Healthy</span>
  if (status === 'diseased') return <span className="px-2 py-0.5 rounded-full text-[11px] font-bold bg-red-100 text-red-700">Diseased</span>
  return <span className="px-2 py-0.5 rounded-full text-[11px] font-bold bg-amber-100 text-amber-700">{status || 'Pending'}</span>
}

function Pagination({ page, total, limit, onChange }) {
  const pages = Math.ceil(total / limit) || 1
  return (
    <div className="flex items-center justify-between mt-4 text-sm text-slate-500">
      <span>Showing page {page} of {pages} ({total} total)</span>
      <div className="flex gap-2">
        <button disabled={page <= 1} onClick={() => onChange(page - 1)}
          className="px-3 py-1.5 rounded-lg bg-slate-100 hover:bg-slate-200 disabled:opacity-40 disabled:cursor-not-allowed transition-colors font-medium">
          ← Prev
        </button>
        <button disabled={page >= pages} onClick={() => onChange(page + 1)}
          className="px-3 py-1.5 rounded-lg bg-slate-100 hover:bg-slate-200 disabled:opacity-40 disabled:cursor-not-allowed transition-colors font-medium">
          Next →
        </button>
      </div>
    </div>
  )
}

// ─── Overview Tab ──────────────────────────────────
function OverviewTab() {
  const [stats, setStats] = useState(null)
  const [analytics, setAnalytics] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    Promise.all([
      adminApi.getStats(),
      adminApi.getAnalytics().catch(() => null)
    ])
      .then(([s, a]) => {
        setStats(s)
        setAnalytics(a)
      })
      .catch(console.error)
      .finally(() => setLoading(false))
  }, [])

  if (loading) return <div className="flex justify-center py-20"><div className="w-8 h-8 rounded-full animate-spin" style={{border:'3px solid #bbf7d0', borderTopColor:'#22c55e'}}/></div>
  if (!stats) return <div className="text-center text-slate-400 py-20">Failed to load stats</div>

  const COLORS = ['#22c55e', '#3b82f6', '#f59e0b', '#ec4899', '#8b5cf6', '#14b8a6']

  return (
    <div className="space-y-6">
      {/* Platform Cards */}
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
        <StatCard label="Total Users" value={stats.total_users} icon="👥" color="blue" />
        <StatCard label="Total Scans" value={stats.total_scans} icon="🔬" color="green" />
        <StatCard label="Diseases Found" value={stats.total_diseased} icon="🦠" color="red" />
        <StatCard label="Scans Today" value={stats.scans_today} icon="📊" color="amber" />
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Top Diseases Chart */}
        <div className="bg-white rounded-2xl border border-slate-100 p-5">
          <h3 className="font-display font-bold text-slate-900 mb-4">Top Diseases Detected</h3>
          {stats.top_diseases?.length > 0 ? (
            <ResponsiveContainer width="100%" height={250}>
              <BarChart data={stats.top_diseases} layout="vertical" margin={{left:20}}>
                <XAxis type="number" tick={{fontSize:12}} />
                <YAxis dataKey="disease" type="category" tick={{fontSize:11}} width={140} />
                <Tooltip contentStyle={{borderRadius:12, border:'1px solid #e2e8f0'}} />
                <Bar dataKey="count" radius={[0,8,8,0]}>
                  {stats.top_diseases.map((_, i) => <Cell key={i} fill={CHART_COLORS[i % CHART_COLORS.length]} />)}
                </Bar>
              </BarChart>
            </ResponsiveContainer>
          ) : (
            <div className="text-slate-400 text-sm py-10 text-center">No scan data yet</div>
          )}
        </div>

        {/* Crop Distribution Pie Chart */}
        <div className="bg-white rounded-2xl border border-slate-100 p-5">
          <h3 className="font-display font-bold text-slate-900 mb-4">Crop Distribution</h3>
          {analytics?.crop_distribution?.length > 0 ? (
            <ResponsiveContainer width="100%" height={250}>
              <PieChart>
                <Pie
                  data={analytics.crop_distribution}
                  cx="50%"
                  cy="50%"
                  innerRadius={60}
                  outerRadius={80}
                  paddingAngle={5}
                  dataKey="value"
                  label={({ name, percent }) => `${name} (${(percent * 100).toFixed(0)}%)`}
                >
                  {analytics.crop_distribution.map((_, index) => (
                    <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                  ))}
                </Pie>
                <Tooltip />
              </PieChart>
            </ResponsiveContainer>
          ) : (
            <div className="text-slate-400 text-sm py-10 text-center">No crop data yet</div>
          )}
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Engine usage (Gemini vs Groq) */}
        <div className="bg-white rounded-2xl border border-slate-100 p-5">
          <h3 className="font-display font-bold text-slate-900 mb-4">AI Engine Usage & Distribution</h3>
          {analytics?.engine_usage?.length > 0 ? (
            <ResponsiveContainer width="100%" height={250}>
              <PieChart>
                <Pie
                  data={analytics.engine_usage}
                  cx="50%"
                  cy="50%"
                  outerRadius={85}
                  dataKey="value"
                  label={({ name, percent }) => `${name} (${(percent * 100).toFixed(0)}%)`}
                >
                  {analytics.engine_usage.map((_, index) => (
                    <Cell key={`cell-${index}`} fill={COLORS[(index + 1) % COLORS.length]} />
                  ))}
                </Pie>
                <Tooltip />
              </PieChart>
            </ResponsiveContainer>
          ) : (
            <div className="text-slate-400 text-sm py-10 text-center">No engine usage data yet</div>
          )}
        </div>

        {/* Monthly Activity Area Chart */}
        <div className="bg-white rounded-2xl border border-slate-100 p-5">
          <h3 className="font-display font-bold text-slate-900 mb-4">Monthly Scan Activity</h3>
          {analytics?.monthly_activity?.length > 0 ? (
            <ResponsiveContainer width="100%" height={250}>
              <AreaChart data={analytics.monthly_activity}>
                <XAxis dataKey="month" tick={{fontSize:11}} />
                <YAxis tick={{fontSize:11}} />
                <Tooltip />
                <Area type="monotone" dataKey="scans" stroke="#22c55e" fillOpacity={0.1} fill="#22c55e" strokeWidth={2} />
              </AreaChart>
            </ResponsiveContainer>
          ) : (
            <div className="text-slate-400 text-sm py-10 text-center">No activity trends yet</div>
          )}
        </div>
      </div>

      {/* MobileNet v3 Experimental Research Logs */}
      <div className="bg-white rounded-2xl border border-slate-100 p-5">
        <div className="flex items-center justify-between border-b border-slate-100 pb-3 mb-4">
          <div>
            <h3 className="font-display font-bold text-slate-900">MobileNet v3 Research Metrics</h3>
            <p className="text-xs text-slate-400 mt-0.5">Experimental local model crop recognition evaluations</p>
          </div>
          {analytics && (
            <span className="text-xs font-black text-slate-700 bg-slate-100 px-3 py-1 rounded-lg">
              Total Matches: {analytics.mobilenet_research?.crop_match_count}
            </span>
          )}
        </div>

        <div className="space-y-4">
          <h4 className="text-xs font-bold text-slate-400 uppercase tracking-wider">Recent Classification Discrepancy Logs</h4>
          <div className="overflow-x-auto">
            <table className="w-full text-left border-collapse text-xs text-slate-600">
              <thead>
                <tr className="border-b border-slate-150 text-slate-400">
                  <th className="pb-2">Scan ID</th>
                  <th className="pb-2">User Selected Crop</th>
                  <th className="pb-2">MobileNet Recognised Crop</th>
                  <th className="pb-2">Final Diagnosis</th>
                  <th className="pb-2">Date</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-100">
                {analytics?.mobilenet_research?.mismatches?.length > 0 ? (
                  analytics.mobilenet_research.mismatches.map(m => (
                    <tr key={m.id} className="hover:bg-slate-50 transition-colors">
                      <td className="py-2.5 font-mono text-slate-400">#{m.id.slice(-6)}</td>
                      <td className="py-2.5 font-semibold text-slate-700">{m.user_crop}</td>
                      <td className="py-2.5 font-semibold text-red-600">{m.mobilenet_crop || 'Unknown'}</td>
                      <td className="py-2.5 text-slate-500">{m.disease}</td>
                      <td className="py-2.5 text-slate-400">{new Date(m.created_at).toLocaleDateString('en-IN')}</td>
                    </tr>
                  ))
                ) : (
                  <tr>
                    <td colSpan={5} className="text-center py-6 text-slate-400">No discrepancies logged yet. Perfect recognition agreement!</td>
                  </tr>
                )}
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
  )
}

// ─── Users Tab ─────────────────────────────────────
function UsersTab() {
  const [users, setUsers] = useState([])
  const [total, setTotal] = useState(0)
  const [page, setPage] = useState(1)
  const [loading, setLoading] = useState(true)
  const [expanded, setExpanded] = useState(null)
  const [expandedScans, setExpandedScans] = useState([])

  const load = useCallback((p) => {
    setLoading(true)
    adminApi.getUsers({ page: p, limit: 15 })
      .then(d => { setUsers(d.users); setTotal(d.total); setPage(d.page) })
      .catch(console.error)
      .finally(() => setLoading(false))
  }, [])

  useEffect(() => { load(1) }, [load])

  const handleExpand = async (id) => {
    if (expanded === id) { setExpanded(null); return }
    setExpanded(id)
    try {
      const detail = await adminApi.getUser(id)
      setExpandedScans(detail.recent_scans || [])
    } catch { setExpandedScans([]) }
  }

  const handleRoleToggle = async (id, currentRole) => {
    const newRole = currentRole === 'admin' ? 'farmer' : 'admin'
    if (!confirm(`Change this user's role to ${newRole}?`)) return
    try {
      await adminApi.changeRole(id, newRole)
      load(page)
    } catch (e) { alert(e.message) }
  }

  const handleDisable = async (id) => {
    if (!confirm('Disable this user account? This is a soft-delete.')) return
    try {
      await adminApi.disableUser(id)
      load(page)
    } catch (e) { alert(e.message) }
  }

  if (loading) return <div className="flex justify-center py-20"><div className="w-8 h-8 rounded-full animate-spin" style={{border:'3px solid #bbf7d0', borderTopColor:'#22c55e'}}/></div>

  return (
    <div>
      <div className="overflow-x-auto bg-white rounded-2xl border border-slate-100">
        <table className="w-full text-sm">
          <thead>
            <tr className="border-b border-slate-100">
              <th className="text-left px-4 py-3 font-semibold text-slate-600">Name</th>
              <th className="text-left px-4 py-3 font-semibold text-slate-600">Email</th>
              <th className="text-left px-4 py-3 font-semibold text-slate-600">Role</th>
              <th className="text-left px-4 py-3 font-semibold text-slate-600">Location</th>
              <th className="text-left px-4 py-3 font-semibold text-slate-600">Joined</th>
              <th className="text-left px-4 py-3 font-semibold text-slate-600">Scans</th>
              <th className="text-left px-4 py-3 font-semibold text-slate-600">Actions</th>
            </tr>
          </thead>
          <tbody>
            {users.map(u => (
              <React.Fragment key={u.id}>
                <tr className="border-b border-slate-50 hover:bg-slate-50/50 transition-colors">
                  <td className="px-4 py-3 font-medium text-slate-800">{u.name}</td>
                  <td className="px-4 py-3 text-slate-500">{u.email}</td>
                  <td className="px-4 py-3"><RoleBadge role={u.role}/></td>
                  <td className="px-4 py-3 text-slate-500">{u.location || '—'}</td>
                  <td className="px-4 py-3 text-slate-500">{u.created_at ? new Date(u.created_at).toLocaleDateString('en-IN', {day:'numeric',month:'short',year:'2-digit'}) : '—'}</td>
                  <td className="px-4 py-3 font-semibold text-brand-600">{u.scans_count ?? 0}</td>
                  <td className="px-4 py-3">
                    <div className="flex gap-1.5">
                      <button onClick={() => handleExpand(u.id)}
                        className="px-2 py-1 rounded-lg text-[11px] font-semibold bg-blue-50 text-blue-600 hover:bg-blue-100 transition-colors">
                        {expanded === u.id ? 'Hide' : 'View'}
                      </button>
                      <button onClick={() => handleRoleToggle(u.id, u.role)}
                        className="px-2 py-1 rounded-lg text-[11px] font-semibold bg-amber-50 text-amber-600 hover:bg-amber-100 transition-colors">
                        {u.role === 'admin' ? 'Remove Admin' : 'Make Admin'}
                      </button>
                      <button onClick={() => handleDisable(u.id)}
                        className="px-2 py-1 rounded-lg text-[11px] font-semibold bg-red-50 text-red-600 hover:bg-red-100 transition-colors">
                        Disable
                      </button>
                    </div>
                  </td>
                </tr>
                {expanded === u.id && (
                  <tr>
                    <td colSpan={7} className="px-4 py-3 bg-slate-50">
                      <div className="text-xs font-semibold text-slate-500 mb-2">Recent Scans</div>
                      {expandedScans.length > 0 ? (
                        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-2">
                          {expandedScans.map(s => (
                            <div key={s.id} className="bg-white rounded-xl p-3 border border-slate-100 text-xs">
                              <div className="flex justify-between"><span className="font-medium">{s.crop}</span><StatusBadge status={s.status}/></div>
                              <div className="text-slate-500 mt-1">{s.disease} · {Math.round(s.confidence)}%</div>
                              <div className="text-slate-400 mt-1">{s.created_at ? new Date(s.created_at).toLocaleDateString('en-IN') : ''}</div>
                            </div>
                          ))}
                        </div>
                      ) : (
                        <div className="text-slate-400 text-xs">No scans found</div>
                      )}
                    </td>
                  </tr>
                )}
              </React.Fragment>
            ))}
          </tbody>
        </table>
      </div>
      <Pagination page={page} total={total} limit={15} onChange={p => load(p)} />
    </div>
  )
}

// ─── All Scans Tab ─────────────────────────────────
function AllScansTab() {
  const [scans, setScans] = useState([])
  const [total, setTotal] = useState(0)
  const [page, setPage] = useState(1)
  const [loading, setLoading] = useState(true)

  const load = useCallback((p) => {
    setLoading(true)
    adminApi.getAllScans({ page: p, limit: 20 })
      .then(d => { setScans(d.scans); setTotal(d.total); setPage(d.page) })
      .catch(console.error)
      .finally(() => setLoading(false))
  }, [])

  useEffect(() => { load(1) }, [load])

  if (loading) return <div className="flex justify-center py-20"><div className="w-8 h-8 rounded-full animate-spin" style={{border:'3px solid #bbf7d0', borderTopColor:'#22c55e'}}/></div>

  return (
    <div>
      <div className="overflow-x-auto bg-white rounded-2xl border border-slate-100">
        <table className="w-full text-sm">
          <thead>
            <tr className="border-b border-slate-100">
              <th className="text-left px-4 py-3 font-semibold text-slate-600">User</th>
              <th className="text-left px-4 py-3 font-semibold text-slate-600">Crop</th>
              <th className="text-left px-4 py-3 font-semibold text-slate-600">Disease</th>
              <th className="text-left px-4 py-3 font-semibold text-slate-600">Confidence</th>
              <th className="text-left px-4 py-3 font-semibold text-slate-600">Status</th>
              <th className="text-left px-4 py-3 font-semibold text-slate-600">AI</th>
              <th className="text-left px-4 py-3 font-semibold text-slate-600">Date</th>
            </tr>
          </thead>
          <tbody>
            {scans.map(s => (
              <tr key={s.id} className="border-b border-slate-50 hover:bg-slate-50/50 transition-colors">
                <td className="px-4 py-3 text-slate-700">{s.user_name || s.user_id?.slice(-6) || '—'}</td>
                <td className="px-4 py-3 font-medium text-slate-800">{s.crop}</td>
                <td className="px-4 py-3 text-slate-700">{s.disease || '—'}</td>
                <td className="px-4 py-3 font-semibold text-slate-700">{s.confidence ? `${Math.round(s.confidence)}%` : '—'}</td>
                <td className="px-4 py-3"><StatusBadge status={s.status}/></td>
                <td className="px-4 py-3">
                  <span className="px-2 py-0.5 rounded-full text-[10px] font-bold bg-purple-50 text-purple-600">{s.ai_source || '—'}</span>
                </td>
                <td className="px-4 py-3 text-slate-500">{s.created_at ? new Date(s.created_at).toLocaleDateString('en-IN', {day:'numeric', month:'short'}) : '—'}</td>
              </tr>
            ))}
            {scans.length === 0 && (
              <tr><td colSpan={7} className="text-center py-10 text-slate-400">No scans found</td></tr>
            )}
          </tbody>
        </table>
      </div>
      <Pagination page={page} total={total} limit={20} onChange={p => load(p)} />
    </div>
  )
}

// ─── Model Tab ─────────────────────────────────────
function ModelTab() {
  const [status, setStatus] = useState(null)
  const [loading, setLoading] = useState(true)
  const [triggering, setTriggering] = useState(false)
  const pollRef = useRef(null)
  const logEndRef = useRef(null)

  const fetchStatus = useCallback(() => {
    adminApi.getModelStatus().then(setStatus).catch(console.error).finally(() => setLoading(false))
  }, [])

  useEffect(() => {
    fetchStatus()
    return () => { if (pollRef.current) clearInterval(pollRef.current) }
  }, [fetchStatus])

  useEffect(() => {
    if (status?.status === 'training' || status?.status === 'downloading') {
      if (!pollRef.current) {
        pollRef.current = setInterval(fetchStatus, 5000)
      }
    } else {
      if (pollRef.current) { clearInterval(pollRef.current); pollRef.current = null }
    }
  }, [status?.status, fetchStatus])

  useEffect(() => {
    logEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [status?.log?.length])

  const handleTrigger = async () => {
    if (!confirm('Start model training? This will download the PlantVillage dataset and train EfficientNetB3.')) return
    setTriggering(true)
    try {
      await adminApi.triggerTraining()
      fetchStatus()
    } catch (e) { alert(e.message) }
    finally { setTriggering(false) }
  }

  if (loading) return <div className="flex justify-center py-20"><div className="w-8 h-8 rounded-full animate-spin" style={{border:'3px solid #bbf7d0', borderTopColor:'#22c55e'}}/></div>

  const isActive = status?.status === 'training' || status?.status === 'downloading'
  const statusColor = {
    idle: 'bg-slate-100 text-slate-600',
    downloading: 'bg-blue-100 text-blue-700',
    training: 'bg-amber-100 text-amber-700',
    done: 'bg-green-100 text-green-700',
    error: 'bg-red-100 text-red-700',
  }[status?.status] || 'bg-slate-100 text-slate-600'

  return (
    <div className="space-y-6">
      {/* Model Info Card */}
      <div className="bg-white rounded-2xl border border-slate-100 p-6">
        <div className="flex items-start justify-between mb-4">
          <div>
            <h3 className="font-display font-bold text-lg text-slate-900">Hybrid Model — EfficientNetB3</h3>
            <p className="text-sm text-slate-500 mt-1">Fine-tuned on PlantVillage dataset from Kaggle</p>
          </div>
          <span className={`px-3 py-1 rounded-full text-xs font-bold ${statusColor}`}>
            {status?.status?.toUpperCase() || 'IDLE'}
          </span>
        </div>

        <div className="grid grid-cols-2 lg:grid-cols-4 gap-4 mt-4">
          <div className="bg-slate-50 rounded-xl p-3 text-center">
            <div className="text-lg font-bold text-brand-600">{status?.version || 'v1.0'}</div>
            <div className="text-[11px] text-slate-500">Version</div>
          </div>
          <div className="bg-slate-50 rounded-xl p-3 text-center">
            <div className="text-lg font-bold text-brand-600">{status?.accuracy != null ? `${status.accuracy}%` : 'Not trained yet'}</div>
            <div className="text-[11px] text-slate-500">Accuracy</div>
          </div>
          <div className="bg-slate-50 rounded-xl p-3 text-center">
            <div className="text-lg font-bold text-brand-600">{status?.last_trained ? new Date(status.last_trained).toLocaleDateString('en-IN') : 'Never'}</div>
            <div className="text-[11px] text-slate-500">Last Trained</div>
          </div>
          <div className="bg-slate-50 rounded-xl p-3 text-center">
            <div className="text-lg font-bold text-brand-600">{status?.dataset || 'PlantVillage'}</div>
            <div className="text-[11px] text-slate-500">Dataset</div>
          </div>
        </div>
      </div>

      {/* Progress Bar */}
      {isActive && (
        <div className="bg-white rounded-2xl border border-slate-100 p-5">
          <div className="flex justify-between text-sm mb-2">
            <span className="font-semibold text-slate-700">Training Progress</span>
            <span className="font-bold text-brand-600">{status?.progress || 0}%</span>
          </div>
          <div className="w-full bg-slate-100 rounded-full h-3">
            <div className="bg-gradient-to-r from-brand-400 to-brand-600 h-3 rounded-full transition-all duration-500"
              style={{ width: `${status?.progress || 0}%` }} />
          </div>
        </div>
      )}

      {/* Training Log */}
      {status?.log?.length > 0 && (
        <div className="bg-brand-950 rounded-2xl p-5">
          <h4 className="text-brand-400 font-semibold text-sm mb-3">Training Log</h4>
          <div className="max-h-64 overflow-y-auto font-mono text-xs space-y-1">
            {status.log.map((line, i) => (
              <div key={i} className={`${line.includes('ERROR') ? 'text-red-400' : line.includes('[Done]') ? 'text-green-400' : 'text-brand-300'}`}>
                {line}
              </div>
            ))}
            <div ref={logEndRef} />
          </div>
        </div>
      )}

      {/* Error Display */}
      {status?.error && (
        <div className="bg-red-50 border border-red-200 rounded-2xl p-4 text-sm text-red-700">
          <span className="font-bold">Error:</span> {status.error}
        </div>
      )}

      {/* Trigger Button */}
      <div className="flex items-center gap-4">
        <button onClick={handleTrigger} disabled={isActive || triggering}
          className="px-6 py-3 rounded-2xl bg-gradient-to-r from-brand-500 to-brand-700 text-white font-bold text-sm hover:shadow-lg hover:shadow-brand-500/25 disabled:opacity-50 disabled:cursor-not-allowed transition-all">
          {isActive ? '⏳ Training in Progress...' : triggering ? '⏳ Starting...' : '🚀 Trigger Training'}
        </button>
      </div>

      {/* Instructions */}
      <div className="bg-blue-50 border border-blue-200 rounded-2xl p-5 text-sm text-blue-800">
        <h4 className="font-bold mb-2">ℹ️ How Training Works</h4>
        <ol className="list-decimal list-inside space-y-1 text-blue-700">
          <li>Downloads the PlantVillage dataset from Kaggle (~2GB)</li>
          <li>Prepares training/validation splits with data augmentation</li>
          <li>Loads EfficientNetB3 pretrained on ImageNet (base layers frozen)</li>
          <li>Fine-tunes the classification head for 10 epochs</li>
          <li>Saves the trained model to <code className="bg-blue-100 px-1 rounded">backend/models/cropguard_hybrid.h5</code></li>
        </ol>
        <p className="mt-3 text-blue-600 text-xs">Requires <code className="bg-blue-100 px-1 rounded">KAGGLE_USERNAME</code> and <code className="bg-blue-100 px-1 rounded">KAGGLE_KEY</code> in the backend <code className="bg-blue-100 px-1 rounded">.env</code> file.</p>
      </div>
    </div>
  )
}

// ─── Main Admin Page ───────────────────────────────
export default function AdminPage() {
  const [tab, setTab] = useState(0)

  return (
    <div className="space-y-6">
      {/* Page Header */}
      <div className="flex items-center justify-between">
        <div>
          <h2 className="font-display text-2xl font-bold text-slate-900">Admin Dashboard</h2>
          <p className="text-sm text-slate-500 mt-1">Platform management & model training</p>
        </div>
        <span className="px-3 py-1.5 rounded-xl bg-brand-50 text-brand-700 text-xs font-bold border border-brand-200">
          🛡️ Admin Access
        </span>
      </div>

      {/* Tab Bar */}
      <div className="flex gap-1 p-1 bg-slate-100 rounded-2xl w-fit">
        {TABS.map((t, i) => (
          <button key={t} onClick={() => setTab(i)}
            className={`px-4 py-2 rounded-xl text-sm font-semibold transition-all ${
              tab === i
                ? 'bg-white text-brand-700 shadow-sm'
                : 'text-slate-500 hover:text-slate-700'
            }`}>
            {t}
          </button>
        ))}
      </div>

      {/* Tab Content */}
      {tab === 0 && <OverviewTab />}
      {tab === 1 && <UsersTab />}
      {tab === 2 && <AllScansTab />}
      {tab === 3 && <ModelTab />}
    </div>
  )
}
