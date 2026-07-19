import { Link } from 'react-router-dom'
import { RecordEntry, useApi } from '../api'
import {
  formatDuration,
  formatMediumDate,
  formatPaceFromSeconds,
  paceUnitLabel,
  paceUnitMeters
} from '../format'

export default function Records() {
  const records = useApi<RecordEntry[]>('/api/records?top=5')

  if (records.error) return <div className="error-box">{records.error}</div>

  const grouped = new Map<string, RecordEntry[]>()
  for (const entry of records.data ?? []) {
    const list = grouped.get(entry.label) ?? []
    grouped.set(entry.label, [...list, entry])
  }

  return (
    <>
      <h1>Personal records</h1>
      {grouped.size === 0 && (
        <div className="empty-state">No best efforts yet — sync some runs first.</div>
      )}
      {[...grouped.entries()]
        .sort(([, a], [, b]) => a[0].distance_m - b[0].distance_m)
        .map(([label, entries]) => (
        <section key={label}>
          <h2>{label}</h2>
          <div className="card table-wrap" style={{ padding: 0 }}>
            <table style={{ tableLayout: 'fixed' }}>
              {/* Shared column widths so the stacked per-distance tables align. */}
              <colgroup>
                <col style={{ width: 44 }} />
                <col style={{ width: 96 }} />
                <col style={{ width: 120 }} />
                <col />
                <col style={{ width: 150 }} />
              </colgroup>
              <tbody>
                {entries.map((entry, i) => (
                  <tr key={`${entry.activity_id}-${i}`}>
                    <td>{['🥇', '🥈', '🥉'][i] ?? `${i + 1}.`}</td>
                    <td className="strong">{formatDuration(entry.duration_s)}</td>
                    <td>
                      {formatPaceFromSeconds(
                        (entry.duration_s / entry.distance_m) * paceUnitMeters()
                      )}{' '}
                      {paceUnitLabel()}
                    </td>
                    <td>
                      <Link to={`/activities/${entry.activity_id}`}>{entry.activity_name}</Link>
                    </td>
                    <td className="muted">{formatMediumDate(entry.start_time_local)}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </section>
      ))}
    </>
  )
}
