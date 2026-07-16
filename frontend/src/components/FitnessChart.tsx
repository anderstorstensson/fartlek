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
  raceDay?: string | null
}

/** Points after today (projected from the plan) render dashed; the boundary
 * point is duplicated into both halves so the lines connect. */
function splitRows(data: FitnessPoint[]) {
  const lastActualIdx = data.reduce((last, p, i) => (p.projected ? last : i), -1)
  return data.map((p, i) => ({
    day: p.day,
    load: p.load,
    ctl: p.projected ? null : p.ctl,
    atl: p.projected ? null : p.atl,
    tsb: p.projected ? null : p.tsb,
    ctl_proj: p.projected || i === lastActualIdx ? p.ctl : null,
    atl_proj: p.projected || i === lastActualIdx ? p.atl : null,
    tsb_proj: p.projected || i === lastActualIdx ? p.tsb : null
  }))
}

export default function FitnessChart({ data, height = 320, raceDay }: FitnessChartProps) {
  const hasProjection = data.some((p) => p.projected)
  const rows = hasProjection ? splitRows(data) : data
  return (
    <ResponsiveContainer width="100%" height={height}>
      <LineChart data={rows} margin={{ top: 8, right: 12, bottom: 0, left: -12 }}>
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
        {raceDay && (
          <ReferenceLine
            x={raceDay}
            stroke="var(--series-workout)"
            strokeDasharray="4 4"
            label={({ viewBox }: { viewBox: { x: number; y: number } }) => (
              <text
                x={viewBox.x - 5}
                y={viewBox.y + 12}
                textAnchor="end"
                fill="var(--text-muted)"
                fontSize={11}
              >
                race
              </text>
            )}
          />
        )}
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
        {hasProjection &&
          SERIES.map((series) => (
            <Line
              key={`${series.key}_proj`}
              type="monotone"
              dataKey={`${series.key}_proj`}
              stroke={series.color}
              strokeWidth={2}
              strokeDasharray="6 4"
              strokeOpacity={0.75}
              dot={false}
              legendType="none"
              tooltipType="none"
              isAnimationActive={false}
            />
          ))}
      </LineChart>
    </ResponsiveContainer>
  )
}
