import { FormEvent, useEffect, useState } from 'react'
import { fetchJson, Niggle } from '../api'
import { formatDate } from '../format'
import { describe, isoDay, SIDES, SITES, TIERS, writable } from '../niggles'

export default function NigglesSection() {
  const [niggles, setNiggles] = useState<Niggle[]>([])
  const [error, setError] = useState<string | null>(null)
  const [site, setSite] = useState('achilles')
  const [side, setSide] = useState('na')
  const [onset, setOnset] = useState(isoDay())
  const [tier, setTier] = useState(1)
  const [trigger, setTrigger] = useState('')
  const [note, setNote] = useState('')
  const [resolving, setResolving] = useState<number | null>(null)
  const [response, setResponse] = useState('')
  const [resolvedOn, setResolvedOn] = useState(isoDay())

  const load = () => {
    fetchJson<Niggle[]>('/api/niggles')
      .then(setNiggles)
      .catch((e: Error) => setError(e.message))
  }

  useEffect(load, [])

  const save = (niggle: Niggle, changes: Partial<ReturnType<typeof writable>>) =>
    fetchJson<Niggle>(`/api/niggles/${niggle.id}`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ ...writable(niggle), ...changes })
    })
      .then(() => {
        setResolving(null)
        setResponse('')
        load()
      })
      .catch((e: Error) => setError(e.message))

  const add = (event: FormEvent) => {
    event.preventDefault()
    setError(null)
    fetchJson<Niggle>('/api/niggles', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        site,
        side,
        onset_date: onset,
        tier,
        trigger,
        note
      })
    })
      .then(() => {
        setTrigger('')
        setNote('')
        load()
      })
      .catch((e: Error) => setError(e.message))
  }

  /** Open the resolve form on a row, starting from a clean slate — otherwise text
   *  typed for one episode follows you to the next. */
  const openResolve = (id: number) => {
    setResolving(id)
    setResponse('')
    setResolvedOn(isoDay())
  }

  const cancelResolve = () => {
    setResolving(null)
    setResponse('')
  }

  const remove = (id: number) => {
    if (!window.confirm('Delete this entry? Injury history is what the coach uses to spot patterns.'))
      return
    fetchJson(`/api/niggles/${id}`, { method: 'DELETE' })
      .then(load)
      .catch((e: Error) => setError(e.message))
  }

  const active = niggles.filter((n) => n.active)

  return (
    <>
      <h2>Niggles &amp; injuries</h2>
      <div className="card">
        {error && <div className="error-box">{error}</div>}

        {active.some((n) => n.tier === 3) && (
          <div className="notice-box">
            You have an entry flagged for referral. That is a clinician's call, not a training
            adjustment — the coach will not plan around it until it is resolved.
          </div>
        )}

        {niggles.length > 0 && (
          <div className="table-wrap" style={{ marginBottom: 14 }}>
            <table>
              <thead>
                <tr>
                  <th>Site</th>
                  <th>Onset</th>
                  <th>Tier</th>
                  <th>Trigger</th>
                  <th>Status</th>
                  <th />
                </tr>
              </thead>
              <tbody>
                {niggles.map((niggle) => (
                  <tr key={niggle.id}>
                    <td className="strong">
                      {describe(niggle)}
                      {niggle.note && (
                        <div className="muted" style={{ fontSize: 11 }}>{niggle.note}</div>
                      )}
                    </td>
                    <td>{formatDate(niggle.onset_date)}</td>
                    <td>
                      <span className="badge">{TIERS[niggle.tier]?.label ?? niggle.tier}</span>
                    </td>
                    <td className="muted" style={{ fontSize: 12 }}>{niggle.trigger || '–'}</td>
                    <td>
                      {niggle.active ? (
                        <span className="strong">Active</span>
                      ) : (
                        <>
                          Resolved {formatDate(niggle.resolved_date as string)}
                          {niggle.duration_days !== null && (
                            <div className="muted" style={{ fontSize: 11 }}>
                              {niggle.duration_days} days
                            </div>
                          )}
                        </>
                      )}
                      {niggle.response && (
                        <div className="muted" style={{ fontSize: 11 }}>{niggle.response}</div>
                      )}
                    </td>
                    <td>
                      {niggle.active ? (
                        <button
                          className="ghost"
                          onClick={() =>
                            resolving === niggle.id ? cancelResolve() : openResolve(niggle.id)
                          }
                        >
                          Resolve
                        </button>
                      ) : (
                        <button
                          className="ghost"
                          onClick={() => save(niggle, { resolved_date: null })}
                        >
                          Reopen
                        </button>
                      )}
                      <button className="ghost danger" onClick={() => remove(niggle.id)}>
                        Delete
                      </button>
                      {resolving === niggle.id && (
                        <div className="form-grid" style={{ marginTop: 8 }}>
                          <label>
                            <div className="muted">Resolved on</div>
                            <input
                              type="date"
                              value={resolvedOn}
                              onChange={(e) => setResolvedOn(e.target.value)}
                            />
                          </label>
                          <label>
                            <div className="muted">What it responded to</div>
                            <input
                              value={response}
                              onChange={(e) => setResponse(e.target.value)}
                              placeholder="cut speed 2 wks, kept easy volume"
                            />
                          </label>
                          <div style={{ display: 'flex', gap: 8, alignItems: 'flex-end' }}>
                            <button
                              onClick={() =>
                                save(niggle, { resolved_date: resolvedOn, response })
                              }
                            >
                              Save
                            </button>
                            <button className="ghost" onClick={cancelResolve}>
                              Cancel
                            </button>
                          </div>
                        </div>
                      )}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}

        <form onSubmit={add}>
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
              <div className="muted">Started</div>
              <input
                type="date"
                value={onset}
                onChange={(e) => setOnset(e.target.value)}
                required
              />
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
              <div className="muted">What preceded it</div>
              <input
                value={trigger}
                onChange={(e) => setTrigger(e.target.value)}
                placeholder="31 km long run, biggest in 4 weeks"
              />
            </label>
            <label>
              <div className="muted">Note</div>
              <input
                value={note}
                onChange={(e) => setNote(e.target.value)}
                placeholder="morning stiffness, eases after 10 min"
              />
            </label>
          </div>
          <button type="submit">Log it</button>
        </form>

        <p className="muted" style={{ fontSize: 12 }}>
          Log niggles early — a previous injury is the strongest known risk factor for the next
          one, so this history is what lets the coach spot a pattern and adjust load before it
          becomes a lay-off. Record where it is, not what you think it is: the coach manages load
          and refers, it does not diagnose. Anything with pinpoint bone tenderness, night pain,
          numbness or pain that worsens through a run belongs with a clinician first.
        </p>
      </div>
    </>
  )
}
