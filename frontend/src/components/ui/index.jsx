import React from 'react'
import clsx from 'clsx'

export function StatCard({ label, value, sub, icon: Icon, trend, color = 'brand' }) {
  const colors = {
    brand: { bg:'bg-brand-50', icon:'text-brand-600', accent:'bg-brand-500' },
    red:   { bg:'bg-red-50',   icon:'text-red-600',   accent:'bg-red-500' },
    amber: { bg:'bg-amber-50', icon:'text-amber-600', accent:'bg-amber-500' },
    teal:  { bg:'bg-teal-50',  icon:'text-teal-600',  accent:'bg-teal-500' },
  }
  const c = colors[color] || colors.brand
  return (
    <div className="card group hover:shadow-card-hover hover:-translate-y-0.5 transition-all duration-200">
      <div className="flex items-start justify-between mb-4">
        <div className={clsx('w-10 h-10 rounded-xl flex items-center justify-center', c.bg)}>
          {Icon && <Icon size={20} className={c.icon}/>}
        </div>
        {trend !== undefined && (
          <span className={clsx('text-xs font-semibold px-2 py-1 rounded-lg', trend >= 0 ? 'bg-brand-50 text-brand-600' : 'bg-red-50 text-red-600')}>
            {trend >= 0 ? '+' : ''}{trend}%
          </span>
        )}
      </div>
      <div className="font-display text-3xl font-bold text-slate-900 mb-1">{value}</div>
      <div className="text-sm font-medium text-slate-700 mb-0.5">{label}</div>
      {sub && <div className="text-xs text-slate-400">{sub}</div>}
    </div>
  )
}

export function SectionCard({ title, subtitle, action, children, className = '' }) {
  return (
    <div className={clsx('card', className)}>
      {(title || action) && (
        <div className="flex items-center justify-between mb-5">
          <div>
            {title && <h2 className="font-display text-base font-bold text-slate-900">{title}</h2>}
            {subtitle && <p className="text-xs text-slate-400 mt-0.5">{subtitle}</p>}
          </div>
          {action}
        </div>
      )}
      {children}
    </div>
  )
}

export function DataTable({ columns, rows, emptyMessage = 'No data yet.' }) {
  if (!rows.length) return (
    <div className="text-center py-12 text-sm text-slate-400">{emptyMessage}</div>
  )
  return (
    <div className="overflow-x-auto -mx-1">
      <table className="w-full text-sm">
        <thead>
          <tr className="border-b border-slate-100">
            {columns.map(c => (
              <th key={c.key} className="text-left text-[11px] font-semibold text-slate-400 uppercase tracking-wider pb-3 px-3 whitespace-nowrap">{c.label}</th>
            ))}
          </tr>
        </thead>
        <tbody className="divide-y divide-slate-50">
          {rows.map((row, i) => (
            <tr key={i} className="hover:bg-slate-50/70 transition-colors group">
              {columns.map(c => (
                <td key={c.key} className="py-3 px-3 text-slate-700 whitespace-nowrap">
                  {c.render ? c.render(row[c.key], row) : row[c.key]}
                </td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}

export function ProgressBar({ value, color = 'bg-brand-500', className = '', showLabel = false }) {
  return (
    <div className={clsx('relative', className)}>
      <div className="h-2 bg-slate-100 rounded-full overflow-hidden">
        <div className={clsx('h-full rounded-full transition-all duration-700 ease-out', color)} style={{ width:`${Math.min(100, Math.max(0, value))}%` }}/>
      </div>
      {showLabel && <span className="absolute right-0 -top-5 text-xs font-medium text-slate-500">{Math.round(value)}%</span>}
    </div>
  )
}

export function Spinner({ size = 'md', className = '' }) {
  const s = { sm:'w-4 h-4 border-2', md:'w-8 h-8 border-[3px]', lg:'w-12 h-12 border-4' }
  return <div className={clsx('rounded-full border-brand-200 border-t-brand-500 animate-spin', s[size], className)}/>
}

export function PageSpinner() {
  return (
    <div className="flex flex-col items-center justify-center py-24 gap-4">
      <Spinner size="lg"/>
      <p className="text-sm text-slate-400 animate-pulse">Loading…</p>
    </div>
  )
}

export function Alert({ type = 'info', title, message, className = '', onClose }) {
  const styles = {
    info:    'bg-blue-50 border-blue-200 text-blue-800',
    warning: 'bg-amber-50 border-amber-200 text-amber-800',
    danger:  'bg-red-50 border-red-200 text-red-700',
    success: 'bg-brand-50 border-brand-200 text-brand-800',
  }
  return (
    <div className={clsx('flex items-start gap-3 border rounded-xl px-4 py-3', styles[type], className)}>
      <div className="flex-1">
        {title   && <p className="font-semibold text-sm">{title}</p>}
        {message && <p className="text-sm mt-0.5 opacity-80">{message}</p>}
      </div>
      {onClose && <button onClick={onClose} className="opacity-50 hover:opacity-100 text-lg leading-none mt-0.5">×</button>}
    </div>
  )
}

export function Badge({ label, color = 'slate' }) {
  const c = {
    green:'bg-brand-100 text-brand-700', red:'bg-red-100 text-red-700',
    amber:'bg-amber-100 text-amber-700', blue:'bg-blue-100 text-blue-700',
    teal:'bg-teal-100 text-teal-700',   slate:'bg-slate-100 text-slate-700',
  }
  return <span className={clsx('inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-semibold', c[color]||c.slate)}>{label}</span>
}
