import {
  Area,
  AreaChart,
  CartesianGrid,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis
} from 'recharts'
import { Streams } from '../api'
import { formatDuration, formatPaceFromSeconds } from '../format'

const TOOLTIP_STYLE = {
  backgroundColor: '#232322',
  border: '1px solid rgba(255,255,255,0.1)',
  borderRadius: 8,
  color: '#ffffff',
  fontSize: 13
}

interface ChartRow {
  x: number
  pace: number | null
  hr: number | null
  altitude: number | null
}

function buildRows(streams: Streams): { rows: ChartRow[]; byDistance: boolean } {
  const n = streams.time_s.length
  const hasDistance = streams.distance_m.some((d) => d !== null && d > 0)
  const rows: ChartRow[] = []
  for (let i = 0; i < n; i++) {
    const time = streams.time_s[i]
    if (time === null) continue
    const dist = streams.distance_m[i]
    const speed = streams.speed_mps[i]
    rows.push({
      x: hasDistance && dist !== null ? dist / 1000 : time,
      pace: speed !== null && speed > 0.5 ? 1000 / speed : null,
      hr: streams.hr[i],
      altitude: streams.altitude_m[i]
    })
  }
  return { rows, byDistance: hasDistance }
}

interface PanelProps {
  rows: ChartRow[]
  byDistance: boolean
  dataKey: 'pace' | 'hr' | 'altitude'
  title: string
  color: string
  reversed?: boolean
  format: (value: number) => string
}

function Panel({ rows, byDistance, dataKey, title, color, reversed, format }: PanelProps) {
  if (!rows.some((r) => r[dataKey] !== null)) return null
  return (
    <div className="chart-card">
      <div className="chart-title">{title}</div>
      <ResponsiveContainer width="100%" height={170}>
        <AreaChart data={rows} margin={{ top: 4, right: 12, bottom: 0, left: -8 }}>
          <CartesianGrid stroke="var(--grid)" vertical={false} />
          <XAxis
            dataKey="x"
            type="number"
            domain={['dataMin', 'dataMax']}
            tickFormatter={(v: number) => (byDistance ? `${v.toFixed(1)}` : formatDuration(v))}
            stroke="var(--baseline)"
            tick={{ fill: 'var(--text-muted)', fontSize: 11 }}
            minTickGap={40}
          />
          <YAxis
            reversed={reversed}
            domain={['auto', 'auto']}
            tickFormatter={format}
            stroke="var(--baseline)"
            tick={{ fill: 'var(--text-muted)', fontSize: 11 }}
            width={52}
          />
          <Tooltip
            contentStyle={TOOLTIP_STYLE}
            labelFormatter={(v: number) =>
              byDistance ? `${v.toFixed(2)} km` : formatDuration(v)
            }
            formatter={(value: number) => [format(value), title]}
          />
          <Area
            type="monotone"
            dataKey={dataKey}
            stroke={color}
            strokeWidth={2}
            fill={color}
            fillOpacity={0.12}
            dot={false}
            isAnimationActive={false}
            connectNulls
          />
        </AreaChart>
      </ResponsiveContainer>
    </div>
  )
}

interface StreamChartsProps {
  streams: Streams
}

export default function StreamCharts({ streams }: StreamChartsProps) {
  const { rows, byDistance } = buildRows(streams)
  if (rows.length < 2) return null
  return (
    <>
      <Panel
        rows={rows}
        byDistance={byDistance}
        dataKey="pace"
        title={byDistance ? 'Pace (min/km vs km)' : 'Pace (min/km)'}
        color="var(--series-pace)"
        reversed
        format={(v) => formatPaceFromSeconds(v)}
      />
      <Panel
        rows={rows}
        byDistance={byDistance}
        dataKey="hr"
        title="Heart rate (bpm)"
        color="var(--series-hr)"
        format={(v) => `${Math.round(v)}`}
      />
      <Panel
        rows={rows}
        byDistance={byDistance}
        dataKey="altitude"
        title="Elevation (m)"
        color="var(--series-elevation)"
        format={(v) => `${Math.round(v)}`}
      />
    </>
  )
}
