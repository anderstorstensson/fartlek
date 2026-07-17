import { useEffect, useState } from 'react'
import { NavLink, Route, Routes } from 'react-router-dom'
import { fetchJson, SyncStatus } from './api'
import { locale, setDisplayLocale, setUnits, Units, units } from './format'
import Activities from './pages/Activities'
import ActivityDetailPage from './pages/ActivityDetail'
import Analysis from './pages/Analysis'
import Calendar from './pages/Calendar'
import Coach from './pages/Coach'
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
  { to: '/analysis', label: 'Analysis', icon: '🧠' },
  { to: '/coach', label: 'Coach', icon: '🎓' },
  { to: '/records', label: 'Records', icon: '🏆' },
  { to: '/settings', label: 'Settings', icon: '⚙️' }
]

export default function App() {
  const [sync, setSync] = useState<SyncStatus | null>(null)
  // Bumped when a saved display preference (locale, pace unit) differs from
  // the cached one, so the whole tree re-renders with the right format.
  const [, setDisplayVersion] = useState(0)

  useEffect(() => {
    let cancelled = false

    fetchJson<{ display_locale: string; units: Units }>('/api/settings')
      .then((settings) => {
        if (cancelled) return
        if ((settings.display_locale || undefined) !== locale()) {
          setDisplayLocale(settings.display_locale)
          setDisplayVersion((v) => v + 1)
        }
        if (settings.units !== units()) {
          setUnits(settings.units)
          setDisplayVersion((v) => v + 1)
        }
      })
      .catch(() => undefined)

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
                <div>Synced {new Date(sync.last_sync_at + 'Z').toLocaleTimeString(locale(), { hour: '2-digit', minute: '2-digit' })}</div>
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
          <Route path="/analysis" element={<Analysis />} />
          <Route path="/coach" element={<Coach />} />
          <Route path="/trends" element={<Trends />} />
          <Route path="/records" element={<Records />} />
          <Route path="/settings" element={<SettingsPage />} />
        </Routes>
      </main>
    </div>
  )
}
