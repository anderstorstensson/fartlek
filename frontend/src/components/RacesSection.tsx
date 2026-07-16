import { FormEvent, useEffect, useState } from 'react'
import { fetchJson, Race } from '../api'
import { formatDate, formatDistance, formatDuration } from '../format'

const DISTANCE_PRESETS = [
  { label: '5K', meters: 5000 },
  { label: '10K', meters: 10000 },
  { label: 'Half marathon', meters: 21097.5 },
  { label: 'Marathon', meters: 42195 }
]

/** Parse "39:30" or "1:32:00" into seconds; empty string → null. */
function parseTime(text: string): number | null {
  const trimmed = text.trim()
  if (!trimmed) return null
  const parts = trimmed.split(':').map(Number)
  if (parts.some(Number.isNaN)) return null
  return parts.reduce((total, part) => total * 60 + part, 0)
}

export default function RacesSection() {
  const [races, setRaces] = useState<Race[]>([])
  const [error, setError] = useState<string | null>(null)
  const [name, setName] = useState('')
  const [day, setDay] = useState('')
  const [distance, setDistance] = useState(10000)
  const [target, setTarget] = useState('')

  const load = () => {
    fetchJson<Race[]>('/api/races')
      .then(setRaces)
      .catch((e: Error) => setError(e.message))
  }

  useEffect(load, [])

  const add = (event: FormEvent) => {
    event.preventDefault()
    setError(null)
    fetchJson<Race>('/api/races', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        name,
        day,
        distance_m: distance,
        target_time_s: parseTime(target)
      })
    })
      .then(() => {
        setName('')
        setDay('')
        setTarget('')
        load()
      })
      .catch((e: Error) => setError(e.message))
  }

  const remove = (id: number) => {
    fetchJson(`/api/races/${id}`, { method: 'DELETE' })
      .then(load)
      .catch((e: Error) => setError(e.message))
  }

  return (
    <>
      <h2>Goal races</h2>
      <div className="card">
        {error && <div className="error-box">{error}</div>}
        {races.length > 0 && (
          <div className="table-wrap" style={{ marginBottom: 14 }}>
            <table>
              <thead>
                <tr>
                  <th>Race</th>
                  <th>Date</th>
                  <th>Distance</th>
                  <th>Target</th>
                  <th>Predicted</th>
                  <th />
                </tr>
              </thead>
              <tbody>
                {races.map((race) => (
                  <tr key={race.id}>
                    <td className="strong">{race.name}</td>
                    <td>
                      {formatDate(race.day)}
                      {race.days_until !== null && race.days_until >= 0 && (
                        <span className="muted"> · in {race.days_until} d</span>
                      )}
                    </td>
                    <td>{formatDistance(race.distance_m)}</td>
                    <td>{race.target_time_s ? formatDuration(race.target_time_s) : '–'}</td>
                    <td>
                      {race.predicted_time_s ? formatDuration(race.predicted_time_s) : '–'}
                      {race.predicted_from && (
                        <div className="muted" style={{ fontSize: 11 }}>
                          from {race.predicted_from}
                        </div>
                      )}
                    </td>
                    <td>
                      <button className="ghost" onClick={() => remove(race.id)}>
                        Delete
                      </button>
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
              <div className="muted">Race name</div>
              <input value={name} onChange={(e) => setName(e.target.value)} required />
            </label>
            <label>
              <div className="muted">Date</div>
              <input type="date" value={day} onChange={(e) => setDay(e.target.value)} required />
            </label>
            <label>
              <div className="muted">Distance</div>
              <select value={distance} onChange={(e) => setDistance(Number(e.target.value))}>
                {DISTANCE_PRESETS.map((preset) => (
                  <option key={preset.label} value={preset.meters}>
                    {preset.label}
                  </option>
                ))}
              </select>
            </label>
            <label>
              <div className="muted">Target time (h:mm:ss, optional)</div>
              <input
                value={target}
                onChange={(e) => setTarget(e.target.value)}
                placeholder="39:30"
              />
            </label>
          </div>
          <button type="submit">Add race</button>
        </form>
        <p className="muted" style={{ fontSize: 12 }}>
          The predicted time is a Riegel extrapolation from your best efforts in the last 120
          days. The dashboard counts down to the next race and projects your form (TSB) to race
          day from the training plan.
        </p>
      </div>
    </>
  )
}
