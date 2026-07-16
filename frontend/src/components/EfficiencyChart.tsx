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
import { EfficiencyPoint } from '../api'
import { formatShortDate } from '../format'

const TOOLTIP_STYLE = {
  backgroundColor: '#232322',
  border: '1px solid rgba(255,255,255,0.1)',
  borderRadius: 8,
  color: '#ffffff',
  fontSize: 13
}

interface EfficiencyChartProps {
  data: EfficiencyPoint[]
  height?: number
}

/** Efficiency (GAP m/min per heartbeat, left axis) and aerobic decoupling
 * (%, right axis) per run over time. Efficiency trending up and decoupling
 * trending down are both fitness gains. */
export default function EfficiencyChart({ data, height = 260 }: EfficiencyChartProps) {
  const rows = data.map((p) => ({
    day: p.day,
    name: p.name,
    efficiency: p.efficiency_index,
    decoupling: p.decoupling_pct
  }))

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
          yAxisId="efficiency"
          domain={['auto', 'auto']}
          stroke="var(--baseline)"
          tick={{ fill: 'var(--text-muted)', fontSize: 11 }}
          tickFormatter={(v: number) => v.toFixed(2)}
        />
        <YAxis
          yAxisId="decoupling"
          orientation="right"
          domain={['auto', 'auto']}
          stroke="var(--baseline)"
          tick={{ fill: 'var(--text-muted)', fontSize: 11 }}
          tickFormatter={(v: number) => `${v.toFixed(0)}%`}
        />
        <Tooltip
          contentStyle={TOOLTIP_STYLE}
          labelFormatter={(day) => formatShortDate(String(day))}
          formatter={(value: number, name: string) => [
            name === 'Decoupling' ? `${value.toFixed(1)}%` : value.toFixed(2),
            name
          ]}
        />
        <Legend wrapperStyle={{ fontSize: 13, color: 'var(--text-secondary)' }} />
        <ReferenceLine yAxisId="decoupling" y={5} stroke="var(--baseline)" strokeDasharray="4 4" />
        <Line
          yAxisId="efficiency"
          type="monotone"
          dataKey="efficiency"
          name="Efficiency (GAP m/min per beat)"
          stroke="var(--series-efficiency)"
          strokeWidth={1.5}
          dot={{ r: 2 }}
          connectNulls
          isAnimationActive={false}
        />
        <Line
          yAxisId="decoupling"
          type="monotone"
          dataKey="decoupling"
          name="Decoupling"
          stroke="var(--series-decoupling)"
          strokeWidth={1.5}
          dot={{ r: 2 }}
          connectNulls
          isAnimationActive={false}
        />
      </LineChart>
    </ResponsiveContainer>
  )
}
