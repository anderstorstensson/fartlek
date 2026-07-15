import { useEffect, useState } from 'react'
import { NavLink, Route, Routes } from 'react-router-dom'
import { fetchJson, SyncStatus } from './api'
import Activities from './pages/Activities'
import ActivityDetailPage from './pages/ActivityDetail'
import Calendar from './pages/Calendar'
import Dashboard from './pages/Dashboard'
import Logbook from './pages/Logbook'
import Records from './pages/Records'
import SettingsPage from './pages/Settings'
import Trends from './pages/Trends'

const NAV_ITEMS = [
  { to: '/', label: 'Dashboard', icon: '📊' },
  { to: '/activities', label: 'Activities', icon: '🏃' },
  { to: '/logbook', label: 'Logbook', icon: '📒' },
  { to: '/calendar', label: 'Calendar', icon: '📅' },
  { to: '/trends', label: 'Trends', icon: '📈' },
  { to: '/records', label: 'Records', icon: '🏆' },
  { to: '/settings', label: 'Settings', icon: '⚙️' }
]

export default function App() {
  const [sync, setSync] = useState<SyncStatus | null>(null)

  useEffect(() => {
    let cancelled = false
    const load = () => {
      fetchJson<SyncStatus>('/api/sync/status')
        .then((status) => {
          if (!cancelled) setSync(status)
        })
        .catch(() => undefined)
    }
    load()
    const timer = setInterval(load, 30000)
    return () => {
      cancelled = true
      clearInterval(timer)
    }
  }, [])

  return (
    <div className="layout">
      <nav className="sidebar">
        <div className="brand">
          fart<span>lek</span>
        </div>
        {NAV_ITEMS.map((item) => (
          <NavLink
            key={item.to}
            to={item.to}
            end={item.to === '/'}
            className={({ isActive }) => (isActive ? 'active' : '')}
          >
            {item.icon} <span className="label-text">{item.label}</span>
          </NavLink>
        ))}
        <div className="sync-footer">
          {sync === null && 'Connecting…'}
          {sync !== null && !sync.logged_in && 'Not logged in to Garmin'}
          {sync !== null && sync.logged_in && (
            <>
              {sync.status === 'running' ? sync.message || 'Syncing…' : `${sync.total_activities} activities`}
              {sync.last_sync_at && sync.status !== 'running' && (
                <div>Synced {new Date(sync.last_sync_at + 'Z').toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}</div>
              )}
            </>
          )}
        </div>
      </nav>
      <main className="content">
        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/activities" element={<Activities />} />
          <Route path="/activities/:id" element={<ActivityDetailPage />} />
          <Route path="/logbook" element={<Logbook />} />
          <Route path="/calendar" element={<Calendar />} />
          <Route path="/trends" element={<Trends />} />
          <Route path="/records" element={<Records />} />
          <Route path="/settings" element={<SettingsPage />} />
        </Routes>
      </main>
    </div>
  )
}
