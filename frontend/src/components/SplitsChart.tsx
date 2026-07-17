import { CSSProperties, MouseEvent, useEffect, useLayoutEffect, useRef, useState } from 'react'
import { Split, SplitsResponse, useApi } from '../api'
import { formatDistance, formatDuration, formatPace } from '../format'

const ACTIVE_COLOR = 'var(--accent)'
const EASY_COLOR = '#5a5a56' // warmup/cooldown/rest and non-workout bars

const CHART_HEIGHT = 150
const LABEL_ABOVE_MIN_PX = 34 // horizontal pace label above the bar
const LABEL_INSIDE_MIN_PX = 13 // vertical pace label inside the bar
const LABEL_INSIDE_MIN_HEIGHT = 48

/* Same look as the recharts tooltips in StreamCharts. */
const POPUP_STYLE: CSSProperties = {
  position: 'absolute',
  top: 0,
  zIndex: 5,
  backgroundColor: '#232322',
  border: '1px solid rgba(255,255,255,0.1)',
  borderRadius: 8,
  color: '#ffffff',
  fontSize: 13,
  padding: '8px 12px',
  whiteSpace: 'nowrap',
  boxShadow: '0 4px 16px rgba(0, 0, 0, 0.4)'
}

function barColor(intensity: string | null): string {
  // Manual-lap workouts often mark every lap "interval"; only explicit
  // warmup/rest/cooldown render muted then.
  if (intensity === null || intensity === 'active' || intensity === 'interval')
    return ACTIVE_COLOR
  return EASY_COLOR
}

function splitName(split: Split): string {
  return split.intensity && !['active', 'interval'].includes(split.intensity)
    ? split.intensity
    : `#${split.index + 1}`
}

function splitTitle(split: Split, label: string): string {
  const parts = [
    label,
    formatDistance(split.distance_m),
    formatDuration(split.elapsed_s),
    formatPace(split.avg_speed_mps)
  ]
  if (split.avg_hr !== null) parts.push(`${Math.round(split.avg_hr)} bpm`)
  if (split.elevation_gain_m !== null) parts.push(`+${Math.round(split.elevation_gain_m)} m`)
  return parts.join(' · ')
}

function PopupRow({ name, value }: { name: string; value: string }) {
  return (
    <div style={{ display: 'flex', justifyContent: 'space-between', gap: 16 }}>
      <span style={{ color: 'var(--text-muted)' }}>{name}</span>
      <span style={{ fontVariantNumeric: 'tabular-nums' }}>{value}</span>
    </div>
  )
}

function SplitPopup({ split, x, width }: { split: Split; x: number; width: number }) {
  // Keep the box inside the chart; on very narrow screens just center it.
  const left = width > 220 ? Math.min(Math.max(x, 100), width - 100) : width / 2
  return (
    <div style={{ ...POPUP_STYLE, left, transform: 'translateX(-50%)' }}>
      <div style={{ color: 'var(--text-secondary)', fontWeight: 600, marginBottom: 4 }}>
        {splitName(split)}
      </div>
      <PopupRow name="Pace" value={formatPace(split.avg_speed_mps)} />
      {split.avg_hr !== null && (
        <PopupRow name="Heart rate" value={`${Math.round(split.avg_hr)} bpm`} />
      )}
      <PopupRow name="Time" value={formatDuration(split.elapsed_s)} />
      <PopupRow name="Distance" value={formatDistance(split.distance_m)} />
      {split.elevation_gain_m !== null && (
        <PopupRow name="Climb" value={`+${Math.round(split.elevation_gain_m)} m`} />
      )}
    </div>
  )
}

/** Column timeline for interval sessions: width ∝ lap duration, height ∝ speed
 * (so walking rest reads as a sliver instead of wrecking a pace axis). Click a
 * column for the detail popup. */
function WorkoutColumns({ splits }: { splits: Split[] }) {
  const wrapRef = useRef<HTMLDivElement>(null)
  const [width, setWidth] = useState(0)
  const [popup, setPopup] = useState<{ index: number; x: number } | null>(null)

  useLayoutEffect(() => {
    const measure = () => setWidth(wrapRef.current?.clientWidth ?? 0)
    measure()
    window.addEventListener('resize', measure)
    return () => window.removeEventListener('resize', measure)
  }, [])

  useEffect(() => {
    if (!popup) return
    const onKey = (event: KeyboardEvent) => event.key === 'Escape' && setPopup(null)
    window.addEventListener('keydown', onKey)
    return () => window.removeEventListener('keydown', onKey)
  }, [popup])

  const totalTime = splits.reduce((sum, s) => sum + s.elapsed_s, 0)
  const maxSpeed = Math.max(...splits.map((s) => s.avg_speed_mps ?? 0))
  if (totalTime <= 0 || maxSpeed <= 0) return null

  const toggle = (index: number) => (event: MouseEvent<HTMLDivElement>) => {
    event.stopPropagation()
    if (popup?.index === index) {
      setPopup(null)
      return
    }
    const el = event.currentTarget
    setPopup({ index, x: el.offsetLeft + el.offsetWidth / 2 })
  }

  return (
    <div ref={wrapRef} style={{ position: 'relative' }} onClick={() => setPopup(null)}>
      <div
        style={{
          display: 'flex',
          alignItems: 'flex-end',
          gap: 2,
          height: CHART_HEIGHT + 22,
          padding: '0 8px 6px'
        }}
      >
        {splits.map((split) => {
          const widthPct = (split.elapsed_s / totalTime) * 100
          const columnPx = (widthPct / 100) * width
          const speed = split.avg_speed_mps ?? 0
          const height = Math.max((speed / maxSpeed) * CHART_HEIGHT, 3)
          const isActive = barColor(split.intensity) === ACTIVE_COLOR
          const pace = formatPace(split.avg_speed_mps).replace(' /km', '')
          const labelAbove = isActive && columnPx >= LABEL_ABOVE_MIN_PX
          const labelInside =
            isActive &&
            !labelAbove &&
            columnPx >= LABEL_INSIDE_MIN_PX &&
            height >= LABEL_INSIDE_MIN_HEIGHT
          const selected = popup?.index === split.index
          return (
            <div
              key={split.index}
              onClick={toggle(split.index)}
              style={{
                width: `${widthPct}%`,
                display: 'flex',
                flexDirection: 'column',
                justifyContent: 'flex-end',
                alignItems: 'center',
                height: '100%',
                minWidth: 3,
                cursor: 'pointer'
              }}
            >
              {labelAbove && (
                <div
                  style={{
                    fontSize: 11,
                    color: 'var(--text-secondary)',
                    fontVariantNumeric: 'tabular-nums',
                    whiteSpace: 'nowrap',
                    marginBottom: 2
                  }}
                >
                  {pace}
                </div>
              )}
              <div
                style={{
                  position: 'relative',
                  width: '100%',
                  height,
                  background: barColor(split.intensity),
                  borderRadius: '3px 3px 0 0',
                  opacity: isActive ? 1 : 0.7,
                  overflow: 'hidden',
                  outline: selected ? '1px solid var(--text-primary)' : 'none'
                }}
              >
                {labelInside && (
                  <span
                    style={{
                      position: 'absolute',
                      top: 4,
                      left: '50%',
                      transform: 'translateX(-50%)',
                      writingMode: 'vertical-rl',
                      fontSize: 10,
                      color: 'rgba(255, 255, 255, 0.9)',
                      fontVariantNumeric: 'tabular-nums'
                    }}
                  >
                    {pace}
                  </span>
                )}
              </div>
            </div>
          )
        })}
      </div>
      {popup && splits[popup.index] && (
        <SplitPopup split={splits[popup.index]} x={popup.x} width={width} />
      )}
    </div>
  )
}

/** Row per split (km or manual lap): bar length ∝ speed, with pace, climb and
 * average heart rate printed. */
function SplitRows({ splits, mode }: { splits: Split[]; mode: 'km' | 'laps' }) {
  const maxSpeed = Math.max(...splits.map((s) => s.avg_speed_mps ?? 0))
  if (maxSpeed <= 0) return null
  const showElevation = splits.some((s) => (s.elevation_gain_m ?? 0) > 0)
  const showHr = splits.some((s) => s.avg_hr !== null)
  const labelWidth = mode === 'km' ? 44 : 90
  const metaWidth = 96 + (showElevation ? 54 : 0) + (showHr ? 70 : 0)

  return (
    <div style={{ padding: '0 8px 10px' }}>
      {splits.map((split) => {
        const speed = split.avg_speed_mps ?? 0
        const label =
          mode === 'km'
            ? split.distance_m >= 999
              ? `${split.index + 1}`
              : formatDistance(split.distance_m)
            : `${split.index + 1} · ${formatDistance(split.distance_m)}`
        const meta = [formatPace(split.avg_speed_mps)]
        if (showElevation && split.elevation_gain_m !== null)
          meta.push(`+${Math.round(split.elevation_gain_m)} m`)
        if (showHr && split.avg_hr !== null) meta.push(`${Math.round(split.avg_hr)} bpm`)
        return (
          <div
            className="split-row"
            key={split.index}
            style={{ gridTemplateColumns: `${labelWidth}px 1fr ${metaWidth}px` }}
            title={splitTitle(split, mode === 'km' ? `km ${split.index + 1}` : `lap ${split.index + 1}`)}
          >
            <span className="muted">{label}</span>
            <div className="bar-track">
              <div
                className="bar-fill"
                style={{ width: `${(speed / maxSpeed) * 100}%`, background: ACTIVE_COLOR }}
              />
            </div>
            <span className="meta">{meta.join(' · ')}</span>
          </div>
        )
      })}
    </div>
  )
}

export default function SplitsChart({ activityId }: { activityId: number }) {
  const splits = useApi<SplitsResponse>(`/api/activities/${activityId}/splits`)
  const data = splits.data
  if (!data || data.mode === 'none' || data.splits.length === 0) return null

  const title =
    data.mode === 'workout' ? 'Intervals' : data.mode === 'laps' ? 'Lap splits' : 'Splits'
  return (
    <div className="chart-card">
      <div className="chart-title">{title}</div>
      {data.mode === 'workout' ? (
        <WorkoutColumns splits={data.splits} />
      ) : (
        <SplitRows splits={data.splits} mode={data.mode} />
      )}
    </div>
  )
}
