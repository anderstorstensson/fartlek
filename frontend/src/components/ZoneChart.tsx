import { Streams } from '../api'
import { formatDuration } from '../format'

/* Ordinal single-hue red ramp (heart rate), light → dark. */
const ZONE_COLORS = ['#f6b3b3', '#f08c8c', '#e66767', '#c74848', '#9c3232']

interface ZoneChartProps {
  streams: Streams
}

export default function ZoneChart({ streams }: ZoneChartProps) {
  const total = streams.time_in_zones_s.reduce((sum, v) => sum + v, 0)
  if (total <= 0) return null

  return (
    <div className="chart-card">
      <div className="chart-title">Time in heart-rate zones</div>
      <div style={{ padding: '0 8px 10px' }}>
        {streams.zones.map((zone, i) => {
          const seconds = streams.time_in_zones_s[i] ?? 0
          const pct = (seconds / total) * 100
          const range = zone.high_bpm
            ? `${zone.low_bpm}–${zone.high_bpm} bpm`
            : `${zone.low_bpm}+ bpm`
          return (
            <div className="zone-row" key={zone.name}>
              <span>
                {zone.name} <span className="zone-range">({range})</span>
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
