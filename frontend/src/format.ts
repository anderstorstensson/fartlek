export function formatDistance(meters: number): string {
  if (meters >= 1000) return `${(meters / 1000).toFixed(meters >= 100000 ? 0 : 2)} km`
  return `${Math.round(meters)} m`
}

export function formatDuration(seconds: number): string {
  const s = Math.round(seconds)
  const h = Math.floor(s / 3600)
  const m = Math.floor((s % 3600) / 60)
  const sec = s % 60
  if (h > 0) return `${h}:${String(m).padStart(2, '0')}:${String(sec).padStart(2, '0')}`
  return `${m}:${String(sec).padStart(2, '0')}`
}

/** Pace as min:sec per km from speed in m/s. */
export function formatPace(speedMps: number | null): string {
  if (!speedMps || speedMps <= 0.3) return '–'
  const secPerKm = 1000 / speedMps
  const m = Math.floor(secPerKm / 60)
  const s = Math.round(secPerKm % 60)
  if (s === 60) return `${m + 1}:00 /km`
  return `${m}:${String(s).padStart(2, '0')} /km`
}

export function formatPaceFromSeconds(secPerKm: number): string {
  const m = Math.floor(secPerKm / 60)
  const s = Math.round(secPerKm % 60)
  return `${m}:${String(s).padStart(2, '0')}`
}

export function formatDate(iso: string): string {
  return new Date(iso).toLocaleDateString(undefined, {
    weekday: 'short',
    day: 'numeric',
    month: 'short',
    year: 'numeric'
  })
}

export function formatShortDate(iso: string): string {
  return new Date(iso).toLocaleDateString(undefined, { day: 'numeric', month: 'short' })
}

export function formatTime(iso: string): string {
  return new Date(iso).toLocaleTimeString(undefined, { hour: '2-digit', minute: '2-digit' })
}

export function formatSportName(sport: string): string {
  return sport.replace(/_/g, ' ').replace(/^\w/, (c) => c.toUpperCase())
}

export function sportEmoji(sport: string): string {
  if (sport.includes('running')) return '🏃'
  if (sport.includes('cycling') || sport.includes('biking')) return '🚴'
  if (sport.includes('swim')) return '🏊'
  if (sport.includes('strength') || sport.includes('training')) return '🏋️'
  if (sport.includes('walk') || sport.includes('hik')) return '🚶'
  if (sport.includes('ski')) return '⛷️'
  return '🏅'
}
