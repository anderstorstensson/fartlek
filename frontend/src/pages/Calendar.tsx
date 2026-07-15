import { useEffect, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { fetchJson } from '../api'
import { formatDistance, formatDuration, sportEmoji } from '../format'

interface PlannedWorkout {
  id: number
  day: string
  title: string
  workout_type: string
  description: string
  target_distance_m: number | null
  target_duration_s: number | null
  plan_name: string
  completed_activity_id: number | null
}

interface PlanInfo {
  plan_name: string
  workouts: number
  first_day: string
  last_day: string
}

interface DayActivity {
  id: number
  name: string
  sport: string
  day_index: number
  distance_m: number
  moving_s: number
  is_workout: boolean
}

interface LogbookWeek {
  week_start: string
  activities: DayActivity[]
}

const DAY_NAMES = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']

function isoDate(d: Date): string {
  return `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, '0')}-${String(d.getDate()).padStart(2, '0')}`
}

function mondayOf(d: Date): Date {
  const monday = new Date(d)
  monday.setDate(d.getDate() - ((d.getDay() + 6) % 7))
  return monday
}

function buildGrid(year: number, month: number): Date[][] {
  const gridStart = mondayOf(new Date(year, month, 1))
  const monthEnd = new Date(year, month + 1, 0)
  const weeks: Date[][] = []
  const cursor = new Date(gridStart)
  while (cursor <= monthEnd || weeks.length === 0) {
    const week: Date[] = []
    for (let i = 0; i < 7; i++) {
      week.push(new Date(cursor))
      cursor.setDate(cursor.getDate() + 1)
    }
    weeks.push(week)
  }
  return weeks
}

function plannedTitle(w: PlannedWorkout): string {
  const parts = [w.title]
  if (w.target_distance_m) parts.push(formatDistance(w.target_distance_m))
  if (w.target_duration_s) parts.push(formatDuration(w.target_duration_s))
  if (w.description) parts.push(w.description)
  if (w.plan_name) parts.push(`[${w.plan_name}]`)
  return parts.join(' · ')
}

export default function Calendar() {
  const navigate = useNavigate()
  const today = new Date()
  const [year, setYear] = useState(today.getFullYear())
  const [month, setMonth] = useState(today.getMonth())
  const [planned, setPlanned] = useState<Record<string, PlannedWorkout[]>>({})
  const [activities, setActivities] = useState<Record<string, DayActivity[]>>({})
  const [plans, setPlans] = useState<PlanInfo[]>([])
  const [error, setError] = useState<string | null>(null)

  const weeks = buildGrid(year, month)
  const gridStart = isoDate(weeks[0][0])
  const gridEnd = isoDate(weeks[weeks.length - 1][6])

  useEffect(() => {
    let cancelled = false
    fetchJson<PlannedWorkout[]>(`/api/plan?start=${gridStart}&end=${gridEnd}`)
      .then((items) => {
        if (cancelled) return
        const byDay: Record<string, PlannedWorkout[]> = {}
        for (const item of items) {
          byDay[item.day] = [...(byDay[item.day] ?? []), item]
        }
        setPlanned(byDay)
      })
      .catch((e: Error) => setError(e.message))

    fetchJson<LogbookWeek[]>(`/api/logbook?weeks=${weeks.length}&until=${isoDate(weeks[weeks.length - 1][0])}`)
      .then((rows) => {
        if (cancelled) return
        const byDay: Record<string, DayActivity[]> = {}
        for (const week of rows) {
          const [y, m, d] = week.week_start.split('-').map(Number)
          for (const activity of week.activities) {
            const day = new Date(y, m - 1, d + activity.day_index)
            const key = isoDate(day)
            byDay[key] = [...(byDay[key] ?? []), activity]
          }
        }
        setActivities(byDay)
      })
      .catch((e: Error) => setError(e.message))

    fetchJson<PlanInfo[]>('/api/plan/plans')
      .then((items) => {
        if (!cancelled) setPlans(items)
      })
      .catch(() => undefined)

    return () => {
      cancelled = true
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [gridStart, gridEnd])

  const deletePlan = (name: string) => {
    if (!window.confirm(`Delete plan "${name}" and all its workouts?`)) return
    fetchJson(`/api/plan?plan_name=${encodeURIComponent(name)}`, { method: 'DELETE' })
      .then(() => {
        setPlans((current) => current.filter((p) => p.plan_name !== name))
        setPlanned((current) => {
          const next: Record<string, PlannedWorkout[]> = {}
          for (const [day, items] of Object.entries(current)) {
            const kept = items.filter((w) => w.plan_name !== name)
            if (kept.length > 0) next[day] = kept
          }
          return next
        })
      })
      .catch((e: Error) => setError(e.message))
  }

  const monthLabel = new Date(year, month, 1).toLocaleDateString(undefined, {
    month: 'long',
    year: 'numeric'
  })
  const todayKey = isoDate(today)

  const shiftMonth = (delta: number) => {
    const next = new Date(year, month + delta, 1)
    setYear(next.getFullYear())
    setMonth(next.getMonth())
  }

  return (
    <>
      <h1>Calendar</h1>
      <div className="toolbar">
        <button className="ghost" onClick={() => shiftMonth(-1)}>
          ‹
        </button>
        <strong style={{ minWidth: 150, textAlign: 'center' }}>{monthLabel}</strong>
        <button className="ghost" onClick={() => shiftMonth(1)}>
          ›
        </button>
        <button
          className="ghost"
          onClick={() => {
            setYear(today.getFullYear())
            setMonth(today.getMonth())
          }}
        >
          Today
        </button>
        <span className="legend">
          <span className="legend-dot run" /> Done
          <span className="legend-dot planned" /> Planned
        </span>
      </div>
      {error && <div className="error-box">{error}</div>}

      <div className="calendar">
        <div className="calendar-row calendar-head">
          {DAY_NAMES.map((name) => (
            <div key={name} className="day-head">
              {name}
            </div>
          ))}
        </div>
        {weeks.map((week) => (
          <div className="calendar-row" key={isoDate(week[0])}>
            {week.map((day) => {
              const key = isoDate(day)
              const inMonth = day.getMonth() === month
              return (
                <div
                  key={key}
                  className={`calendar-cell${inMonth ? '' : ' outside'}${key === todayKey ? ' today' : ''}`}
                >
                  <div className="date-num">{day.getDate()}</div>
                  {(activities[key] ?? []).map((activity) => (
                    <button
                      key={activity.id}
                      className={`cal-chip done${activity.is_workout ? ' workout' : ''}`}
                      title={activity.name}
                      onClick={() => navigate(`/activities/${activity.id}`)}
                    >
                      {activity.sport.includes('running')
                        ? `${(activity.distance_m / 1000).toFixed(1)} km`
                        : sportEmoji(activity.sport)}
                    </button>
                  ))}
                  {(planned[key] ?? []).map((workout) => (
                    <button
                      key={workout.id}
                      className={`cal-chip planned${workout.completed_activity_id ? ' completed' : ''}`}
                      title={plannedTitle(workout)}
                      onClick={() =>
                        workout.completed_activity_id &&
                        navigate(`/activities/${workout.completed_activity_id}`)
                      }
                    >
                      {workout.completed_activity_id ? '✓ ' : ''}
                      {workout.title}
                    </button>
                  ))}
                </div>
              )
            })}
          </div>
        ))}
      </div>

      {plans.length > 0 && (
        <>
          <h2>Training plans</h2>
          <div className="card table-wrap" style={{ padding: 0 }}>
            <table>
              <tbody>
                {plans.map((plan) => (
                  <tr key={plan.plan_name}>
                    <td className="strong">{plan.plan_name}</td>
                    <td>{plan.workouts} workouts</td>
                    <td className="muted">
                      {plan.first_day} → {plan.last_day}
                    </td>
                    <td style={{ textAlign: 'right' }}>
                      <button className="ghost" onClick={() => deletePlan(plan.plan_name)}>
                        Delete
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </>
      )}
      {plans.length === 0 && (
        <p className="muted">
          No training plan yet — ask Claude Code in this project to create one; it will show up
          here.
        </p>
      )}
    </>
  )
}
