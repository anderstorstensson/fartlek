import { useState } from 'react'
import { Link } from 'react-router-dom'
import {
  CoachStatus,
  EfficiencyPoint,
  FitnessPoint,
  LoadModel,
  useApi,
  WeeklyStat,
  WeeklyZones,
  WellnessDay
} from '../api'
import { coachUrl, TREND_PROMPT } from '../coachLink'
import EfficiencyChart from '../components/EfficiencyChart'
import FitnessChart from '../components/FitnessChart'
import Vo2maxChart from '../components/Vo2maxChart'
import WeeklyChart, { WeeklyMetric } from '../components/WeeklyChart'
import ZoneDistributionChart from '../components/ZoneDistributionChart'

const RANGES = [
  { label: '3 m', days: 90 },
  { label: '6 m', days: 180 },
  { label: '1 y', days: 365 },
  { label: '2 y', days: 730 }
]

const WEEK_RANGES = [
  { label: '12 w', weeks: 12 },
  { label: '26 w', weeks: 26 },
  { label: '52 w', weeks: 52 },
  { label: '2 y', weeks: 104 }
]

export default function Trends() {
  const [model, setModel] = useState<LoadModel>('trimp')
  const [days, setDays] = useState(180)
  const [metric, setMetric] = useState<WeeklyMetric>('distance')
  const [weeks, setWeeks] = useState(26)

  const [zoneWeeks, setZoneWeeks] = useState(26)
  const [efficiencyDays, setEfficiencyDays] = useState(365)
  const [longRunsOnly, setLongRunsOnly] = useState(false)
  const [vo2maxDays, setVo2maxDays] = useState(365)

  const coachStatus = useApi<CoachStatus>('/api/coach/status')
  const coachReady =
    coachStatus.data?.enabled === true && coachStatus.data?.cli_available === true

  const fitness = useApi<FitnessPoint[]>(`/api/trends/fitness?model=${model}&days=${days}`)
  const weekly = useApi<WeeklyStat[]>(`/api/trends/weekly?weeks=${weeks}`)
  const zones = useApi<WeeklyZones[]>(`/api/trends/zones?weeks=${zoneWeeks}`)
  const efficiency = useApi<EfficiencyPoint[]>(`/api/trends/efficiency?days=${efficiencyDays}`)
  const wellness = useApi<WellnessDay[]>(`/api/wellness?days=${vo2maxDays}`)
  const efficiencyPoints = (efficiency.data ?? []).filter(
    (p) => !longRunsOnly || p.moving_s >= 4500
  )

  return (
    <>
      <div style={{ display: 'flex', alignItems: 'baseline', gap: 12 }}>
        <h1>Trends</h1>
        {coachReady && (
          <Link to={coachUrl(TREND_PROMPT)} className="btn-ghost" style={{ marginLeft: 'auto' }}>
            🎓 Review trends with the coach
          </Link>
        )}
      </div>

      <div className="chart-card">
        <div className="chart-title">
          <span>Fitness &amp; freshness</span>
          <span style={{ display: 'flex', gap: 10 }}>
            <span className="segmented">
              <button className={model === 'trimp' ? 'on' : ''} onClick={() => setModel('trimp')}>
                TRIMP (HR)
              </button>
              <button className={model === 'rtss' ? 'on' : ''} onClick={() => setModel('rtss')}>
                rTSS (pace)
              </button>
            </span>
            <span className="segmented">
              {RANGES.map((range) => (
                <button
                  key={range.days}
                  className={days === range.days ? 'on' : ''}
                  onClick={() => setDays(range.days)}
                >
                  {range.label}
                </button>
              ))}
            </span>
          </span>
        </div>
        {fitness.error && <div className="error-box">{fitness.error}</div>}
        {fitness.data && <FitnessChart data={fitness.data} />}
        <p className="muted" style={{ fontSize: 12, padding: '4px 8px' }}>
          Fitness (CTL) is a 42-day weighted average of daily load; Fatigue (ATL) a 7-day
          average; Form (TSB) is fitness minus fatigue — positive means fresh, below −20 means
          high strain.{' '}
          {model === 'rtss'
            ? 'Pace model: rTSS for runs, HR-based TSS for other sports.'
            : 'HR model: Banister TRIMP for all activities with heart rate.'}
        </p>
      </div>

      <div className="chart-card">
        <div className="chart-title">
          <span>Weekly volume</span>
          <span style={{ display: 'flex', gap: 10 }}>
            <span className="segmented">
              <button
                className={metric === 'distance' ? 'on' : ''}
                onClick={() => setMetric('distance')}
              >
                Distance
              </button>
              <button className={metric === 'time' ? 'on' : ''} onClick={() => setMetric('time')}>
                Time
              </button>
              <button className={metric === 'load' ? 'on' : ''} onClick={() => setMetric('load')}>
                Load
              </button>
            </span>
            <span className="segmented">
              {WEEK_RANGES.map((range) => (
                <button
                  key={range.weeks}
                  className={weeks === range.weeks ? 'on' : ''}
                  onClick={() => setWeeks(range.weeks)}
                >
                  {range.label}
                </button>
              ))}
            </span>
          </span>
        </div>
        {weekly.error && <div className="error-box">{weekly.error}</div>}
        {weekly.data && <WeeklyChart data={weekly.data} metric={metric} />}
      </div>

      <div className="chart-card">
        <div className="chart-title">
          <span>Intensity distribution (time in HR zones)</span>
          <span className="segmented">
            {WEEK_RANGES.map((range) => (
              <button
                key={range.weeks}
                className={zoneWeeks === range.weeks ? 'on' : ''}
                onClick={() => setZoneWeeks(range.weeks)}
              >
                {range.label}
              </button>
            ))}
          </span>
        </div>
        {zones.error && <div className="error-box">{zones.error}</div>}
        {zones.data && <ZoneDistributionChart data={zones.data} />}
      </div>

      <div className="chart-card">
        <div className="chart-title">
          <span>Efficiency &amp; decoupling (runs)</span>
          <span style={{ display: 'flex', gap: 10 }}>
            <span className="segmented">
              <button
                className={longRunsOnly ? 'on' : ''}
                onClick={() => setLongRunsOnly(!longRunsOnly)}
              >
                Runs ≥ 75 min
              </button>
            </span>
            <span className="segmented">
              {RANGES.map((range) => (
                <button
                  key={range.days}
                  className={efficiencyDays === range.days ? 'on' : ''}
                  onClick={() => setEfficiencyDays(range.days)}
                >
                  {range.label}
                </button>
              ))}
            </span>
          </span>
        </div>
        {efficiency.error && <div className="error-box">{efficiency.error}</div>}
        {efficiency.data && <EfficiencyChart data={efficiencyPoints} />}
        <p className="muted" style={{ fontSize: 12, padding: '4px 8px' }}>
          Efficiency is grade-adjusted meters per minute per heartbeat — higher at the same
          effort means growing aerobic fitness. Decoupling compares the first and second half
          speed:HR of each run; staying under ~5% (dashed line) on long runs signals durability.
        </p>
      </div>

      <div className="chart-card">
        <div className="chart-title">
          <span>VO₂max (Garmin estimate)</span>
          <span className="segmented">
            {RANGES.map((range) => (
              <button
                key={range.days}
                className={vo2maxDays === range.days ? 'on' : ''}
                onClick={() => setVo2maxDays(range.days)}
              >
                {range.label}
              </button>
            ))}
          </span>
        </div>
        {wellness.error && <div className="error-box">{wellness.error}</div>}
        {wellness.data && <Vo2maxChart data={wellness.data} />}
        <p className="muted" style={{ fontSize: 12, padding: '4px 8px' }}>
          Garmin&apos;s daily running VO₂max estimate. The absolute number is model output —
          read the direction over weeks, not single-day wiggles.
        </p>
      </div>
    </>
  )
}
