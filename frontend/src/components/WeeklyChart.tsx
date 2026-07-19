import {
  Bar,
  BarChart,
  CartesianGrid,
  Cell,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis
} from 'recharts'
import { WeeklyStat } from '../api'
import { distanceUnitLabel, formatDuration, formatShortDate, metersToDistanceUnit } from '../format'

function currentWeekKey(): string {
  const now = new Date()
  const monday = new Date(now)
  monday.setDate(now.getDate() - ((now.getDay() + 6) % 7))
  const m = String(monday.getMonth() + 1).padStart(2, '0')
  const d = String(monday.getDate()).padStart(2, '0')
  return `${monday.getFullYear()}-${m}-${d}`
}

export type WeeklyMetric = 'distance' | 'time' | 'load'

const METRIC_CONFIG: Record<WeeklyMetric, { name: string; format: (v: number) => string }> = {
  distance: { name: 'Run distance', format: (v) => `${v.toFixed(1)} ${distanceUnitLabel()}` },
  time: { name: 'Moving time', format: (v) => formatDuration(v * 3600) },
  load: { name: 'Training load (TRIMP)', format: (v) => v.toFixed(0) }
}

interface WeeklyChartProps {
  data: WeeklyStat[]
  metric: WeeklyMetric
  height?: number
  selectedWeek?: string | null
  onSelectWeek?: (weekStart: string | null) => void
}

export default function WeeklyChart({
  data,
  metric,
  height = 260,
  selectedWeek = null,
  onSelectWeek
}: WeeklyChartProps) {
  const config = METRIC_CONFIG[metric]
  const thisWeek = currentWeekKey()
  const rows = data.map((week) => ({
    week_start: week.week_start,
    value:
      metric === 'distance'
        ? metersToDistanceUnit(week.run_distance_m)
        : metric === 'time'
          ? week.total_moving_s / 3600
          : week.load_trimp
  }))

  return (
    <ResponsiveContainer width="100%" height={height}>
      <BarChart data={rows} margin={{ top: 8, right: 12, bottom: 0, left: -12 }}>
        <CartesianGrid stroke="var(--grid)" vertical={false} />
        <XAxis
          dataKey="week_start"
          tickFormatter={formatShortDate}
          stroke="var(--baseline)"
          tick={{ fill: 'var(--text-muted)', fontSize: 12 }}
          minTickGap={40}
        />
        <YAxis stroke="var(--baseline)" tick={{ fill: 'var(--text-muted)', fontSize: 12 }} />
        <Tooltip
          contentStyle={{
            backgroundColor: '#232322',
            border: '1px solid rgba(255,255,255,0.1)',
            borderRadius: 8,
            color: '#ffffff',
            fontSize: 13
          }}
          labelFormatter={(day) =>
            `Week of ${formatShortDate(String(day))}${String(day) === thisWeek ? ' (in progress)' : ''}`
          }
          formatter={(value: number) => [config.format(value), config.name]}
          cursor={{ fill: 'rgba(255,255,255,0.05)' }}
        />
        <Bar
          dataKey="value"
          name={config.name}
          fill="var(--series-fitness)"
          radius={[4, 4, 0, 0]}
          isAnimationActive={false}
          cursor={onSelectWeek ? 'pointer' : undefined}
          onClick={(row: { week_start?: string; payload?: { week_start?: string } }) => {
            const weekStart = row.week_start ?? row.payload?.week_start
            if (onSelectWeek && weekStart) {
              onSelectWeek(weekStart === selectedWeek ? null : weekStart)
            }
          }}
        >
          {rows.map((row) => (
            <Cell
              key={row.week_start}
              fillOpacity={
                selectedWeek
                  ? row.week_start === selectedWeek
                    ? 1
                    : 0.3
                  : row.week_start === thisWeek
                    ? 0.4
                    : 1
              }
            />
          ))}
        </Bar>
      </BarChart>
    </ResponsiveContainer>
  )
}
