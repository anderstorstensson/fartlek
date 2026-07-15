import { Streams } from '../api'
import { formatDuration } from '../format'

/* Ordinal single-hue ramp (validated for the dark surface). */
const ZONE_COLORS = ['#9ec5f4', '#6da7ec', '#3987e5', '#256abf', '#184f95']

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
          return (
            <div className="zone-row" key={zone.name}>
              <span>{zone.name}</span>
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
        <div className="zone-row muted" style={{ fontSize: 12 }}>
          <span />
          <span>
            {streams.zones
              .map((z) => `${z.name} ${z.low_bpm}${z.high_bpm ? `–${z.high_bpm}` : '+'}`)
              .join('  ·  ')}{' '}
            bpm
          </span>
          <span />
        </div>
      </div>
    </div>
  )
}
