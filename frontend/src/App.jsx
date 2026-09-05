import React from 'react'
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom'
import { AuthProvider, useAuth } from './context/AuthContext'
import AppLayout     from './components/layout/AppLayout'
import LoginPage     from './pages/LoginPage'
import RegisterPage  from './pages/RegisterPage'
import DashboardPage from './pages/DashboardPage'
import ScanPage      from './pages/ScanPage'
import HistoryPage   from './pages/HistoryPage'
import TreatmentPage from './pages/TreatmentPage'
import WeatherPage   from './pages/WeatherPage'
import ProfilePage   from './pages/ProfilePage'
import AdminPage     from './pages/AdminPage'
import ResearchPage  from './pages/ResearchPage'

function Splash() {
  return (
    <div className="min-h-screen bg-brand-950 flex items-center justify-center">
      <div className="flex flex-col items-center gap-4">
        <div className="w-12 h-12 rounded-2xl bg-brand-600 flex items-center justify-center">
          <span className="text-white text-2xl">🌿</span>
        </div>
        <div className="w-8 h-8 rounded-full animate-spin"
          style={{border:'3px solid #bbf7d0', borderTopColor:'#22c55e'}}/>
      </div>
    </div>
  )
}

function Guard({ children }) {
  const { user, loading } = useAuth()
  if (loading) return <Splash/>
  if (!user)   return <Navigate to="/login" replace/>
  return children
}
function Public({ children }) {
  const { user, loading } = useAuth()
  if (loading) return <Splash/>
  if (user)    return <Navigate to="/dashboard" replace/>
  return children
}
function AdminGuard({ children }) {
  const { user, loading } = useAuth()
  if (loading) return <Splash/>
  if (!user)   return <Navigate to="/login" replace/>
  if (!user.is_admin) return <Navigate to="/dashboard" replace/>
  return children
}

import { LanguageProvider } from './context/LanguageContext'

export default function App() {
  return (
    <LanguageProvider>
      <AuthProvider>
      <BrowserRouter>
        <Routes>
          <Route path="/login"    element={<Public><LoginPage/></Public>}/>
          <Route path="/register" element={<Public><RegisterPage/></Public>}/>
          <Route path="/" element={<Guard><AppLayout/></Guard>}>
            <Route index element={<Navigate to="/dashboard" replace/>}/>
            <Route path="dashboard"  element={<DashboardPage/>}/>
            <Route path="scan"       element={<ScanPage/>}/>
            <Route path="history"    element={<HistoryPage/>}/>
            <Route path="treatment"  element={<TreatmentPage/>}/>
            <Route path="weather"    element={<WeatherPage/>}/>
            <Route path="profile"    element={<ProfilePage/>}/>
            <Route path="admin"      element={<AdminGuard><AdminPage/></AdminGuard>}/>
            <Route path="research"   element={<ResearchPage/>}/>
          </Route>
          <Route path="*" element={<Navigate to="/dashboard" replace/>}/>
        </Routes>
      </BrowserRouter>
    </AuthProvider>
    </LanguageProvider>
  )
}
