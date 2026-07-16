import { useEffect, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { fetchJson } from '../api'
import { formatDistance, formatDuration, formatPace, locale, sportEmoji } from '../format'

interface LogbookActivity {
  id: number
  name: string
  sport: string
  day_index: number
  distance_m: number
  moving_s: number
  start_time_local: string
  is_workout: boolean
}

interface LogbookWeek {
  week_start: string
  run_distance_m: number
  total_moving_s: number
  runs: number
  activities: LogbookActivity[]
}

type SizeMetric = 'distance' | 'time'

const PAGE_WEEKS = 16
const DAY_NAMES = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
/* Values at (or above) which a circle reaches full size. */
const SIZE_REF: Record<SizeMetric, number> = { distance: 25000, time: 3 * 3600 }
const MIN_DIAMETER = 10
const MAX_DIAMETER = 68

function circleDiameter(activity: LogbookActivity, metric: SizeMetric): number {
  const value = metric === 'distance' ? activity.distance_m : activity.moving_s
  if (value <= 0) return MIN_DIAMETER
  const frac = Math.min(value / SIZE_REF[metric], 1)
  return MIN_DIAMETER + (MAX_DIAMETER - MIN_DIAMETER) * Math.sqrt(frac)
}

function circleLabel(activity: LogbookActivity, diameter: number): string {
  if (diameter < 26 || activity.distance_m <= 0) return ''
  return (activity.distance_m / 1000).toFixed(1)
}

function isoWeekNumber(date: Date): number {
  // ISO 8601: week 1 contains the first Thursday of the year.
  const thursday = new Date(date)
  thursday.setDate(date.getDate() + 3 - ((date.getDay() + 6) % 7))
  const yearStart = new Date(thursday.getFullYear(), 0, 1)
  return Math.round(((thursday.getTime() - yearStart.getTime()) / 86400000 + 1) / 7)
}

function weekLabel(iso: string): { week: string; date: string } {
  const [y, m, d] = iso.split('-').map(Number)
  const monday = new Date(y, m - 1, d)
  return {
    week: `W${isoWeekNumber(monday)}`,
    date: monday.toLocaleDateString(locale(), { day: 'numeric', month: 'short' })
  }
}

function activityTitle(activity: LogbookActivity): string {
  const parts = [activity.is_workout ? `${activity.name} (workout)` : activity.name]
  if (activity.distance_m > 0) parts.push(formatDistance(activity.distance_m))
  parts.push(formatDuration(activity.moving_s))
  if (activity.sport.includes('running') && activity.moving_s > 0 && activity.distance_m > 0) {
    parts.push(formatPace(activity.distance_m / activity.moving_s))
  }
  return parts.join(' · ')
}

export default function Logbook() {
  const navigate = useNavigate()
  const [weeks, setWeeks] = useState<LogbookWeek[]>([])
  const [metric, setMetric] = useState<SizeMetric>('distance')
  const [error, setError] = useState<string | null>(null)
  const [loading, setLoading] = useState(false)

  const load = (until?: string) => {
    setLoading(true)
    const url = `/api/logbook?weeks=${PAGE_WEEKS}${until ? `&until=${until}` : ''}`
    fetchJson<LogbookWeek[]>(url)
      .then((page) => setWeeks((current) => [...current, ...page]))
      .catch((e: Error) => setError(e.message))
      .finally(() => setLoading(false))
  }

  useEffect(() => {
    load()
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [])

  const loadMore = () => {
    const oldest = weeks[weeks.length - 1]
    if (!oldest) return
    const [y, m, d] = oldest.week_start.split('-').map(Number)
    const prev = new Date(y, m - 1, d - 7)
    const key = `${prev.getFullYear()}-${String(prev.getMonth() + 1).padStart(2, '0')}-${String(prev.getDate()).padStart(2, '0')}`
    load(key)
  }

  return (
    <>
      <h1>Logbook</h1>
      <div className="toolbar">
        <span className="segmented">
          <button className={metric === 'distance' ? 'on' : ''} onClick={() => setMetric('distance')}>
            Size by distance
          </button>
          <button className={metric === 'time' ? 'on' : ''} onClick={() => setMetric('time')}>
            Size by time
          </button>
        </span>
        <span className="legend">
          <span className="legend-dot run" /> Run
          <span className="legend-dot workout" /> Workout / intervals
          <span className="legend-dot" /> Other
        </span>
      </div>
      {error && <div className="error-box">{error}</div>}

      <div className="logbook">
        <div className="logbook-row logbook-head">
          <div className="week-label" />
          {DAY_NAMES.map((day) => (
            <div key={day} className="day-head">
              {day}
            </div>
          ))}
          <div className="week-totals" />
        </div>

        {weeks.map((week) => (
          <div className="logbook-row" key={week.week_start}>
            <div className="week-label">
              <strong>{weekLabel(week.week_start).week}</strong>
              <span>{weekLabel(week.week_start).date}</span>
            </div>
            {DAY_NAMES.map((_, dayIndex) => {
              const dayActivities = week.activities.filter((a) => a.day_index === dayIndex)
              return (
                <div key={dayIndex} className="day-cell">
                  {dayActivities.map((activity) => {
                    const diameter = circleDiameter(activity, metric)
                    const isRun = activity.sport.includes('running')
                    const variant = activity.is_workout ? ' workout' : isRun ? ' run' : ''
                    return (
                      <button
                        key={activity.id}
                        className={`activity-circle${variant}`}
                        style={{ width: diameter, height: diameter }}
                        title={activityTitle(activity)}
                        onClick={() => navigate(`/activities/${activity.id}`)}
                      >
                        {isRun || activity.is_workout
                          ? circleLabel(activity, diameter)
                          : sportEmoji(activity.sport)}
                      </button>
                    )
                  })}
                </div>
              )
            })}
            <div className="week-totals">
              <strong>{(week.run_distance_m / 1000).toFixed(1)} km</strong>
              <div className="muted">
                {formatDuration(week.total_moving_s)}
                {week.runs > 0 && ` · ${week.runs} runs`}
              </div>
            </div>
          </div>
        ))}
      </div>

      <div style={{ textAlign: 'center', marginTop: 20 }}>
        <button className="ghost" onClick={loadMore} disabled={loading}>
          {loading ? 'Loading…' : 'Earlier weeks'}
        </button>
      </div>
    </>
  )
}
