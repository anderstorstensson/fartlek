import { memo, useState } from 'react'
import {
  Area,
  AreaChart,
  CartesianGrid,
  ComposedChart,
  Line,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis
} from 'recharts'
import { ActivityDetail, Streams } from '../api'
import { formatDuration, formatPace, formatPaceFromSeconds } from '../format'

const TOOLTIP_STYLE = {
  backgroundColor: '#232322',
  border: '1px solid rgba(255,255,255,0.1)',
  borderRadius: 8,
  color: '#ffffff',
  fontSize: 13
}

/* Hover overlay order: pace, heart rate, cadence, elevation. */
const TOOLTIP_ORDER: Record<string, number> = {
  Pace: 0,
  GAP: 0,
  'Heart rate': 1,
  Cadence: 2,
  Elevation: 3
}

/** Chart hover callback: original stream sample index, or null when leaving. */
export type HoverIndexHandler = (index: number | null) => void

interface ChartRow {
  x: number
  streamIndex: number
  pace: number | null
  gapPace: number | null
  hr: number | null
  cadence: number | null
  altitude: number | null
  power: number | null
  respiration: number | null
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
    const gapSpeed = streams.gap_speed_mps[i] ?? null
    const cadence = streams.cadence[i]
    rows.push({
      x: hasDistance && dist !== null ? dist / 1000 : time,
      streamIndex: i,
      pace: speed !== null && speed > 0.5 ? 1000 / speed : null,
      gapPace: gapSpeed !== null && gapSpeed > 0.5 ? 1000 / gapSpeed : null,
      hr: streams.hr[i],
      // FIT records carry running cadence as rpm (one leg); display spm.
      cadence: cadence !== null && cadence > 0 ? cadence * 2 : null,
      altitude: streams.altitude_m[i],
      power: streams.power[i] ?? null,
      respiration: streams.respiration[i] ?? null
    })
  }
  return { rows, byDistance: hasDistance }
}

/** Domain that confines a series' data to a vertical band of the chart.
 * fTop/fBot are fractions from the chart top (0 = top, 1 = bottom). */
function bandDomain(
  lo: number,
  hi: number,
  fTop: number,
  fBot: number,
  reversed: boolean,
  minSpan: number
): [number, number] {
  const range = Math.max(hi - lo, minSpan)
  const span = range / (fBot - fTop)
  const min = reversed ? lo - span * fTop : lo - span * (1 - fBot)
  return [min, min + span]
}

function seriesRange(rows: ChartRow[], key: keyof ChartRow): [number, number] {
  const values = rows.map((r) => r[key]).filter((v): v is number => v !== null)
  if (values.length === 0) return [0, 0]
  return [Math.min(...values), Math.max(...values)]
}

/** Recharts mouse-state → original stream index reporting, shared by all panels. */
function hoverHandlers(rows: ChartRow[], onHoverIndex?: HoverIndexHandler) {
  if (!onHoverIndex) return {}
  return {
    onMouseMove: (state: { activeTooltipIndex?: number | string }) => {
      const idx = typeof state?.activeTooltipIndex === 'number' ? state.activeTooltipIndex : null
      onHoverIndex(idx !== null && rows[idx] ? rows[idx].streamIndex : null)
    },
    onMouseLeave: () => onHoverIndex(null)
  }
}

type SeriesKey = 'pace' | 'hr' | 'cadence' | 'elevation'

const SERIES_META: Record<SeriesKey, { color: string; minSpan: number }> = {
  pace: { color: 'var(--series-pace)', minSpan: 30 },
  hr: { color: 'var(--series-hr)', minSpan: 10 },
  cadence: { color: 'var(--series-cadence)', minSpan: 10 },
  elevation: { color: 'var(--series-elevation)', minSpan: 10 }
}

/** Combined pace + HR + cadence + elevation chart (Strava-style): elevation as
 * a muted background area, the rest as banded lines, one hover for all, and
 * show/hide chips with the activity averages underneath. */
function CombinedPanel({
  rows,
  byDistance,
  activity,
  onHoverIndex
}: {
  rows: ChartRow[]
  byDistance: boolean
  activity: ActivityDetail
  onHoverIndex?: HoverIndexHandler
}) {
  const [paceMode, setPaceMode] = useState<'pace' | 'gap'>('pace')
  const [visible, setVisible] = useState<Record<SeriesKey, boolean>>({
    pace: true,
    hr: true,
    cadence: false,
    elevation: true
  })

  const available: Record<SeriesKey, boolean> = {
    pace: rows.some((r) => r.pace !== null),
    hr: rows.some((r) => r.hr !== null),
    cadence: rows.some((r) => r.cadence !== null),
    elevation: rows.some((r) => r.altitude !== null)
  }
  if (!available.pace && !available.hr && !available.elevation) return null
  const shown = (key: SeriesKey) => available[key] && visible[key]

  const hasGap = rows.some(
    (r) => r.pace !== null && r.gapPace !== null && Math.abs(r.gapPace - r.pace) / r.pace > 0.01
  )
  const paceKey = paceMode === 'gap' && hasGap ? 'gapPace' : 'pace'

  // Vertical layout: shown line series split the region above the elevation
  // band evenly; hiding a series re-spreads the rest (the "auto scale").
  const lineOrder: SeriesKey[] = ['pace', 'hr', 'cadence']
  const shownLines = lineOrder.filter(shown)
  const regionBottom = shown('elevation') ? 0.72 : 0.95
  const bandHeight = shownLines.length ? (regionBottom - 0.03) / shownLines.length : 0
  const domains: Partial<Record<SeriesKey, [number, number]>> = {}
  shownLines.forEach((key, i) => {
    const rowKey: keyof ChartRow = key === 'pace' ? paceKey : (key as 'hr' | 'cadence')
    const [lo, hi] = seriesRange(rows, rowKey)
    const fTop = 0.03 + i * bandHeight + (i > 0 ? 0.02 : 0)
    const fBot = 0.03 + (i + 1) * bandHeight - 0.02
    domains[key] = bandDomain(lo, hi, fTop, fBot, key === 'pace', SERIES_META[key].minSpan)
  })
  if (shown('elevation')) {
    const [lo, hi] = seriesRange(rows, 'altitude')
    domains.elevation = bandDomain(lo, hi, 0.8, 1.0, false, SERIES_META.elevation.minSpan)
  }

  const toggle = (key: SeriesKey) =>
    setVisible((current) => ({ ...current, [key]: !current[key] }))

  const paceStat =
    paceKey === 'gapPace' && activity.gap_speed_mps !== null
      ? `${formatPace(activity.gap_speed_mps)} GAP`
      : formatPace(activity.avg_speed_mps)
  const stats: Record<SeriesKey, string> = {
    pace: paceStat,
    hr: activity.avg_hr !== null ? `${Math.round(activity.avg_hr)} bpm` : '–',
    cadence: activity.avg_cadence !== null ? `${Math.round(activity.avg_cadence)} spm` : '–',
    elevation: activity.ascent_m !== null ? `${Math.round(activity.ascent_m)} m` : '–'
  }
  const labels: Record<SeriesKey, string> = {
    pace: paceKey === 'gapPace' ? 'GAP' : 'Pace',
    hr: 'Heart rate',
    cadence: 'Cadence',
    elevation: 'Elevation'
  }

  return (
    <div className="chart-card">
      <div className="chart-title">
        <span>Pace · heart rate · elevation</span>
        {hasGap && (
          <span className="segmented">
            <button className={paceMode === 'pace' ? 'on' : ''} onClick={() => setPaceMode('pace')}>
              Pace
            </button>
            <button className={paceMode === 'gap' ? 'on' : ''} onClick={() => setPaceMode('gap')}>
              GAP
            </button>
          </span>
        )}
      </div>
      <ResponsiveContainer width="100%" height={260}>
        <ComposedChart
          data={rows}
          margin={{ top: 4, right: 12, bottom: 0, left: 12 }}
          {...hoverHandlers(rows, onHoverIndex)}
        >
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
          {/* Banded domains make tick values meaningless — axes stay hidden,
              the tooltip and the chips carry the numbers. */}
          {shown('pace') && <YAxis yAxisId="pace" reversed hide domain={domains.pace} />}
          {shown('hr') && <YAxis yAxisId="hr" hide domain={domains.hr} />}
          {shown('cadence') && <YAxis yAxisId="cadence" hide domain={domains.cadence} />}
          {shown('elevation') && <YAxis yAxisId="elevation" hide domain={domains.elevation} />}
          <Tooltip
            contentStyle={TOOLTIP_STYLE}
            itemSorter={(item) => TOOLTIP_ORDER[String(item.name)] ?? 9}
            labelFormatter={(v: number) =>
              byDistance ? `${v.toFixed(2)} km` : formatDuration(v)
            }
            formatter={(value: number, name: string) => {
              if (name === 'Pace' || name === 'GAP') return [formatPaceFromSeconds(value), name]
              if (name === 'Heart rate') return [`${Math.round(value)} bpm`, name]
              if (name === 'Cadence') return [`${Math.round(value)} spm`, name]
              return [`${Math.round(value)} m`, name]
            }}
          />
          {shown('elevation') && (
            <Area
              yAxisId="elevation"
              type="monotone"
              dataKey="altitude"
              name="Elevation"
              stroke="var(--series-elevation)"
              strokeWidth={1}
              fill="var(--series-elevation)"
              fillOpacity={0.2}
              dot={false}
              isAnimationActive={false}
              connectNulls
            />
          )}
          {shown('pace') && (
            <Line
              yAxisId="pace"
              type="monotone"
              dataKey={paceKey}
              name={labels.pace}
              stroke="var(--series-pace)"
              strokeWidth={2}
              dot={false}
              isAnimationActive={false}
              connectNulls
            />
          )}
          {shown('hr') && (
            <Line
              yAxisId="hr"
              type="monotone"
              dataKey="hr"
              name="Heart rate"
              stroke="var(--series-hr)"
              strokeWidth={1.5}
              dot={false}
              isAnimationActive={false}
              connectNulls
            />
          )}
          {shown('cadence') && (
            <Line
              yAxisId="cadence"
              type="monotone"
              dataKey="cadence"
              name="Cadence"
              stroke="var(--series-cadence)"
              strokeWidth={1.5}
              dot={false}
              isAnimationActive={false}
              connectNulls
            />
          )}
        </ComposedChart>
      </ResponsiveContainer>
      <div className="series-toggles">
        {(['pace', 'hr', 'cadence', 'elevation'] as SeriesKey[])
          .filter((key) => available[key])
          .map((key) => (
            <button
              key={key}
              className={`series-toggle${visible[key] ? '' : ' off'}`}
              onClick={() => toggle(key)}
              title={visible[key] ? 'Hide' : 'Show'}
            >
              <span className="dot" style={{ background: SERIES_META[key].color }} />
              {labels[key]}
              <span className="stat">{stats[key]}</span>
            </button>
          ))}
      </div>
    </div>
  )
}

interface PanelProps {
  rows: ChartRow[]
  byDistance: boolean
  dataKey: 'power' | 'respiration'
  title: string
  color: string
  format: (value: number) => string
  onHoverIndex?: HoverIndexHandler
}

function Panel({ rows, byDistance, dataKey, title, color, format, onHoverIndex }: PanelProps) {
  if (!rows.some((r) => r[dataKey] !== null)) return null
  return (
    <div className="chart-card">
      <div className="chart-title">{title}</div>
      <ResponsiveContainer width="100%" height={170}>
        <AreaChart
          data={rows}
          margin={{ top: 4, right: 12, bottom: 0, left: -8 }}
          {...hoverHandlers(rows, onHoverIndex)}
        >
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
  activity: ActivityDetail
  onHoverIndex?: HoverIndexHandler
}

/** Memoized: hover state lives in the parent and must not re-render the charts. */
const StreamCharts = memo(function StreamCharts({
  streams,
  activity,
  onHoverIndex
}: StreamChartsProps) {
  const { rows, byDistance } = buildRows(streams)
  if (rows.length < 2) return null
  return (
    <>
      <CombinedPanel
        rows={rows}
        byDistance={byDistance}
        activity={activity}
        onHoverIndex={onHoverIndex}
      />
      <Panel
        rows={rows}
        byDistance={byDistance}
        dataKey="power"
        title="Power (W)"
        color="var(--series-power)"
        format={(v) => `${Math.round(v)}`}
        onHoverIndex={onHoverIndex}
      />
      <Panel
        rows={rows}
        byDistance={byDistance}
        dataKey="respiration"
        title="Respiration (brpm)"
        color="var(--series-respiration)"
        format={(v) => `${Math.round(v)}`}
        onHoverIndex={onHoverIndex}
      />
    </>
  )
})

export default StreamCharts
