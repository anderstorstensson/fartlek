import { useEffect, useMemo, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { ActivitySummary, fetchJson, useApi } from '../api'
import RouteThumb from '../components/RouteThumb'
import {
  formatDistance,
  formatDuration,
  formatPace,
  formatSportName,
  formatTime,
  locale,
  sportEmoji
} from '../format'

const PAGE_SIZE = 100

function weekKey(iso: string): string {
  const date = new Date(iso)
  const day = (date.getDay() + 6) % 7 // Monday = 0
  const monday = new Date(date)
  monday.setDate(date.getDate() - day)
  // Build from local date parts — toISOString would shift across UTC midnight.
  const y = monday.getFullYear()
  const m = String(monday.getMonth() + 1).padStart(2, '0')
  const d = String(monday.getDate()).padStart(2, '0')
  return `${y}-${m}-${d}`
}

function formatWeekLabel(key: string): string {
  const [y, m, d] = key.split('-').map(Number)
  const monday = new Date(y, m - 1, d)
  const sunday = new Date(monday)
  sunday.setDate(monday.getDate() + 6)
  const opts: Intl.DateTimeFormatOptions = { day: 'numeric', month: 'short' }
  return `${monday.toLocaleDateString(locale(), opts)} – ${sunday.toLocaleDateString(locale(), opts)}`
}

export default function Activities() {
  const navigate = useNavigate()
  const [sport, setSport] = useState('')
  const [query, setQuery] = useState('')
  const [debouncedQuery, setDebouncedQuery] = useState('')
  const [items, setItems] = useState<ActivitySummary[]>([])
  const [total, setTotal] = useState(0)
  const [error, setError] = useState<string | null>(null)
  const sports = useApi<string[]>('/api/activities/sports')

  useEffect(() => {
    const timer = setTimeout(() => setDebouncedQuery(query), 300)
    return () => clearTimeout(timer)
  }, [query])

  const baseUrl = useMemo(() => {
    const params = new URLSearchParams({ limit: String(PAGE_SIZE) })
    if (sport) params.set('sport', sport)
    if (debouncedQuery) params.set('q', debouncedQuery)
    return `/api/activities?${params.toString()}`
  }, [sport, debouncedQuery])

  useEffect(() => {
    let cancelled = false
    fetchJson<{ items: ActivitySummary[]; total: number }>(baseUrl)
      .then((body) => {
        if (cancelled) return
        setItems(body.items)
        setTotal(body.total)
        setError(null)
      })
      .catch((err: Error) => {
        if (!cancelled) setError(err.message)
      })
    return () => {
      cancelled = true
    }
  }, [baseUrl])

  const loadMore = () => {
    fetchJson<{ items: ActivitySummary[]; total: number }>(`${baseUrl}&offset=${items.length}`)
      .then((body) => setItems((current) => [...current, ...body.items]))
      .catch((err: Error) => setError(err.message))
  }

  const weeks = useMemo(() => {
    const grouped = new Map<string, ActivitySummary[]>()
    for (const activity of items) {
      const key = weekKey(activity.start_time_local)
      const list = grouped.get(key) ?? []
      grouped.set(key, [...list, activity])
    }
    return [...grouped.entries()]
  }, [items])

  return (
    <>
      <h1>Activities</h1>
      <div className="toolbar">
        <select value={sport} onChange={(e) => setSport(e.target.value)}>
          <option value="">All sports</option>
          <option value="running">All running</option>
          {sports.data?.map((name) => (
            <option key={name} value={name}>
              {formatSportName(name)}
            </option>
          ))}
        </select>
        <input
          type="text"
          placeholder="Search by name…"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
        />
        <span className="muted">{total} activities</span>
      </div>
      {error && <div className="error-box">{error}</div>}

      {weeks.map(([key, weekItems]) => {
        const runDist = weekItems
          .filter((a) => a.sport.includes('running'))
          .reduce((sum, a) => sum + a.distance_m, 0)
        const time = weekItems.reduce((sum, a) => sum + a.moving_s, 0)
        return (
          <section key={key}>
            <div className="week-header">
              <strong>{formatWeekLabel(key)}</strong>
              <span className="totals">
                {weekItems.length} activities · {formatDistance(runDist)} run ·{' '}
                {formatDuration(time)}
              </span>
            </div>
            <div className="table-wrap">
              <table>
                <tbody>
                  {weekItems.map((activity) => (
                    <tr
                      key={activity.id}
                      className="clickable"
                      onClick={() => navigate(`/activities/${activity.id}`)}
                    >
                      <td style={{ width: 110 }}>
                        {new Date(activity.start_time_local).toLocaleDateString(locale(), {
                          weekday: 'short',
                          day: 'numeric',
                          month: 'short'
                        })}
                        <div className="muted" style={{ fontSize: 12 }}>
                          {formatTime(activity.start_time_local)}
                        </div>
                      </td>
                      <td style={{ width: 100 }}>
                        <RouteThumb activityId={activity.id} hasGps={activity.has_gps} />
                      </td>
                      <td className="strong">
                        {sportEmoji(activity.sport)} {activity.name}
                        {activity.is_workout && <span className="badge workout">workout</span>}
                        {activity.has_analysis && (
                          <span title="Has a saved analysis" style={{ marginLeft: 6 }}>
                            🧠
                          </span>
                        )}
                        <div className="muted" style={{ fontSize: 12, fontWeight: 400 }}>
                          {formatSportName(activity.sport)}
                        </div>
                      </td>
                      <td>{activity.distance_m > 0 ? formatDistance(activity.distance_m) : '–'}</td>
                      <td>{formatDuration(activity.moving_s)}</td>
                      <td>
                        {activity.sport.includes('running')
                          ? formatPace(activity.avg_speed_mps)
                          : '–'}
                      </td>
                      <td>{activity.avg_hr ? `${Math.round(activity.avg_hr)} bpm` : '–'}</td>
                      <td>
                        {activity.trimp !== null && (
                          <span className="badge">TRIMP {activity.trimp.toFixed(0)}</span>
                        )}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </section>
        )
      })}

      {items.length === 0 && !error && <div className="empty-state">No activities found</div>}
      {items.length < total && (
        <div style={{ textAlign: 'center', marginTop: 20 }}>
          <button className="ghost" onClick={loadMore}>
            Load more ({items.length} / {total})
          </button>
        </div>
      )}
    </>
  )
}
