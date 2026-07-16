import {
  Bar,
  BarChart,
  CartesianGrid,
  Legend,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis
} from 'recharts'
import { WeeklyZones } from '../api'
import { formatDuration, formatShortDate } from '../format'

/* Same ordinal ramp as ZoneChart. */
const ZONE_COLORS = ['#9ec5f4', '#6da7ec', '#3987e5', '#256abf', '#184f95']
const ZONE_NAMES = ['Z1', 'Z2', 'Z3', 'Z4', 'Z5']

const TOOLTIP_STYLE = {
  backgroundColor: '#232322',
  border: '1px solid rgba(255,255,255,0.1)',
  borderRadius: 8,
  color: '#ffffff',
  fontSize: 13
}

interface ZoneDistributionChartProps {
  data: WeeklyZones[]
  height?: number
}

export default function ZoneDistributionChart({ data, height = 240 }: ZoneDistributionChartProps) {
  const rows = data.map((week) => ({
    week_start: week.week_start,
    z1: (week.zone_seconds[0] ?? 0) / 3600,
    z2: (week.zone_seconds[1] ?? 0) / 3600,
    z3: (week.zone_seconds[2] ?? 0) / 3600,
    z4: (week.zone_seconds[3] ?? 0) / 3600,
    z5: (week.zone_seconds[4] ?? 0) / 3600
  }))

  const totals = data.reduce(
    (acc, week) => acc.map((v, i) => v + (week.zone_seconds[i] ?? 0)),
    [0, 0, 0, 0, 0]
  )
  const totalAll = totals.reduce((sum, v) => sum + v, 0)
  const low = totals[0] + totals[1]
  const high = totals[3] + totals[4]

  return (
    <>
      <ResponsiveContainer width="100%" height={height}>
        <BarChart data={rows} margin={{ top: 4, right: 12, bottom: 0, left: -12 }}>
          <CartesianGrid stroke="var(--grid)" vertical={false} />
          <XAxis
            dataKey="week_start"
            tickFormatter={formatShortDate}
            stroke="var(--baseline)"
            tick={{ fill: 'var(--text-muted)', fontSize: 11 }}
            minTickGap={32}
          />
          <YAxis
            stroke="var(--baseline)"
            tick={{ fill: 'var(--text-muted)', fontSize: 11 }}
            tickFormatter={(v: number) => `${v.toFixed(0)}h`}
          />
          <Tooltip
            contentStyle={TOOLTIP_STYLE}
            labelFormatter={(day) => `Week of ${formatShortDate(String(day))}`}
            formatter={(value: number, name: string) => [formatDuration(value * 3600), name]}
          />
          <Legend wrapperStyle={{ fontSize: 13, color: 'var(--text-secondary)' }} />
          {ZONE_NAMES.map((name, i) => (
            <Bar
              key={name}
              dataKey={name.toLowerCase()}
              name={name}
              stackId="zones"
              fill={ZONE_COLORS[i]}
              isAnimationActive={false}
            />
          ))}
        </BarChart>
      </ResponsiveContainer>
      {totalAll > 0 && (
        <p className="muted" style={{ fontSize: 12, padding: '4px 8px' }}>
          Whole window: {((low / totalAll) * 100).toFixed(0)}% low (Z1–Z2) ·{' '}
          {((totals[2] / totalAll) * 100).toFixed(0)}% moderate (Z3) ·{' '}
          {((high / totalAll) * 100).toFixed(0)}% high (Z4–Z5). Polarized training targets
          roughly 80% low; a fat Z3 share suggests easy runs drifting too hard.
        </p>
      )}
    </>
  )
}
