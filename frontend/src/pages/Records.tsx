import { Link } from 'react-router-dom'
import { RecordEntry, useApi } from '../api'
import { formatDuration, formatPaceFromSeconds, formatShortDate, paceUnitLabel, paceUnitMeters } from '../format'

export default function Records() {
  const records = useApi<RecordEntry[]>('/api/records?top=3')

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
      {[...grouped.entries()].map(([label, entries]) => (
        <section key={label}>
          <h2>{label}</h2>
          <div className="card table-wrap" style={{ padding: 0 }}>
            <table>
              <tbody>
                {entries.map((entry, i) => (
                  <tr key={`${entry.activity_id}-${i}`}>
                    <td style={{ width: 40 }}>{['🥇', '🥈', '🥉'][i] ?? `${i + 1}.`}</td>
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
                    <td className="muted">{formatShortDate(entry.start_time_local)}</td>
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
