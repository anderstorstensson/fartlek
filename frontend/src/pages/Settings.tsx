import { FormEvent, useEffect, useState } from 'react'
import { fetchJson, Settings, SyncStatus } from '../api'
import RacesSection from '../components/RacesSection'
import { formatPaceFromSeconds, locale, setDisplayLocale } from '../format'

const PACE_ZONE_LABELS = ['recovery', 'easy', 'marathon', 'threshold', 'VO2max+']

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
        sex: settings.sex,
        zone_mode: settings.zone_mode,
        manual_zone_bounds: settings.manual_zone_bounds,
        rtss_use_gap: settings.rtss_use_gap,
        pace_zone_mode: settings.pace_zone_mode,
        manual_pace_zone_bounds: settings.manual_pace_zone_bounds,
        coaching_tone: settings.coaching_tone,
        display_locale: settings.display_locale
      })
    })
      .then((updated) => {
        setSettings(updated)
        setDisplayLocale(updated.display_locale)
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
              ` · last sync ${new Date(sync.last_sync_at + 'Z').toLocaleString(locale())}`}
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

      <RacesSection />

      <h2>Athlete</h2>
      {settings && (
        <form className="card" onSubmit={save}>
          <div className="form-grid" style={{ marginBottom: 16 }}>
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
              <div className="muted">Threshold pace (s/km)</div>
              <input
                type="number"
                value={settings.threshold_pace_s_per_km}
                onChange={(e) => update({ threshold_pace_s_per_km: Number(e.target.value) })}
              />
              <div className="muted" style={{ fontSize: 12, marginTop: 2 }}>
                = {formatPaceFromSeconds(settings.threshold_pace_s_per_km)}/km
              </div>
            </label>
            <label>
              <div className="muted">Sex (TRIMP coefficients)</div>
              <select value={settings.sex} onChange={(e) => update({ sex: e.target.value })}>
                <option value="male">male</option>
                <option value="female">female</option>
              </select>
            </label>
            <label>
              <div className="muted">rTSS pace source</div>
              <select
                value={settings.rtss_use_gap ? 'gap' : 'raw'}
                onChange={(e) => update({ rtss_use_gap: e.target.value === 'gap' })}
              >
                <option value="gap">Grade-adjusted pace (GAP)</option>
                <option value="raw">Raw pace</option>
              </select>
              <div className="muted" style={{ fontSize: 12, marginTop: 2 }}>
                Switch to raw pace if the watch&apos;s barometric altitude is unreliable.
              </div>
            </label>
            <label>
              <div className="muted">Coaching tone</div>
              <select
                value={settings.coaching_tone}
                onChange={(e) =>
                  update({ coaching_tone: e.target.value as Settings['coaching_tone'] })
                }
              >
                <option value="drill">Drill sergeant — yells at mistakes</option>
                <option value="harsh">Harsh — frank, no sugarcoating</option>
                <option value="balanced">Balanced — honest, encouraging</option>
                <option value="supportive">Supportive — gentle framing</option>
              </select>
              <div className="muted" style={{ fontSize: 12, marginTop: 2 }}>
                How the AI coach talks in analyses and plans. Tone only — the numbers and
                recommendations never change.
              </div>
            </label>
            <label>
              <div className="muted">Date &amp; time format</div>
              <select
                value={settings.display_locale}
                onChange={(e) => update({ display_locale: e.target.value })}
              >
                <option value="">Browser default</option>
                <option value="en-GB">European — 16/07/2026, 20:46</option>
                <option value="sv-SE">ISO / Swedish — 2026-07-16, 20:46</option>
                <option value="en-US">US — 7/16/2026, 8:46 PM</option>
              </select>
              <div className="muted" style={{ fontSize: 12, marginTop: 2 }}>
                Date-picker inputs follow the browser&apos;s own language setting and
                can&apos;t be changed here.
              </div>
            </label>
          </div>
          <button type="submit">Save settings</button>
        </form>
      )}

      {settings && (
        <>
          <h2>Heart-rate zones</h2>
          <div className="card">
            <label>
              <div className="muted">Zones based on</div>
              <select
                value={settings.zone_mode}
                onChange={(e) => {
                  const mode = e.target.value as Settings['zone_mode']
                  const patch: Partial<Settings> = { zone_mode: mode }
                  if (mode === 'manual' && !settings.manual_zone_bounds) {
                    patch.manual_zone_bounds = settings.zones.map((z) => z.low_bpm)
                  }
                  update(patch)
                }}
              >
                <option value="max_hr">% of max HR</option>
                <option value="lthr">% of lactate threshold HR</option>
                <option value="manual">Manual (bpm)</option>
              </select>
            </label>
            {settings.zone_mode === 'manual' && settings.manual_zone_bounds && (
              <div className="form-grid" style={{ marginTop: 12 }}>
                {settings.manual_zone_bounds.map((bound, i) => (
                  <label key={i}>
                    <div className="muted">Z{i + 1} from (bpm)</div>
                    <input
                      type="number"
                      value={bound}
                      onChange={(e) => {
                        const bounds = settings.manual_zone_bounds!.map((b, j) =>
                          j === i ? Number(e.target.value) : b
                        )
                        update({ manual_zone_bounds: bounds })
                      }}
                    />
                  </label>
                ))}
              </div>
            )}
            <p className="muted" style={{ fontSize: 12 }}>
              Save settings to recalculate the zone table below.
            </p>
            <div className="table-wrap">
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
          </div>

          <h2>Pace zones</h2>
          <div className="card">
            <label>
              <div className="muted">Zones based on</div>
              <select
                value={settings.pace_zone_mode}
                onChange={(e) => {
                  const mode = e.target.value as Settings['pace_zone_mode']
                  const patch: Partial<Settings> = { pace_zone_mode: mode }
                  if (mode === 'manual' && !settings.manual_pace_zone_bounds) {
                    patch.manual_pace_zone_bounds = settings.pace_zones.map((z) =>
                      Math.round(1000 / z.low_speed_mps)
                    )
                  }
                  update(patch)
                }}
              >
                <option value="threshold">% of threshold pace</option>
                <option value="manual">Manual (s/km)</option>
              </select>
            </label>
            {settings.pace_zone_mode === 'manual' && settings.manual_pace_zone_bounds && (
              <div className="form-grid" style={{ marginTop: 12 }}>
                {settings.manual_pace_zone_bounds.map((bound, i) => (
                  <label key={i}>
                    <div className="muted">Z{i + 1} from (s/km)</div>
                    <input
                      type="number"
                      value={bound}
                      onChange={(e) => {
                        const bounds = settings.manual_pace_zone_bounds!.map((b, j) =>
                          j === i ? Number(e.target.value) : b
                        )
                        update({ manual_pace_zone_bounds: bounds })
                      }}
                    />
                    <div className="muted" style={{ fontSize: 12, marginTop: 2 }}>
                      = {formatPaceFromSeconds(bound)}/km
                    </div>
                  </label>
                ))}
              </div>
            )}
            <p className="muted" style={{ fontSize: 12 }}>
              Each bound is the zone&apos;s slowest pace; bounds must get faster from Z1 to Z5.
              Save settings to recalculate the table below. The activity pages classify time in
              these zones using grade-adjusted pace.
            </p>
            <div className="table-wrap">
              <table>
                <tbody>
                  {settings.pace_zones.map((zone, i) => (
                    <tr key={zone.name}>
                      <td className="strong" style={{ width: 60 }}>
                        {zone.name}
                      </td>
                      <td style={{ width: 110 }}>{PACE_ZONE_LABELS[i]}</td>
                      <td>
                        {formatPaceFromSeconds(1000 / zone.low_speed_mps)}
                        {zone.high_speed_mps
                          ? ` – ${formatPaceFromSeconds(1000 / zone.high_speed_mps)}`
                          : ' and faster'}{' '}
                        /km
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        </>
      )}
    </>
  )
}
