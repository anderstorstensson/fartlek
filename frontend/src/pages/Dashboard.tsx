import { useState } from 'react'
import { Link } from 'react-router-dom'
import {
  ActivityList,
  FitnessPoint,
  PlannedWorkout,
  Race,
  Readiness,
  StatsSummary,
  useApi,
  WeeklyStat
} from '../api'
import FitnessChart from '../components/FitnessChart'
import StatCard from '../components/StatCard'
import WeeklyChart, { WeeklyMetric } from '../components/WeeklyChart'
import {
  formatDate,
  formatDistance,
  formatDuration,
  formatPace,
  formatSportName,
  sportEmoji
} from '../format'

const KEY_TYPES = ['intervals', 'tempo', 'long', 'race']

function isoToday(offsetDays = 0): string {
  const d = new Date()
  d.setDate(d.getDate() + offsetDays)
  return `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, '0')}-${String(d.getDate()).padStart(2, '0')}`
}

const READINESS_LABEL: Record<Readiness['status'], string> = {
  ready: '🟢 Ready',
  caution: '🟡 Caution',
  rest: '🔴 Take it easy'
}

const FLAG_LABEL: Record<string, string> = {
  'hrv-low': 'HRV below baseline',
  'rhr-elevated': 'resting HR elevated',
  'sleep-poor': 'poor sleep'
}

function ReadinessTile({ readiness }: { readiness: Readiness }) {
  const detail = [
    readiness.hrv_last_night_avg !== null
      ? `HRV ${Math.round(readiness.hrv_last_night_avg)}${
          readiness.hrv_baseline !== null ? `/${Math.round(readiness.hrv_baseline)}` : ''
        } ms`
      : null,
    readiness.resting_hr !== null ? `RHR ${readiness.resting_hr}` : null,
    readiness.sleep_score !== null ? `sleep ${readiness.sleep_score}` : null
  ]
    .filter(Boolean)
    .join(' · ')
  return (
    <div className="card stat-tile">
      <div className="label">Readiness · {formatDate(readiness.day)}</div>
      <div className="value" style={{ fontSize: 17 }}>
        {READINESS_LABEL[readiness.status]}
      </div>
      <div className="delta">
        {readiness.flags.length > 0
          ? readiness.flags.map((f) => FLAG_LABEL[f] ?? f).join(', ')
          : detail}
      </div>
    </div>
  )
}

function RaceTile({ race }: { race: Race }) {
  return (
    <div className="card stat-tile">
      <div className="label">
        {race.name} · {formatDate(race.day)}
      </div>
      <div className="value" style={{ fontSize: 17 }}>
        {race.days_until !== null && race.days_until >= 0 ? `${race.days_until} days to go` : '–'}
      </div>
      <div className="delta">
        {formatDistance(race.distance_m)}
        {race.target_time_s ? ` · target ${formatDuration(race.target_time_s)}` : ''}
        {race.predicted_time_s ? ` · predicted ${formatDuration(race.predicted_time_s)}` : ''}
      </div>
    </div>
  )
}

function NextWorkoutTile({ workout }: { workout: PlannedWorkout }) {
  const [y, m, d] = workout.day.split('-').map(Number)
  const dayLabel = new Date(y, m - 1, d).toLocaleDateString(undefined, {
    weekday: 'short',
    day: 'numeric',
    month: 'short'
  })
  return (
    <Link to="/calendar" className="card stat-tile next-workout">
      <div className="label">Next key workout · {dayLabel}</div>
      <div className="value" style={{ fontSize: 17, lineHeight: 1.3 }}>
        {workout.title}
      </div>
      <div className="delta">
        {workout.workout_type}
        {workout.target_distance_m ? ` · ${formatDistance(workout.target_distance_m)}` : ''}
      </div>
    </Link>
  )
}

export default function Dashboard() {
  const stats = useApi<StatsSummary>('/api/stats/summary')
  const weekly = useApi<WeeklyStat[]>('/api/trends/weekly?weeks=26')
  const recent = useApi<ActivityList>('/api/activities?limit=6')
  const [weeklyMetric, setWeeklyMetric] = useState<WeeklyMetric>('distance')
  const plan = useApi<PlannedWorkout[]>(`/api/plan?start=${isoToday()}&end=${isoToday(28)}`)
  const nextKey = plan.data?.find(
    (w) => KEY_TYPES.includes(w.workout_type) && !w.completed_activity_id
  )
  const readiness = useApi<Readiness | null>('/api/wellness/readiness')
  const races = useApi<Race[]>('/api/races?upcoming=true')
  const nextRace = races.data?.[0]
  // Project the fitness curve through the next race (or 4 weeks of plan);
  // wait for the races call so the chart doesn't fetch twice.
  const projectDays = Math.min(Math.max(nextRace?.days_until ?? 28, 14), 120)
  const fitness = useApi<FitnessPoint[]>(
    races.loading
      ? null
      : `/api/trends/fitness?model=trimp&days=120&project_days=${projectDays}`
  )

  if (stats.error) return <div className="error-box">Failed to load stats: {stats.error}</div>

  const summary = stats.data
  const week = summary?.this_week
  const last = summary?.last_week
  const form = summary?.form_trimp

  return (
    <>
      <h1>Dashboard</h1>
      {summary && summary.total_activities === 0 && (
        <div className="card">
          <p>No activities yet. To get started:</p>
          <ol className="muted">
            <li>
              Log in to Garmin from a terminal: <code>make login</code>
            </li>
            <li>
              Backfill your history: <code>make backfill</code> (or use Settings → Sync)
            </li>
          </ol>
        </div>
      )}
      {week && last && (
        <div className="stat-grid">
          <StatCard
            label="Run distance · this week"
            value={formatDistance(week.run_distance_m)}
            delta={`last week ${formatDistance(last.run_distance_m)}`}
            deltaGood={week.run_distance_m >= last.run_distance_m}
          />
          <StatCard
            label="Time · this week"
            value={formatDuration(week.total_moving_s)}
            delta={`last week ${formatDuration(last.total_moving_s)}`}
          />
          <StatCard
            label="Load (TRIMP) · this week"
            value={week.load_trimp.toFixed(0)}
            delta={`last week ${last.load_trimp.toFixed(0)}`}
          />
          {nextKey ? (
            <NextWorkoutTile workout={nextKey} />
          ) : (
            form && (
              <StatCard
                label="Form (TSB) · today"
                value={form.tsb.toFixed(0)}
                delta={`fitness ${form.ctl.toFixed(0)} · fatigue ${form.atl.toFixed(0)}`}
                deltaGood={form.tsb >= 0}
              />
            )
          )}
          {readiness.data && <ReadinessTile readiness={readiness.data} />}
          {nextRace && <RaceTile race={nextRace} />}
        </div>
      )}

      <h2>Fitness · last 120 days (TRIMP model{nextRace ? ', projected to race day' : ''})</h2>
      <div className="chart-card">
        {fitness.data && (
          <FitnessChart data={fitness.data} height={260} raceDay={nextRace?.day ?? null} />
        )}
      </div>

      <div className="chart-card" style={{ marginTop: 28 }}>
        <div className="chart-title">
          <span>
            {weeklyMetric === 'distance' && 'Weekly mileage'}
            {weeklyMetric === 'time' && 'Weekly time'}
            {weeklyMetric === 'load' && 'Weekly training load (TRIMP)'}
            {' · last 26 weeks'}
          </span>
          <span className="segmented">
            <button
              className={weeklyMetric === 'distance' ? 'on' : ''}
              onClick={() => setWeeklyMetric('distance')}
            >
              Distance
            </button>
            <button
              className={weeklyMetric === 'time' ? 'on' : ''}
              onClick={() => setWeeklyMetric('time')}
            >
              Time
            </button>
            <button
              className={weeklyMetric === 'load' ? 'on' : ''}
              onClick={() => setWeeklyMetric('load')}
            >
              Load
            </button>
          </span>
        </div>
        {weekly.data && <WeeklyChart data={weekly.data} metric={weeklyMetric} height={200} />}
      </div>

      <h2>Recent activities</h2>
      <div className="card table-wrap" style={{ padding: 0 }}>
        <table>
          <thead>
            <tr>
              <th>Date</th>
              <th>Activity</th>
              <th>Distance</th>
              <th>Time</th>
              <th>Pace</th>
              <th>HR</th>
            </tr>
          </thead>
          <tbody>
            {recent.data?.items.map((activity) => (
              <tr key={activity.id}>
                <td>{formatDate(activity.start_time_local)}</td>
                <td className="strong">
                  <Link to={`/activities/${activity.id}`}>
                    {sportEmoji(activity.sport)} {activity.name}
                  </Link>
                  {activity.is_workout && <span className="badge workout">workout</span>}
                  <span className="muted"> · {formatSportName(activity.sport)}</span>
                </td>
                <td>{activity.distance_m > 0 ? formatDistance(activity.distance_m) : '–'}</td>
                <td>{formatDuration(activity.moving_s)}</td>
                <td>{activity.sport.includes('running') ? formatPace(activity.avg_speed_mps) : '–'}</td>
                <td>{activity.avg_hr ? Math.round(activity.avg_hr) : '–'}</td>
              </tr>
            ))}
          </tbody>
        </table>
        {recent.data && recent.data.items.length === 0 && (
          <div className="empty-state">Nothing here yet</div>
        )}
      </div>
    </>
  )
}
