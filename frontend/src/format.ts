/** Locale for all date/time rendering; undefined = browser default. Cached in
 * localStorage so the first paint already uses the saved preference; the
 * server-stored setting (athlete_settings.display_locale) is applied on load
 * and on save via setDisplayLocale. */
let displayLocale: string | undefined =
  (typeof localStorage !== 'undefined' && localStorage.getItem('fartlek-locale')) || undefined

export function setDisplayLocale(newLocale: string): void {
  displayLocale = newLocale || undefined
  try {
    localStorage.setItem('fartlek-locale', newLocale)
  } catch {
    /* private browsing — server setting still applies next load */
  }
}

/** Pass as the first argument of any toLocale*String call. */
export function locale(): string | undefined {
  return displayLocale
}

/** Display units (pace + distance); storage stays SI (m, m/s, s/km) everywhere.
 * Cached in localStorage like the locale; the server setting
 * (athlete_settings.units) is applied on load and on save via setUnits. */
export type Units = 'metric' | 'imperial'

const MILE_M = 1609.344

let unitsValue: Units =
  typeof localStorage !== 'undefined' && localStorage.getItem('fartlek-units') === 'imperial'
    ? 'imperial'
    : 'metric'

export function setUnits(units: Units): void {
  unitsValue = units
  try {
    localStorage.setItem('fartlek-units', units)
  } catch {
    /* private browsing — server setting still applies next load */
  }
}

export function units(): Units {
  return unitsValue
}

/** Suffix for pace values in the current unit. */
export function paceUnitLabel(): string {
  return unitsValue === 'imperial' ? '/mi' : '/km'
}

/** Meters per pace/distance unit — the single source of the mile constant. */
export function paceUnitMeters(): number {
  return unitsValue === 'imperial' ? MILE_M : 1000
}

/** Unit name for long distances ("km" | "mi") — chart axes, week totals. */
export function distanceUnitLabel(): string {
  return unitsValue === 'imperial' ? 'mi' : 'km'
}

/** Meters → the current long-distance unit (km or miles), as a number. */
export function metersToDistanceUnit(meters: number): number {
  return meters / paceUnitMeters()
}

/** Convert a stored s/km pace value to seconds per current display unit. */
export function secPerKmToDisplay(secPerKm: number): number {
  return secPerKm * (paceUnitMeters() / 1000)
}

export function formatDistance(meters: number): string {
  // Short distances stay in meters in both systems (track reps are metric).
  if (meters < 1000) return `${Math.round(meters)} m`
  const value = metersToDistanceUnit(meters)
  return `${value.toFixed(value >= 100 ? 0 : 2)} ${distanceUnitLabel()}`
}

export function formatDuration(seconds: number): string {
  const s = Math.round(seconds)
  const h = Math.floor(s / 3600)
  const m = Math.floor((s % 3600) / 60)
  const sec = s % 60
  if (h > 0) return `${h}:${String(m).padStart(2, '0')}:${String(sec).padStart(2, '0')}`
  return `${m}:${String(sec).padStart(2, '0')}`
}

/** Pace as min:sec per current display unit from speed in m/s, with suffix. */
export function formatPace(speedMps: number | null): string {
  const value = formatPaceValue(speedMps)
  return value === '–' ? value : `${value} ${paceUnitLabel()}`
}

/** Like formatPace but without the unit suffix (chart labels, tight tables). */
export function formatPaceValue(speedMps: number | null): string {
  if (!speedMps || speedMps <= 0.3) return '–'
  return formatPaceFromSeconds(paceUnitMeters() / speedMps)
}

/** Pure m:ss formatter — unit-agnostic; the caller owns the conversion.
 * Feed it s/km values through secPerKmToDisplay first when displaying pace. */
export function formatPaceFromSeconds(seconds: number): string {
  const m = Math.floor(seconds / 60)
  const s = Math.round(seconds % 60)
  if (s === 60) return `${m + 1}:00`
  return `${m}:${String(s).padStart(2, '0')}`
}

export function formatDate(iso: string): string {
  return new Date(iso).toLocaleDateString(locale(), {
    weekday: 'short',
    day: 'numeric',
    month: 'short',
    year: 'numeric'
  })
}

export function formatShortDate(iso: string): string {
  return new Date(iso).toLocaleDateString(locale(), { day: 'numeric', month: 'short' })
}

export function formatMediumDate(iso: string): string {
  return new Date(iso).toLocaleDateString(locale(), {
    day: 'numeric',
    month: 'short',
    year: 'numeric'
  })
}

export function formatTime(iso: string): string {
  return new Date(iso).toLocaleTimeString(locale(), { hour: '2-digit', minute: '2-digit' })
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
