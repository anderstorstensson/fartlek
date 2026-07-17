import {
  CartesianGrid,
  Line,
  LineChart,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis
} from 'recharts'
import { WellnessDay } from '../api'
import { formatShortDate } from '../format'

const TOOLTIP_STYLE = {
  backgroundColor: '#232322',
  border: '1px solid rgba(255,255,255,0.1)',
  borderRadius: 8,
  color: '#ffffff',
  fontSize: 13
}

interface Vo2maxChartProps {
  data: WellnessDay[]
  height?: number
}

/** Garmin's daily running VO2 max estimate over time. Days without a value
 * (no qualifying run) are skipped; the line connects across them. */
export default function Vo2maxChart({ data, height = 220 }: Vo2maxChartProps) {
  const rows = data
    .filter((d) => d.vo2max !== null)
    .map((d) => ({ day: d.day, vo2max: d.vo2max }))

  if (rows.length === 0) {
    return (
      <p className="muted" style={{ padding: '4px 8px' }}>
        No VO₂max data yet — run a sync (Garmin estimates it on outdoor runs with HR).
      </p>
    )
  }

  return (
    <ResponsiveContainer width="100%" height={height}>
      <LineChart data={rows} margin={{ top: 8, right: 0, bottom: 0, left: -12 }}>
        <CartesianGrid stroke="var(--grid)" vertical={false} />
        <XAxis
          dataKey="day"
          tickFormatter={formatShortDate}
          stroke="var(--baseline)"
          tick={{ fill: 'var(--text-muted)', fontSize: 11 }}
          minTickGap={48}
        />
        <YAxis
          domain={['auto', 'auto']}
          stroke="var(--baseline)"
          tick={{ fill: 'var(--text-muted)', fontSize: 11 }}
          tickFormatter={(v: number) => v.toFixed(0)}
        />
        <Tooltip
          contentStyle={TOOLTIP_STYLE}
          labelFormatter={(day) => formatShortDate(String(day))}
          formatter={(value: number) => [value.toFixed(1), 'VO₂max']}
        />
        <Line
          type="monotone"
          dataKey="vo2max"
          name="VO₂max"
          stroke="var(--series-efficiency)"
          strokeWidth={1.5}
          dot={{ r: 2 }}
          connectNulls
          isAnimationActive={false}
        />
      </LineChart>
    </ResponsiveContainer>
  )
}
