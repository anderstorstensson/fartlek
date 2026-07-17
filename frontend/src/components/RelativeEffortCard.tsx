import { RelativeEffort, useApi } from '../api'
import { formatDate } from '../format'

const BAND_STYLES: Record<string, { color: string; label: string }> = {
  easy: { color: '#6dbf7b', label: 'Easy' },
  moderate: { color: '#3987e5', label: 'Moderate' },
  tough: { color: '#e5a139', label: 'Tough' },
  massive: { color: '#e55c39', label: 'Massive' }
}

const STRIP_HEIGHT = 44

/** The session's TRIMP ranked against the trailing 90 days, Strava
 * relative-effort style: headline + band, one-line context sentence, and a
 * strip of recent session loads with this one highlighted. */
export default function RelativeEffortCard({ activityId }: { activityId: number }) {
  const effort = useApi<RelativeEffort>(`/api/activities/${activityId}/relative-effort`)
  const data = effort.data
  if (!data || data.load === null) return null

  const band = data.band ? BAND_STYLES[data.band] : null
  const maxLoad = Math.max(...data.recent.map((r) => r.load), data.load)

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
        <div>
          <span style={{ fontSize: 28, fontWeight: 600 }}>{Math.round(data.load)}</span>
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
        {data.recent.length > 1 && (
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
