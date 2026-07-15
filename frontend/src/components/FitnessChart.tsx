import {
  CartesianGrid,
  Legend,
  Line,
  LineChart,
  ReferenceLine,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis
} from 'recharts'
import { FitnessPoint } from '../api'
import { formatShortDate } from '../format'

const SERIES = [
  { key: 'ctl', name: 'Fitness (CTL)', color: 'var(--series-fitness)' },
  { key: 'atl', name: 'Fatigue (ATL)', color: 'var(--series-fatigue)' },
  { key: 'tsb', name: 'Form (TSB)', color: 'var(--series-form)' }
] as const

const TOOLTIP_STYLE = {
  backgroundColor: '#232322',
  border: '1px solid rgba(255,255,255,0.1)',
  borderRadius: 8,
  color: '#ffffff',
  fontSize: 13
}

interface FitnessChartProps {
  data: FitnessPoint[]
  height?: number
}

export default function FitnessChart({ data, height = 320 }: FitnessChartProps) {
  return (
    <ResponsiveContainer width="100%" height={height}>
      <LineChart data={data} margin={{ top: 8, right: 12, bottom: 0, left: -12 }}>
        <CartesianGrid stroke="var(--grid)" vertical={false} />
        <XAxis
          dataKey="day"
          tickFormatter={formatShortDate}
          stroke="var(--baseline)"
          tick={{ fill: 'var(--text-muted)', fontSize: 12 }}
          minTickGap={48}
        />
        <YAxis
          stroke="var(--baseline)"
          tick={{ fill: 'var(--text-muted)', fontSize: 12 }}
        />
        <Tooltip
          contentStyle={TOOLTIP_STYLE}
          labelFormatter={(day) => formatShortDate(String(day))}
          formatter={(value: number) => value.toFixed(1)}
        />
        <Legend wrapperStyle={{ fontSize: 13, color: 'var(--text-secondary)' }} />
        <ReferenceLine y={0} stroke="var(--baseline)" />
        {SERIES.map((series) => (
          <Line
            key={series.key}
            type="monotone"
            dataKey={series.key}
            name={series.name}
            stroke={series.color}
            strokeWidth={2}
            dot={false}
            activeDot={{ r: 4 }}
            isAnimationActive={false}
          />
        ))}
      </LineChart>
    </ResponsiveContainer>
  )
}
