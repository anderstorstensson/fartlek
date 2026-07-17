import { FormEvent, useCallback, useState } from 'react'
import { Link, useNavigate, useParams } from 'react-router-dom'
import {
  ActivityDetail,
  AnalysisNote,
  CoachStatus,
  deleteActivity,
  fetchJson,
  Streams,
  useApi
} from '../api'
import { analyzePrompt, coachUrl } from '../coachLink'
import ActivityMap from '../components/ActivityMap'
import NoteCard from '../components/NoteCard'
import PaceZoneChart from '../components/PaceZoneChart'
import RelativeEffortCard from '../components/RelativeEffortCard'
import SplitsChart from '../components/SplitsChart'
import StreamCharts from '../components/StreamCharts'
import ZoneChart from '../components/ZoneChart'
import {
  formatDate,
  formatDistance,
  formatDuration,
  formatPace,
  formatSportName,
  formatTime,
  sportEmoji
} from '../format'

function formatWeatherSub(windMps: number | null, humidityPct: number | null): string | undefined {
  const parts = []
  if (windMps !== null) parts.push(`${Math.round(windMps)} m/s wind`)
  if (humidityPct !== null) parts.push(`${Math.round(humidityPct)}% RH`)
  return parts.length ? parts.join(' · ') : undefined
}

const TAGS = ['', 'easy', 'recovery', 'long', 'intervals', 'tempo', 'race', 'cross']

function EditForm({
  activity,
  onSaved,
  onCancel,
  onDeleted
}: {
  activity: ActivityDetail
  onSaved: () => void
  onCancel: () => void
  onDeleted: () => void
}) {
  const [name, setName] = useState(activity.name)
  const [tag, setTag] = useState(activity.tag ?? '')
  const [note, setNote] = useState(activity.user_note)
  const [error, setError] = useState<string | null>(null)
  const [deleting, setDeleting] = useState(false)

  const save = (event: FormEvent) => {
    event.preventDefault()
    fetchJson(`/api/activities/${activity.id}`, {
      method: 'PATCH',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ name, tag, user_note: note })
    })
      .then(onSaved)
      .catch((e: Error) => setError(e.message))
  }

  const remove = () => {
    if (
      !window.confirm(
        `Delete "${activity.name}"? This removes the activity and its charts, laps ` +
          'and records. A synced Garmin activity will reappear on the next sync; ' +
          'manually-added ones stay gone. This cannot be undone.'
      )
    )
      return
    setError(null)
    setDeleting(true)
    deleteActivity(activity.id)
      .then(onDeleted)
      .catch((e: Error) => {
        setError(e.message)
        setDeleting(false)
      })
  }

  return (
    <form className="card" style={{ marginBottom: 16 }} onSubmit={save}>
      {error && <div className="error-box">{error}</div>}
      <div className="form-grid" style={{ marginBottom: 12 }}>
        <label style={{ gridColumn: 'span 2' }}>
          <div className="muted">Title</div>
          <input value={name} onChange={(e) => setName(e.target.value)} required />
        </label>
        <label>
          <div className="muted">Tag</div>
          <select value={tag} onChange={(e) => setTag(e.target.value)}>
            {TAGS.map((t) => (
              <option key={t} value={t}>
                {t || (activity.is_workout ? '(auto: workout)' : '(none)')}
              </option>
            ))}
          </select>
          <div className="muted" style={{ fontSize: 12, marginTop: 2 }}>
            {activity.is_workout
              ? 'Interval structure was auto-detected; a tag replaces the generic "workout" badge.'
              : 'Your session label — shows as a badge and guides the coach.'}
          </div>
        </label>
      </div>
      <label style={{ display: 'block', marginBottom: 12 }}>
        <div className="muted">Your note (visible to the AI coach in analyses)</div>
        <textarea
          value={note}
          onChange={(e) => setNote(e.target.value)}
          rows={3}
          style={{ width: '100%', boxSizing: 'border-box', marginTop: 4 }}
          placeholder="e.g. felt flat, slept 4h · new shoes · raced this one"
        />
      </label>
      <div style={{ display: 'flex', gap: 10, alignItems: 'center' }}>
        <button type="submit" disabled={deleting}>
          Save
        </button>
        <button type="button" className="ghost" onClick={onCancel} disabled={deleting}>
          Cancel
        </button>
        <button
          type="button"
          className="ghost danger"
          onClick={remove}
          disabled={deleting}
          style={{ marginLeft: 'auto' }}
        >
          {deleting ? 'Deleting…' : 'Delete activity'}
        </button>
      </div>
    </form>
  )
}

function DynamicsLine({ activity }: { activity: ActivityDetail }) {
  const parts: string[] = []
  if (activity.avg_vertical_oscillation_mm !== null)
    parts.push(`vertical oscillation ${activity.avg_vertical_oscillation_mm.toFixed(0)} mm`)
  if (activity.avg_vertical_ratio_pct !== null)
    parts.push(`vertical ratio ${activity.avg_vertical_ratio_pct.toFixed(1)}%`)
  if (activity.avg_stance_time_ms !== null)
    parts.push(`ground contact ${activity.avg_stance_time_ms.toFixed(0)} ms`)
  if (activity.avg_step_length_mm !== null)
    parts.push(`step length ${(activity.avg_step_length_mm / 10).toFixed(0)} cm`)
  if (activity.avg_respiration_brpm !== null)
    parts.push(`respiration ${activity.avg_respiration_brpm.toFixed(0)} brpm`)
  if (parts.length === 0) return null
  return (
    <p className="muted" style={{ fontSize: 13 }}>
      Running dynamics: {parts.join(' · ')}
    </p>
  )
}

function Stat({ label, value, sub }: { label: string; value: string; sub?: string }) {
  return (
    <div className="stat-tile card">
      <div className="label">{label}</div>
      <div className="value" style={{ fontSize: 17 }}>
        {value}
      </div>
      {sub && <div className="delta">{sub}</div>}
    </div>
  )
}

export default function ActivityDetailPage() {
  const { id } = useParams()
  const navigate = useNavigate()
  const [version, setVersion] = useState(0)
  const [editing, setEditing] = useState(false)
  const detail = useApi<ActivityDetail>(id ? `/api/activities/${id}?v=${version}` : null)
  const streams = useApi<Streams>(id ? `/api/activities/${id}/streams` : null)
  const notes = useApi<AnalysisNote[]>(id ? `/api/notes?activity_id=${id}` : null)
  const coachStatus = useApi<CoachStatus>('/api/coach/status')
  const coachReady =
    coachStatus.data?.enabled === true && coachStatus.data?.cli_available === true

  // Chart hover → map marker. The chart reports a stream index; resolve it to
  // the nearest GPS fix (samples can lack a position, e.g. in tunnels).
  const [hoverPoint, setHoverPoint] = useState<[number, number] | null>(null)
  const streamData = streams.data
  const handleHoverIndex = useCallback(
    (index: number | null) => {
      if (index === null || !streamData) {
        setHoverPoint(null)
        return
      }
      const { lat, lng } = streamData
      for (let offset = 0; offset < 25; offset++) {
        for (const j of offset === 0 ? [index] : [index - offset, index + offset]) {
          if (j >= 0 && j < lat.length && lat[j] !== null && lng[j] !== null) {
            setHoverPoint([lat[j] as number, lng[j] as number])
            return
          }
        }
      }
      setHoverPoint(null)
    },
    [streamData]
  )

  if (detail.error) return <div className="error-box">Failed to load: {detail.error}</div>
  if (!detail.data) return <p className="muted">Loading…</p>

  const activity = detail.data
  const isRun = activity.sport.includes('running')

  return (
    <>
      <p style={{ margin: '0 0 4px' }}>
        <Link to="/activities" className="muted">
          ← Activities
        </Link>
      </p>
      <h1 style={{ marginBottom: 4 }}>
        {sportEmoji(activity.sport)} {activity.name}
        {activity.tag ? (
          <span className="badge workout">{activity.tag}</span>
        ) : (
          activity.is_workout && <span className="badge workout">workout</span>
        )}
      </h1>
      <p className="muted" style={{ marginTop: 0 }}>
        {formatSportName(activity.sport)} · {formatDate(activity.start_time_local)} at{' '}
        {formatTime(activity.start_time_local)}
        {' · '}
        <button
          className="ghost"
          style={{ padding: '2px 10px', fontSize: 12 }}
          onClick={() => setEditing(!editing)}
        >
          Edit
        </button>
        {coachReady && (
          <>
            {' '}
            <Link
              to={coachUrl(analyzePrompt(activity))}
              className="btn-ghost"
              style={{ padding: '2px 10px', fontSize: 12 }}
            >
              🎓 {activity.tag === 'race' ? 'Race analysis with the coach' : 'Analyze with the coach'}
            </Link>
          </>
        )}
      </p>

      {editing && (
        <EditForm
          activity={activity}
          onSaved={() => {
            setEditing(false)
            setVersion((v) => v + 1)
          }}
          onCancel={() => setEditing(false)}
          onDeleted={() => navigate('/activities')}
        />
      )}

      {activity.user_note && !editing && (
        <div className="card" style={{ marginBottom: 16 }}>
          <span className="badge">your note</span>
          <span style={{ marginLeft: 10 }}>{activity.user_note}</span>
        </div>
      )}

      <div className="stat-grid dense" style={{ marginBottom: 20 }}>
        {activity.distance_m > 0 && <Stat label="Distance" value={formatDistance(activity.distance_m)} />}
        <Stat
          label="Moving time"
          value={formatDuration(activity.moving_s)}
          sub={activity.calories !== null ? `${Math.round(activity.calories)} kcal` : undefined}
        />
        {isRun && (
          <Stat
            label="Avg pace"
            value={formatPace(activity.avg_speed_mps)}
            sub={
              activity.gap_speed_mps !== null
                ? `GAP ${formatPace(activity.gap_speed_mps)}`
                : undefined
            }
          />
        )}
        {activity.avg_hr !== null && (
          <Stat
            label="Heart rate"
            value={`${Math.round(activity.avg_hr)} / ${activity.max_hr ? Math.round(activity.max_hr) : '–'}`}
            sub="avg / max bpm"
          />
        )}
        {activity.ascent_m !== null && activity.ascent_m > 0 && (
          <Stat label="Ascent" value={`${Math.round(activity.ascent_m)} m`} />
        )}
        {(activity.trimp !== null || activity.rtss !== null) && (
          <Stat
            label="Load"
            value={[
              activity.trimp !== null ? activity.trimp.toFixed(0) : null,
              activity.rtss !== null ? activity.rtss.toFixed(0) : null
            ]
              .filter((v) => v !== null)
              .join(' · ')}
            sub={
              activity.trimp !== null && activity.rtss !== null
                ? 'TRIMP · rTSS'
                : activity.trimp !== null
                  ? 'TRIMP'
                  : 'rTSS'
            }
          />
        )}
        {activity.avg_power_w !== null && (
          <Stat label="Power" value={`${Math.round(activity.avg_power_w)} W`} />
        )}
        {activity.decoupling_pct !== null && (
          <Stat
            label="Decoupling"
            value={`${activity.decoupling_pct.toFixed(1)}%`}
            sub={
              activity.efficiency_index !== null
                ? `EF ${activity.efficiency_index.toFixed(2)}`
                : undefined
            }
          />
        )}
        {activity.weather_temp_c !== null && (
          <Stat
            label="Weather"
            value={`${Math.round(activity.weather_temp_c)}°C`}
            sub={formatWeatherSub(activity.weather_wind_mps, activity.weather_humidity_pct)}
          />
        )}
      </div>

      {id && <RelativeEffortCard activityId={Number(id)} />}

      <DynamicsLine activity={activity} />

      {activity.best_efforts.length > 0 && (
        <p>
          {activity.best_efforts.map((effort) => (
            <span className="badge" key={effort.label} style={{ marginRight: 8 }}>
              {effort.label}: {formatDuration(effort.duration_s)}
            </span>
          ))}
        </p>
      )}

      {notes.data && notes.data.length > 0 && (
        <>
          <h2>Analysis</h2>
          {notes.data.map((note) => (
            <NoteCard key={note.id} note={note} showActivityLink={false} />
          ))}
        </>
      )}

      {streams.data && <ActivityMap streams={streams.data} hoverPoint={hoverPoint} />}
      {streams.data && (
        <StreamCharts
          streams={streams.data}
          activity={activity}
          onHoverIndex={handleHoverIndex}
        />
      )}
      {id && isRun && <SplitsChart key={version} activityId={Number(id)} />}
      {streams.data && <ZoneChart streams={streams.data} />}
      {streams.data && isRun && <PaceZoneChart streams={streams.data} />}

      {activity.laps.length > 1 && (
        <>
          <h2>Laps</h2>
          <div className="card table-wrap" style={{ padding: 0 }}>
            <table>
              <thead>
                <tr>
                  <th>#</th>
                  <th>Distance</th>
                  <th>Time</th>
                  <th>Pace</th>
                  <th>Avg HR</th>
                  <th>Max HR</th>
                  {activity.is_workout && <th>Step</th>}
                </tr>
              </thead>
              <tbody>
                {activity.laps.map((lap) => (
                  <tr
                    key={lap.lap_index}
                    className={lap.intensity === 'active' ? 'lap-active' : ''}
                  >
                    <td>{lap.lap_index + 1}</td>
                    <td>{formatDistance(lap.distance_m)}</td>
                    <td>{formatDuration(lap.elapsed_s)}</td>
                    <td>{formatPace(lap.avg_speed_mps)}</td>
                    <td>{lap.avg_hr ? Math.round(lap.avg_hr) : '–'}</td>
                    <td>{lap.max_hr ? Math.round(lap.max_hr) : '–'}</td>
                    {activity.is_workout && <td>{lap.intensity ?? '–'}</td>}
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
