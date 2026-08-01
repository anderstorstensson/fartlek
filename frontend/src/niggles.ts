import { Niggle } from './api'

/** Anatomical sites, mirroring backend/schemas.py NIGGLE_SITES. These are body
 *  locations, not diagnoses — the coach recognises patterns and manages load, it
 *  does not diagnose (docs/coach/physio-guidance.md §1). Keep in sync with the
 *  backend: it rejects anything outside this vocabulary with a 422. */
export const SITES: { value: string; label: string }[] = [
  { value: 'achilles', label: 'Achilles' },
  { value: 'calf', label: 'Calf' },
  { value: 'shin', label: 'Shin' },
  { value: 'knee_anterior', label: 'Knee — front' },
  { value: 'knee_lateral', label: 'Knee — outside' },
  { value: 'knee_other', label: 'Knee — other' },
  { value: 'hamstring', label: 'Hamstring' },
  { value: 'quad', label: 'Quad' },
  { value: 'hip', label: 'Hip' },
  { value: 'glute', label: 'Glute' },
  { value: 'groin', label: 'Groin' },
  { value: 'ankle', label: 'Ankle' },
  { value: 'foot_plantar', label: 'Foot — sole/heel' },
  { value: 'foot_other', label: 'Foot — other' },
  { value: 'back', label: 'Back' },
  { value: 'other', label: 'Other' }
]

export const TIERS: Record<number, { label: string; option: string }> = {
  1: { label: 'Niggle', option: 'Niggle — modify and monitor' },
  2: { label: 'Injury', option: 'Injury — restructure the plan' },
  3: { label: 'Referred', option: 'Referred — clinician, not training' }
}

export const SIDES: { value: string; label: string }[] = [
  { value: 'na', label: 'n/a' },
  { value: 'left', label: 'Left' },
  { value: 'right', label: 'Right' },
  { value: 'both', label: 'Both' }
]

export const siteLabel = (value: string) =>
  SITES.find((s) => s.value === value)?.label ?? value

export const sideLabel = (side: string) =>
  side === 'left' ? 'L' : side === 'right' ? 'R' : side === 'both' ? 'both' : ''

/** Local calendar day as YYYY-MM-DD (not UTC — an evening run must not log as tomorrow). */
export const isoDay = (value?: string) => {
  const d = value ? new Date(value) : new Date()
  return `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, '0')}-${String(
    d.getDate()
  ).padStart(2, '0')}`
}

/** PUT is a full replace (NiggleIn), so every writable field goes back. */
export const writable = (n: Niggle) => ({
  site: n.site,
  side: n.side,
  onset_date: n.onset_date,
  onset_activity_id: n.onset_activity_id,
  tier: n.tier,
  trigger: n.trigger,
  response: n.response,
  resolved_date: n.resolved_date,
  note: n.note
})

/** "Achilles · R" — the compact label used wherever an episode is named. */
export const describe = (n: Niggle) => {
  const side = sideLabel(n.side)
  return side ? `${siteLabel(n.site)} · ${side}` : siteLabel(n.site)
}
