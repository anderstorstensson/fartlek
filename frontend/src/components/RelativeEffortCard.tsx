import { RelativeEffort, useApi } from '../api'
import { formatDate } from '../format'

const BAND_STYLES: Record<string, { color: string; label: string }> = {
  easy: { color: '#6dbf7b', label: 'Easy' },
  moderate: { color: '#3987e5', label: 'Moderate' },
  tough: { color: '#e5a139', label: 'Tough' },
  massive: { color: '#e55c39', label: 'Massive' }
}

const STRIP_HEIGHT = 44

// Garmin's five feel smileys, 1 (very weak) … 5 (very strong).
const FEEL_LABELS = ['very weak', 'weak', 'normal', 'strong', 'very strong']

function feelLabel(feel: number | null): string | null {
  if (feel === null) return null
  const label = FEEL_LABELS[feel - 1]
  return label ? `felt ${label}` : null
}

interface RelativeEffortCardProps {
  activityId: number
  /** Watch self-evaluation (RPE 1-10, feel 1-5); shown next to the load. */
  perceivedExertion?: number | null
  feel?: number | null
}

/** The session's TRIMP ranked against the trailing 90 days, Strava
 * relative-effort style: headline + band, one-line context sentence, the
 * athlete's own rating (when entered on the watch), and a strip of recent
 * session loads with this one highlighted. */
export default function RelativeEffortCard({
  activityId,
  perceivedExertion = null,
  feel = null
}: RelativeEffortCardProps) {
  const effort = useApi<RelativeEffort>(`/api/activities/${activityId}/relative-effort`)
  const data = effort.data
  const hasSelfEval = perceivedExertion !== null || feel !== null
  const hasLoad = data !== null && data.load !== null
  if (!hasLoad && !hasSelfEval) return null

  const band = hasLoad && data.band ? BAND_STYLES[data.band] : null
  const maxLoad = hasLoad ? Math.max(...data.recent.map((r) => r.load), data.load!) : 0

  return (
    <div className="chart-card">
      <div className="chart-title">Relative effort</div>
      <div
        style={{
          display: 'flex',
          alignItems: 'center',
          gap: 20,
          padding: '0 8px 10px',
          flexWrap: 'wrap'
        }}
      >
        {hasLoad && (
          <div>
            <span style={{ fontSize: 28, fontWeight: 600 }}>{Math.round(data.load!)}</span>
            {band && (
              <span
                className="badge"
                style={{ marginLeft: 10, color: band.color, borderColor: band.color }}
              >
                {band.label}
              </span>
            )}
            <div className="muted" style={{ fontSize: 13, marginTop: 2 }}>
              {data.percentile !== null
                ? `Harder than ${Math.round(data.percentile)}% of your ${data.window_sessions} sessions in the last ${data.window_days} days`
                : 'Not enough recent sessions to put this effort in context yet'}
            </div>
          </div>
        )}
        {hasSelfEval && (
          <div>
            <div style={{ fontSize: 17, fontWeight: 600 }}>
              {perceivedExertion !== null ? `RPE ${perceivedExertion}/10` : feelLabel(feel)}
            </div>
            <div className="muted" style={{ fontSize: 13, marginTop: 2 }}>
              {perceivedExertion !== null
                ? (feelLabel(feel) ?? 'your rating on the watch')
                : 'your rating on the watch'}
            </div>
          </div>
        )}
        {hasLoad && data.recent.length > 1 && (
          <div
            style={{
              display: 'flex',
              alignItems: 'flex-end',
              gap: 2,
              height: STRIP_HEIGHT,
              flex: '1 1 200px',
              maxWidth: 420
            }}
          >
            {data.recent.map((r) => (
              <div
                key={r.activity_id}
                title={`${r.name} · ${formatDate(r.day)} · ${Math.round(r.load)}`}
                style={{
                  flex: 1,
                  height: Math.max((r.load / maxLoad) * STRIP_HEIGHT, 2),
                  background: r.current ? (band?.color ?? 'var(--accent)') : 'var(--surface-2)',
                  border: r.current ? 'none' : '1px solid var(--grid)',
                  borderRadius: 2,
                  boxSizing: 'border-box'
                }}
              />
            ))}
          </div>
        )}
      </div>
    </div>
  )
}
