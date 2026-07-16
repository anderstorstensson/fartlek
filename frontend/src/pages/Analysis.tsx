import { useMemo, useState } from 'react'
import { AnalysisNote, useApi } from '../api'
import NoteCard from '../components/NoteCard'

const FILTERS = [
  { key: '', label: 'All' },
  { key: 'session', label: 'Sessions' },
  { key: 'race', label: 'Races' },
  { key: 'weekly', label: 'Weekly' },
  { key: 'trend', label: 'Trends' },
  { key: 'plan-checkin', label: 'Plan check-ins' }
]

export default function Analysis() {
  const [kind, setKind] = useState('')
  const [deleted, setDeleted] = useState<number[]>([])
  const url = useMemo(
    () => `/api/notes?limit=100${kind ? `&kind=${kind}` : ''}`,
    [kind]
  )
  const notes = useApi<AnalysisNote[]>(url)

  const visible = (notes.data ?? []).filter((n) => !deleted.includes(n.id))

  return (
    <>
      <h1>Analysis</h1>
      <div className="toolbar">
        <span className="segmented">
          {FILTERS.map((filter) => (
            <button
              key={filter.key}
              className={kind === filter.key ? 'on' : ''}
              onClick={() => setKind(filter.key)}
            >
              {filter.label}
            </button>
          ))}
        </span>
      </div>
      {notes.error && <div className="error-box">{notes.error}</div>}
      {visible.map((note) => (
        <NoteCard
          key={note.id}
          note={note}
          onDeleted={(id) => setDeleted((current) => [...current, id])}
        />
      ))}
      {notes.data && visible.length === 0 && (
        <div className="empty-state">
          No saved analyses yet. Ask Claude Code to analyze a workout or your training —
          it saves its findings here.
        </div>
      )}
    </>
  )
}
