interface StatCardProps {
  label: string
  value: string
  delta?: string
  deltaGood?: boolean
}

export default function StatCard({ label, value, delta, deltaGood }: StatCardProps) {
  return (
    <div className="card stat-tile">
      <div className="label">{label}</div>
      <div className="value">{value}</div>
      {delta !== undefined && <div className={`delta${deltaGood ? ' up' : ''}`}>{delta}</div>}
    </div>
  )
}
