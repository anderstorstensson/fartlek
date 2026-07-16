import { Streams } from '../api'
import { formatDuration, formatPace } from '../format'

/* Ordinal single-hue blue ramp (pace), light → dark. */
const ZONE_COLORS = ['#9ec5f4', '#6da7ec', '#3987e5', '#256abf', '#184f95']

const ZONE_LABELS = ['recovery', 'easy', 'marathon', 'threshold', 'VO2max+']

interface PaceZoneChartProps {
  streams: Streams
}

/** Time-in-pace-zone bars, the pace twin of the HR-zone chart. Zones are
 * fractions of threshold speed; classification uses GAP when enabled. */
export default function PaceZoneChart({ streams }: PaceZoneChartProps) {
  const total = streams.time_in_pace_zones_s.reduce((sum, v) => sum + v, 0)
  if (total <= 0 || streams.pace_zones.length === 0) return null

  return (
    <div className="chart-card">
      <div className="chart-title">Time in pace zones (min/km)</div>
      <div style={{ padding: '0 8px 10px' }}>
        {streams.pace_zones.map((zone, i) => {
          const seconds = streams.time_in_pace_zones_s[i] ?? 0
          const pct = (seconds / total) * 100
          const slow = formatPace(zone.low_speed_mps).replace(' /km', '')
          const fast = zone.high_speed_mps
            ? formatPace(zone.high_speed_mps).replace(' /km', '')
            : null
          const range = fast ? `${slow}–${fast}` : `<${slow}`
          return (
            <div className="zone-row" key={zone.name}>
              <span>
                {zone.name} {ZONE_LABELS[i]} <span className="zone-range">({range})</span>
              </span>
              <div className="bar-track">
                <div
                  className="bar-fill"
                  style={{ width: `${pct}%`, background: ZONE_COLORS[i] }}
                />
              </div>
              <span className="meta">
                {formatDuration(seconds)} · {pct.toFixed(0)}%
              </span>
            </div>
          )
        })}
      </div>
    </div>
  )
}
