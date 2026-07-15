import { FormEvent, useEffect, useState } from 'react'
import { fetchJson, Settings, SyncStatus } from '../api'
import { formatPaceFromSeconds } from '../format'

export default function SettingsPage() {
  const [settings, setSettings] = useState<Settings | null>(null)
  const [sync, setSync] = useState<SyncStatus | null>(null)
  const [message, setMessage] = useState<string | null>(null)
  const [error, setError] = useState<string | null>(null)

  const loadAll = () => {
    fetchJson<Settings>('/api/settings').then(setSettings).catch((e: Error) => setError(e.message))
    fetchJson<SyncStatus>('/api/sync/status').then(setSync).catch(() => undefined)
  }

  useEffect(() => {
    loadAll()
    const timer = setInterval(
      () => fetchJson<SyncStatus>('/api/sync/status').then(setSync).catch(() => undefined),
      5000
    )
    return () => clearInterval(timer)
  }, [])

  const save = (event: FormEvent) => {
    event.preventDefault()
    if (!settings) return
    setMessage(null)
    setError(null)
    fetchJson<Settings>('/api/settings', {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        resting_hr: settings.resting_hr,
        max_hr: settings.max_hr,
        lthr: settings.lthr,
        threshold_pace_s_per_km: settings.threshold_pace_s_per_km,
        sex: settings.sex
      })
    })
      .then((updated) => {
        setSettings(updated)
        setMessage('Saved. Load metrics are being recomputed in the background.')
      })
      .catch((e: Error) => setError(e.message))
  }

  const triggerSync = (full: boolean) => {
    fetchJson('/api/sync' + (full ? '?full=true' : ''), { method: 'POST' })
      .then(() => setMessage(full ? 'Full backfill started…' : 'Sync started…'))
      .catch((e: Error) => setError(e.message))
  }

  const update = (patch: Partial<Settings>) => {
    setSettings((current) => (current ? { ...current, ...patch } : current))
  }

  return (
    <>
      <h1>Settings</h1>
      {error && <div className="error-box">{error}</div>}
      {message && <div className="card" style={{ marginBottom: 16 }}>{message}</div>}

      <h2>Garmin sync</h2>
      <div className="card">
        {sync && !sync.logged_in && (
          <p>
            Not logged in. Run <code>make login</code> in the project directory to
            authenticate with Garmin Connect (tokens are stored locally; your password is not
            saved).
          </p>
        )}
        {sync && sync.logged_in && (
          <p className="muted">
            {sync.total_activities} activities in the database
            {sync.last_sync_at &&
              ` · last sync ${new Date(sync.last_sync_at + 'Z').toLocaleString()}`}
            {sync.status === 'running' && ` · ${sync.message || 'syncing…'}`}
            {sync.status === 'error' && (
              <span style={{ color: 'var(--critical)' }}> · {sync.message}</span>
            )}
          </p>
        )}
        <div style={{ display: 'flex', gap: 10 }}>
          <button onClick={() => triggerSync(false)} disabled={sync?.status === 'running'}>
            Sync now
          </button>
          <button
            className="ghost"
            onClick={() => triggerSync(true)}
            disabled={sync?.status === 'running'}
          >
            Full backfill
          </button>
        </div>
      </div>

      <h2>Athlete</h2>
      {settings && (
        <form className="card" onSubmit={save}>
          <div className="stat-grid" style={{ marginBottom: 16 }}>
            <label>
              <div className="muted">Resting HR</div>
              <input
                type="number"
                value={settings.resting_hr}
                onChange={(e) => update({ resting_hr: Number(e.target.value) })}
              />
            </label>
            <label>
              <div className="muted">Max HR</div>
              <input
                type="number"
                value={settings.max_hr}
                onChange={(e) => update({ max_hr: Number(e.target.value) })}
              />
            </label>
            <label>
              <div className="muted">Lactate threshold HR</div>
              <input
                type="number"
                value={settings.lthr}
                onChange={(e) => update({ lthr: Number(e.target.value) })}
              />
            </label>
            <label>
              <div className="muted">
                Threshold pace (s/km) = {formatPaceFromSeconds(settings.threshold_pace_s_per_km)}{' '}
                /km
              </div>
              <input
                type="number"
                value={settings.threshold_pace_s_per_km}
                onChange={(e) => update({ threshold_pace_s_per_km: Number(e.target.value) })}
              />
            </label>
            <label>
              <div className="muted">Sex (TRIMP coefficients)</div>
              <select value={settings.sex} onChange={(e) => update({ sex: e.target.value })}>
                <option value="male">male</option>
                <option value="female">female</option>
              </select>
            </label>
          </div>
          <button type="submit">Save settings</button>
        </form>
      )}

      {settings && (
        <>
          <h2>Heart-rate zones (% of max HR)</h2>
          <div className="card table-wrap" style={{ padding: 0 }}>
            <table>
              <tbody>
                {settings.zones.map((zone) => (
                  <tr key={zone.name}>
                    <td className="strong" style={{ width: 60 }}>
                      {zone.name}
                    </td>
                    <td>
                      {zone.low_bpm}
                      {zone.high_bpm ? ` – ${zone.high_bpm}` : '+'} bpm
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </>
      )}
    </>
  )
}
