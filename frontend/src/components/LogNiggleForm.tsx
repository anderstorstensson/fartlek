import { FormEvent, useState } from 'react'
import { fetchJson, Niggle } from '../api'
import { formatDistance } from '../format'
import { isoDay, SIDES, SITES, TIERS } from '../niggles'

/** Log a niggle from the run it started in.
 *
 *  This is the entry point that matters: most overuse running injuries trace to a
 *  single session rather than accumulating invisibly, so capturing which run it
 *  began in is what later lets the coach line the onset up against the load that
 *  preceded it. It is also the only place onset_activity_id gets set.
 */
export default function LogNiggleForm({
  activity,
  onSaved,
  onCancel
}: {
  activity: { id: number; name: string; start_time_local: string; distance_m: number }
  onSaved: () => void
  onCancel: () => void
}) {
  const [site, setSite] = useState('achilles')
  const [side, setSide] = useState('na')
  const [tier, setTier] = useState(1)
  const [note, setNote] = useState('')
  const [error, setError] = useState<string | null>(null)
  const [saving, setSaving] = useState(false)

  const submit = (event: FormEvent) => {
    event.preventDefault()
    setError(null)
    setSaving(true)
    const distance = activity.distance_m > 0 ? ` (${formatDistance(activity.distance_m)})` : ''
    fetchJson<Niggle>('/api/niggles', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        site,
        side,
        onset_date: isoDay(activity.start_time_local),
        onset_activity_id: activity.id,
        tier,
        trigger: `${activity.name}${distance}`,
        note
      })
    })
      .then(onSaved)
      .catch((e: Error) => setError(e.message))
      .finally(() => setSaving(false))
  }

  return (
    <form className="card" style={{ marginBottom: 16 }} onSubmit={submit}>
      {error && <div className="error-box">{error}</div>}
      <div className="form-grid" style={{ marginBottom: 12 }}>
        <label>
          <div className="muted">Where</div>
          <select value={site} onChange={(e) => setSite(e.target.value)}>
            {SITES.map((s) => (
              <option key={s.value} value={s.value}>{s.label}</option>
            ))}
          </select>
        </label>
        <label>
          <div className="muted">Side</div>
          <select value={side} onChange={(e) => setSide(e.target.value)}>
            {SIDES.map((s) => (
              <option key={s.value} value={s.value}>{s.label}</option>
            ))}
          </select>
        </label>
        <label>
          <div className="muted">Tier</div>
          <select value={tier} onChange={(e) => setTier(Number(e.target.value))}>
            {[1, 2, 3].map((t) => (
              <option key={t} value={t}>{TIERS[t].option}</option>
            ))}
          </select>
        </label>
        <label>
          <div className="muted">Note</div>
          <input
            value={note}
            onChange={(e) => setNote(e.target.value)}
            placeholder="tightened up around 20 km, eased off after"
          />
        </label>
      </div>
      <div style={{ display: 'flex', gap: 8 }}>
        <button type="submit" disabled={saving}>
          {saving ? 'Saving…' : 'Log it'}
        </button>
        <button type="button" className="ghost" onClick={onCancel}>
          Cancel
        </button>
      </div>
      <p className="muted" style={{ fontSize: 12, marginBottom: 0 }}>
        Dated to this run, so the coach can line the onset up against the load that led into
        it. Record where it is, not what you think it is. Manage it from Settings → Niggles
        &amp; injuries.
      </p>
    </form>
  )
}
