import { Link, useParams } from 'react-router-dom'
import { ActivityDetail, Streams, useApi } from '../api'
import ActivityMap from '../components/ActivityMap'
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

function Stat({ label, value }: { label: string; value: string }) {
  return (
    <div className="stat-tile card">
      <div className="label">{label}</div>
      <div className="value" style={{ fontSize: 20 }}>
        {value}
      </div>
    </div>
  )
}

export default function ActivityDetailPage() {
  const { id } = useParams()
  const detail = useApi<ActivityDetail>(id ? `/api/activities/${id}` : null)
  const streams = useApi<Streams>(id ? `/api/activities/${id}/streams` : null)

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
        {activity.is_workout && <span className="badge workout">workout</span>}
      </h1>
      <p className="muted" style={{ marginTop: 0 }}>
        {formatSportName(activity.sport)} · {formatDate(activity.start_time_local)} at{' '}
        {formatTime(activity.start_time_local)}
      </p>

      <div className="stat-grid" style={{ marginBottom: 20 }}>
        {activity.distance_m > 0 && <Stat label="Distance" value={formatDistance(activity.distance_m)} />}
        <Stat label="Moving time" value={formatDuration(activity.moving_s)} />
        {isRun && <Stat label="Avg pace" value={formatPace(activity.avg_speed_mps)} />}
        {activity.avg_hr !== null && (
          <Stat
            label="Heart rate"
            value={`${Math.round(activity.avg_hr)} / ${activity.max_hr ? Math.round(activity.max_hr) : '–'} bpm`}
          />
        )}
        {activity.ascent_m !== null && activity.ascent_m > 0 && (
          <Stat label="Ascent" value={`${Math.round(activity.ascent_m)} m`} />
        )}
        {activity.calories !== null && <Stat label="Calories" value={`${Math.round(activity.calories)}`} />}
        {activity.trimp !== null && <Stat label="TRIMP" value={activity.trimp.toFixed(0)} />}
        {activity.rtss !== null && <Stat label="rTSS" value={activity.rtss.toFixed(0)} />}
      </div>

      {activity.best_efforts.length > 0 && (
        <p>
          {activity.best_efforts.map((effort) => (
            <span className="badge" key={effort.label} style={{ marginRight: 8 }}>
              {effort.label}: {formatDuration(effort.duration_s)}
            </span>
          ))}
        </p>
      )}

      {streams.data && <ActivityMap streams={streams.data} />}
      {streams.data && <StreamCharts streams={streams.data} />}
      {streams.data && <ZoneChart streams={streams.data} />}

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
