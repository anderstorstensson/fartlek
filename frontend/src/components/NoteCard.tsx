import ReactMarkdown from 'react-markdown'
import { AnalysisNote, fetchJson } from '../api'
import { formatDate } from '../format'

const KIND_LABELS: Record<AnalysisNote['kind'], string> = {
  session: 'Session analysis',
  race: 'Race analysis',
  weekly: 'Weekly check-in',
  trend: 'Trend review',
  'plan-checkin': 'Plan check-in',
  other: 'Note'
}

interface NoteCardProps {
  note: AnalysisNote
  onDeleted?: (id: number) => void
}

export default function NoteCard({ note, onDeleted }: NoteCardProps) {
  const remove = () => {
    if (!window.confirm(`Delete "${note.title}"?`)) return
    fetchJson(`/api/notes/${note.id}`, { method: 'DELETE' })
      .then(() => onDeleted?.(note.id))
      .catch(() => undefined)
  }

  return (
    <div className="card note-card">
      <div className="note-head">
        <div>
          <span className="badge">{KIND_LABELS[note.kind]}</span>
          <strong style={{ marginLeft: 10 }}>{note.title}</strong>
        </div>
        <div className="muted" style={{ fontSize: 12, display: 'flex', gap: 12, alignItems: 'center' }}>
          {note.period_start && note.period_end && (
            <span>
              {note.period_start} → {note.period_end}
            </span>
          )}
          <span>{formatDate(note.created_at)}</span>
          {onDeleted && (
            <button className="ghost" style={{ padding: '3px 10px' }} onClick={remove}>
              Delete
            </button>
          )}
        </div>
      </div>
      <div className="markdown">
        <ReactMarkdown>{note.content}</ReactMarkdown>
      </div>
    </div>
  )
}
