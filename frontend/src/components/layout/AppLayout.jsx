import React, { useState, useEffect } from 'react'
import { Outlet, NavLink, useNavigate, useLocation } from 'react-router-dom'
import { LayoutDashboard, Leaf, History, Pill, CloudRain, User, LogOut, Menu, X, Bell, ChevronRight, Shield, FlaskConical } from 'lucide-react'
import { useAuth } from '../../context/AuthContext'
import { useLanguage } from '../../context/LanguageContext'
import { notificationsApi } from '../../api/index.js'
import clsx from 'clsx'

const NAV = [
  { to:'/dashboard', icon:LayoutDashboard, label:'Dashboard',  desc:'Overview & stats' },
  { to:'/scan',      icon:Leaf,            label:'Scan Leaf',  desc:'AI disease detection' },
  { to:'/history',   icon:History,         label:'History',    desc:'All detections' },
  { to:'/treatment', icon:Pill,            label:'Treatments', desc:'Disease remedies' },
  { to:'/weather',   icon:CloudRain,       label:'Weather',    desc:'Vizag forecast' },
  { to:'/profile',   icon:User,            label:'Profile',    desc:'Your farm' },
  { to:'/research',  icon:FlaskConical,    label:'Research Lab', desc:'Experimental AI' },
]

const NAV_KEYS = {
  '/dashboard': 'nav.dashboard',
  '/scan': 'nav.scan',
  '/history': 'nav.history',
  '/treatment': 'nav.treatment',
  '/weather': 'nav.weather',
  '/profile': 'nav.profile',
  '/research': 'nav.research',
}

const TITLES = {
  '/dashboard': 'nav.dashboard',
  '/scan': 'nav.scan',
  '/history': 'nav.history',
  '/treatment': 'nav.treatment',
  '/weather': 'nav.weather',
  '/profile': 'nav.profile',
  '/admin': 'nav.admin',
  '/research': 'nav.research',
}

export default function AppLayout() {
  const { user, logout } = useAuth()
  const { lang, setLang, t } = useLanguage()
  const navigate = useNavigate()
  const location = useLocation()
  const [open, setOpen] = useState(false)
  const [notifications, setNotifications] = useState([])
  const [notifDropdownOpen, setNotifDropdownOpen] = useState(false)
  const [permissionPrompt, setPermissionPrompt] = useState(false)

  const initials = (user?.name||'FK').split(' ').map(w=>w[0]).join('').slice(0,2).toUpperCase()
  const titleKey = TITLES[location.pathname]
  const title    = titleKey ? t(titleKey) : 'CropGuard AI'

  const fetchNotifications = () => {
    if (!user) return
    notificationsApi.list()
      .then(setNotifications)
      .catch(err => console.warn('Failed to load notifications:', err))
  }

  useEffect(() => {
    fetchNotifications()
    const timer = setInterval(fetchNotifications, 15000)
    return () => clearInterval(timer)
  }, [user])

  useEffect(() => {
    if ('Notification' in window) {
      const storedPref = localStorage.getItem('cg_notif_permission_prompted')
      if (Notification.permission === 'default' && !storedPref) {
        setPermissionPrompt(true)
      }
    }
  }, [])

  const handleRequestPermission = async () => {
    setPermissionPrompt(false)
    localStorage.setItem('cg_notif_permission_prompted', 'true')
    if ('Notification' in window) {
      const res = await Notification.requestPermission()
      if (res === 'granted') {
        new Notification("CropGuard AI", { body: "In-app notifications enabled successfully!" })
      }
    }
  }

  const handleSkipPermission = () => {
    setPermissionPrompt(false)
    localStorage.setItem('cg_notif_permission_prompted', 'true')
  }

  const markAllAsRead = () => {
    notificationsApi.markAllRead()
      .then(() => {
        setNotifications(prev => prev.map(n => ({ ...n, read: true })))
      })
      .catch(err => console.warn(err))
  }

  const markSingleRead = (id) => {
    notificationsApi.markRead(id)
      .then(() => {
        setNotifications(prev => prev.map(n => n.id === id ? { ...n, read: true } : n))
      })
      .catch(err => console.warn(err))
  }

  const unreadCount = notifications.filter(n => !n.read).length

  return (
    <div className="flex min-h-screen bg-slate-50">
      {open && <div className="fixed inset-0 bg-black/50 z-20 lg:hidden backdrop-blur-sm" onClick={()=>setOpen(false)}/>}

      {/* Sidebar */}
      <aside className={clsx(
        'fixed top-0 left-0 h-full w-64 z-30 transition-transform duration-300 flex flex-col',
        'lg:translate-x-0 lg:sticky lg:top-0 lg:h-screen',
        open ? 'translate-x-0' : '-translate-x-full',
        'bg-brand-950'
      )}>
        {/* Logo */}
        <div className="flex items-center gap-3 px-5 py-5 border-b border-white/10">
          <div className="w-9 h-9 rounded-xl bg-brand-600 flex items-center justify-center flex-shrink-0">
            <span className="text-lg">🌿</span>
          </div>
          <div>
            <div className="font-display text-[15px] font-bold text-white">CropGuard AI</div>
            <div className="text-[11px] text-brand-400">Visakhapatnam</div>
          </div>
          <button className="ml-auto lg:hidden text-brand-400 hover:text-white" onClick={()=>setOpen(false)}><X size={18}/></button>
        </div>

        {/* User card */}
        <div className="mx-3 mt-4 p-3 rounded-xl glass-card">
          <div className="flex items-center gap-3">
            <div className="w-9 h-9 rounded-xl bg-gradient-to-br from-brand-400 to-brand-600 flex items-center justify-center text-white text-sm font-bold flex-shrink-0">{initials}</div>
            <div className="min-w-0">
              <div className="text-sm font-semibold text-white truncate">{user?.name || 'Farmer'}</div>
              <div className="text-[11px] text-brand-400 truncate">{user?.farm_name || 'My Farm'}</div>
            </div>
          </div>
        </div>

        {/* Nav */}
        <nav className="flex-1 px-3 py-4 space-y-1 overflow-y-auto">
          <div className="text-[10px] font-semibold text-brand-600 uppercase tracking-widest px-3 mb-2">Navigation</div>
          {NAV.map(({to,icon:Icon,label})=>(
            <NavLink key={to} to={to} onClick={()=>setOpen(false)}
              className={({isActive})=>clsx(isActive?'nav-item-active':'nav-item-inactive')}>
              <Icon size={18} className="flex-shrink-0"/>
              <span>{t(NAV_KEYS[to] || label)}</span>
              {location.pathname===to && <ChevronRight size={14} className="ml-auto opacity-60"/>}
            </NavLink>
          ))}

          {/* Admin nav — only for admins */}
          {user?.is_admin && (
            <>
              <div className="text-[10px] font-semibold text-brand-600 uppercase tracking-widest px-3 mt-4 mb-2">Administration</div>
              <NavLink to="/admin" onClick={()=>setOpen(false)}
                className={({isActive})=>clsx(isActive?'nav-item-active':'nav-item-inactive')}>
                <Shield size={18} className="flex-shrink-0"/>
                <span>{t('nav.admin')}</span>
                {location.pathname==='/admin' && <ChevronRight size={14} className="ml-auto opacity-60"/>}
              </NavLink>
            </>
          )}
        </nav>

        {/* Footer */}
        <div className="p-3 border-t border-white/10">
          <button onClick={()=>{logout();navigate('/login')}}
            className="flex items-center gap-3 w-full px-3 py-2.5 rounded-xl text-sm text-brand-400 hover:text-white hover:bg-white/10 transition-all">
            <LogOut size={16}/> {t('nav.logout')}
          </button>
          <div className="text-[10px] text-brand-800 text-center mt-2">v4.0 · Hybrid AI Edition</div>
        </div>
      </aside>

      {/* Main */}
      <div className="flex-1 flex flex-col min-w-0">
        {/* Topbar */}
        <header className="sticky top-0 z-10 bg-white/80 backdrop-blur-md border-b border-slate-100 px-4 lg:px-6 py-3">
          <div className="flex items-center gap-3">
            <button className="lg:hidden text-slate-500 hover:text-slate-900" onClick={()=>setOpen(true)}><Menu size={22}/></button>
            <div>
              <h1 className="font-display text-[17px] font-bold text-slate-900">{title}</h1>
            </div>
            <div className="ml-auto flex items-center gap-3">
              {/* Language Switcher */}
              <select
                value={lang}
                onChange={(e) => setLang(e.target.value)}
                className="bg-slate-50 border border-slate-200 text-slate-700 text-xs font-semibold rounded-xl px-2.5 py-1.5 focus:outline-none focus:ring-2 focus:ring-brand-500 hover:bg-slate-100 transition-colors cursor-pointer"
              >
                <option value="en">English (EN)</option>
                <option value="hi">हिन्दी (HI)</option>
                <option value="te">తెలుగు (TE)</option>
              </select>

              <button onClick={()=>navigate('/weather')}
                className="hidden sm:flex items-center gap-2 px-3 py-1.5 bg-brand-50 text-brand-700 text-xs font-semibold rounded-xl hover:bg-brand-100 transition-colors border border-brand-200">
                <CloudRain size={13}/> Vizag Weather
              </button>
              <div className="relative">
                <button 
                  onClick={() => setNotifDropdownOpen(!notifDropdownOpen)}
                  className="relative w-9 h-9 flex items-center justify-center rounded-xl hover:bg-slate-100 text-slate-500 transition-colors"
                >
                  <Bell size={18}/>
                  {unreadCount > 0 && (
                    <span className="absolute top-1 right-1 min-w-[15px] h-[15px] px-1 bg-red-500 rounded-full text-[9px] font-bold text-white flex items-center justify-center border-2 border-white">
                      {unreadCount}
                    </span>
                  )}
                </button>
                
                {notifDropdownOpen && (
                  <>
                    <div className="fixed inset-0 z-40" onClick={() => setNotifDropdownOpen(false)}/>
                    <div className="absolute right-0 mt-2 w-80 bg-white rounded-2xl border border-slate-100 shadow-xl z-50 overflow-hidden divide-y divide-slate-100">
                      <div className="p-3 flex items-center justify-between bg-slate-50/50">
                        <span className="font-semibold text-xs text-slate-900">{t('notifications.title')}</span>
                        {unreadCount > 0 && (
                          <button onClick={markAllAsRead} className="text-[10px] text-brand-600 font-bold hover:underline">
                            {t('notifications.mark_all_read')}
                          </button>
                        )}
                      </div>
                      <div className="max-h-72 overflow-y-auto divide-y divide-slate-50">
                        {notifications.length === 0 ? (
                          <div className="py-8 text-center text-xs text-slate-400">
                            {t('notifications.no_notifications')}
                          </div>
                        ) : (
                          notifications.map(n => (
                            <div 
                              key={n.id} 
                              onClick={() => { 
                                markSingleRead(n.id); 
                                setNotifDropdownOpen(false);
                                if (n.metadata?.scan_id) navigate(`/scan?id=${n.metadata.scan_id}`); 
                              }}
                              className={clsx(
                                "p-3 text-left transition-colors cursor-pointer hover:bg-slate-50 flex gap-2.5 items-start",
                                !n.read ? "bg-brand-50/20" : ""
                              )}
                            >
                              <div className="text-sm mt-0.5">
                                {n.type === 'disease_alert' ? '⚠️'
                                  : n.type === 'weather_alert' ? '🌦️'
                                  : n.type === 'scan_completed' ? '🌿'
                                  : n.type === 'treatment_reminder' ? '💊'
                                  : '🔔'}
                              </div>
                              <div className="flex-1 min-w-0">
                                <div className="flex justify-between items-start gap-1">
                                  <p className={clsx("text-xs truncate", !n.read ? "font-bold text-slate-900" : "text-slate-700")}>{n.title}</p>
                                  {!n.read && <span className="w-1.5 h-1.5 bg-brand-500 rounded-full flex-shrink-0 mt-1"/>}
                                </div>
                                <p className="text-[11px] text-slate-400 mt-0.5 line-clamp-2">{n.message}</p>
                                <p className="text-[9px] text-slate-300 mt-1">{new Date(n.created_at).toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'})}</p>
                              </div>
                            </div>
                          ))
                        )}
                      </div>
                    </div>
                  </>
                )}
              </div>
              <button onClick={()=>navigate('/profile')}
                className="w-9 h-9 rounded-xl bg-gradient-to-br from-brand-400 to-brand-600 flex items-center justify-center text-white text-xs font-bold hover:shadow-md transition-all">
                {initials}
              </button>
            </div>
          </div>
        </header>
 
        <main className="flex-1 p-4 lg:p-6 page-enter overflow-y-auto">
          <Outlet/>
        </main>
      </div>

      {permissionPrompt && (
        <div className="fixed bottom-4 right-4 z-50 w-80 bg-white/95 backdrop-blur-md rounded-2xl border border-slate-100 shadow-2xl p-4 flex flex-col gap-3">
          <div className="flex items-start gap-3">
            <div className="w-9 h-9 rounded-xl bg-brand-50 flex items-center justify-center text-brand-600 flex-shrink-0">
              <Bell size={18}/>
            </div>
            <div>
              <h4 className="font-display font-bold text-xs text-slate-950">Allow CropGuard notifications?</h4>
              <p className="text-[11px] text-slate-400 mt-0.5 leading-relaxed">Get weather warnings, disease risk warnings, and scan updates in real-time.</p>
            </div>
          </div>
          <div className="flex gap-2 justify-end">
            <button onClick={handleSkipPermission} className="px-3 py-1.5 text-[10px] font-bold text-slate-600 hover:bg-slate-50 rounded-lg">Skip</button>
            <button onClick={handleRequestPermission} className="px-3 py-1.5 text-[10px] font-bold bg-brand-600 text-white hover:bg-brand-700 rounded-lg shadow-sm">Allow</button>
          </div>
        </div>
      )}
    </div>
  )
}
