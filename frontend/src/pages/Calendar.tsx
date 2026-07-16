import { useEffect, useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import ReactMarkdown from 'react-markdown'
import { CoachStatus, fetchJson, PlanInfo, PlannedWorkout, useApi } from '../api'
import { coachUrl, PLAN_PROMPT } from '../coachLink'
import { formatDistance, formatDuration, sportEmoji } from '../format'

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

const TYPE_ICONS: Record<string, string> = {
  cross: '🏋️',
  race: '🏁',
  rest: '😴'
}

function WorkoutModal({
  workout,
  onClose,
  onOpenActivity
}: {
  workout: PlannedWorkout
  onClose: () => void
  onOpenActivity: (id: number) => void
}) {
  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal card" onClick={(e) => e.stopPropagation()}>
        <div className="note-head">
          <div>
            <span className="badge">{workout.workout_type}</span>
            <strong style={{ marginLeft: 10 }}>{workout.title}</strong>
          </div>
          <button className="ghost" onClick={onClose}>
            Close
          </button>
        </div>
        <p className="muted" style={{ margin: '4px 0 10px', fontSize: 13 }}>
          {workout.day}
          {workout.plan_name && ` · ${workout.plan_name}`}
        </p>
        <div className="stat-grid" style={{ marginBottom: 12 }}>
          {workout.target_distance_m !== null && workout.target_distance_m > 0 && (
            <div className="stat-tile">
              <div className="label">Target distance</div>
              <div className="value" style={{ fontSize: 18 }}>
                {formatDistance(workout.target_distance_m)}
              </div>
            </div>
          )}
          {workout.target_duration_s !== null && workout.target_duration_s > 0 && (
            <div className="stat-tile">
              <div className="label">Target duration</div>
              <div className="value" style={{ fontSize: 18 }}>
                {formatDuration(workout.target_duration_s)}
              </div>
            </div>
          )}
        </div>
        {workout.description && (
          <div className="markdown">
            <ReactMarkdown>{workout.description}</ReactMarkdown>
          </div>
        )}
        {workout.completed_activity_id && (
          <button
            style={{ marginTop: 12 }}
            onClick={() => onOpenActivity(workout.completed_activity_id!)}
          >
            ✓ View completed activity
          </button>
        )}
      </div>
    </div>
  )
}

export default function Calendar() {
  const navigate = useNavigate()
  const today = new Date()
  const [year, setYear] = useState(today.getFullYear())
  const [month, setMonth] = useState(today.getMonth())
  const [planned, setPlanned] = useState<Record<string, PlannedWorkout[]>>({})
  const [activities, setActivities] = useState<Record<string, DayActivity[]>>({})
  const [plans, setPlans] = useState<PlanInfo[]>([])
  const coachStatus = useApi<CoachStatus>('/api/coach/status')
  const coachReady =
    coachStatus.data?.enabled === true && coachStatus.data?.cli_available === true
  const [error, setError] = useState<string | null>(null)
  const [selected, setSelected] = useState<PlannedWorkout | null>(null)

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
        {coachReady && (
          <Link to={coachUrl(PLAN_PROMPT)} className="btn-ghost" style={{ marginLeft: 'auto' }}>
            🎓 Plan with the coach
          </Link>
        )}
      </div>
      {error && <div className="error-box">{error}</div>}

      <div className="calendar">
        <div className="calendar-row calendar-head">
          {DAY_NAMES.map((name) => (
            <div key={name} className="day-head">
              {name}
            </div>
          ))}
          <div className="day-head">Week</div>
        </div>
        {weeks.map((week) => {
          const weekKeys = week.map(isoDate)
          const plannedKm =
            weekKeys.flatMap((k) => planned[k] ?? []).reduce(
              (sum, w) => sum + (w.target_distance_m ?? 0), 0) / 1000
          const doneKm =
            weekKeys.flatMap((k) => activities[k] ?? []).reduce(
              (sum, a) => sum + a.distance_m, 0) / 1000
          return (
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
                      onClick={() => setSelected(workout)}
                    >
                      {workout.completed_activity_id ? '✓ ' : ''}
                      {TYPE_ICONS[workout.workout_type] ? `${TYPE_ICONS[workout.workout_type]} ` : ''}
                      {workout.title}
                    </button>
                  ))}
                </div>
              )
            })}
            <div className="calendar-cell week-summary">
              {plannedKm > 0 && (
                <div>
                  <span className="muted">plan</span> {plannedKm.toFixed(0)} km
                </div>
              )}
              {doneKm > 0 && (
                <div>
                  <span className="muted">done</span> {doneKm.toFixed(1)} km
                </div>
              )}
            </div>
          </div>
          )
        })}
      </div>

      {selected && (
        <WorkoutModal
          workout={selected}
          onClose={() => setSelected(null)}
          onOpenActivity={(id) => navigate(`/activities/${id}`)}
        />
      )}

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
                    <td style={{ textAlign: 'right', whiteSpace: 'nowrap' }}>
                      <a
                        className="btn-ghost"
                        href={`/api/plan/export.ics?plan_name=${encodeURIComponent(plan.plan_name)}`}
                        download
                      >
                        Export .ics
                      </a>
                      <button
                        className="ghost"
                        style={{ marginLeft: 8 }}
                        onClick={() => deletePlan(plan.plan_name)}
                      >
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
