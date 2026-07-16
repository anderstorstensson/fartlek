import { useEffect, useState } from 'react'

export interface ActivitySummary {
  id: number
  name: string
  sport: string
  start_time_local: string
  elapsed_s: number
  moving_s: number
  distance_m: number
  avg_hr: number | null
  max_hr: number | null
  avg_speed_mps: number | null
  ascent_m: number | null
  trimp: number | null
  rtss: number | null
  hrtss: number | null
  has_gps: boolean
  is_workout: boolean
  tag: string | null
}

export interface Lap {
  lap_index: number
  start_offset_s: number
  elapsed_s: number
  distance_m: number
  avg_hr: number | null
  max_hr: number | null
  avg_speed_mps: number | null
  intensity: string | null
}

export interface BestEffortItem {
  label: string
  distance_m: number
  duration_s: number
}

export interface ActivityDetail extends ActivitySummary {
  max_speed_mps: number | null
  descent_m: number | null
  calories: number | null
  avg_cadence: number | null
  has_fit: boolean
  avg_power_w: number | null
  avg_vertical_oscillation_mm: number | null
  avg_vertical_ratio_pct: number | null
  avg_step_length_mm: number | null
  avg_stance_time_ms: number | null
  avg_respiration_brpm: number | null
  gap_speed_mps: number | null
  decoupling_pct: number | null
  efficiency_index: number | null
  weather_temp_c: number | null
  weather_humidity_pct: number | null
  weather_wind_mps: number | null
  weather_code: number | null
  user_note: string
  laps: Lap[]
  best_efforts: BestEffortItem[]
}

export interface ActivityList {
  items: ActivitySummary[]
  total: number
}

export interface Zone {
  name: string
  low_bpm: number
  high_bpm: number | null
}

export interface Streams {
  time_s: (number | null)[]
  distance_m: (number | null)[]
  hr: (number | null)[]
  speed_mps: (number | null)[]
  gap_speed_mps: (number | null)[]
  altitude_m: (number | null)[]
  cadence: (number | null)[]
  lat: (number | null)[]
  lng: (number | null)[]
  power: (number | null)[]
  vertical_oscillation: (number | null)[]
  vertical_ratio: (number | null)[]
  step_length: (number | null)[]
  stance_time: (number | null)[]
  respiration: (number | null)[]
  zones: Zone[]
  time_in_zones_s: number[]
  pace_zones: PaceZone[]
  time_in_pace_zones_s: number[]
}

export interface PaceZone {
  name: string
  low_speed_mps: number
  high_speed_mps: number | null
}

export interface FitnessPoint {
  day: string
  load: number
  ctl: number
  atl: number
  tsb: number
  projected: boolean
}

export interface WeeklyZones {
  week_start: string
  zone_seconds: number[]
  total_s: number
}

export interface EfficiencyPoint {
  day: string
  activity_id: number
  name: string
  efficiency_index: number | null
  decoupling_pct: number | null
  distance_m: number
  moving_s: number
  is_workout: boolean
}

export interface WellnessDay {
  day: string
  resting_hr: number | null
  hrv_last_night_avg: number | null
  hrv_status: string | null
  sleep_s: number | null
  deep_sleep_s: number | null
  sleep_score: number | null
  body_battery_max: number | null
  body_battery_min: number | null
  stress_avg: number | null
  steps: number | null
}

export interface Readiness {
  day: string
  resting_hr: number | null
  resting_hr_baseline: number | null
  hrv_last_night_avg: number | null
  hrv_baseline: number | null
  sleep_score: number | null
  sleep_s: number | null
  body_battery_max: number | null
  stress_avg: number | null
  flags: string[]
  status: 'ready' | 'caution' | 'rest'
}

export interface Race {
  id: number
  name: string
  day: string
  distance_m: number
  target_time_s: number | null
  priority: 'A' | 'B' | 'C'
  notes: string
  days_until: number | null
  predicted_time_s: number | null
  predicted_from: string | null
}

export interface WeeklyStat {
  week_start: string
  run_distance_m: number
  total_moving_s: number
  load_trimp: number
  load_rtss: number
  activities: number
  runs: number
  ascent_m: number
}

export interface RecordEntry {
  label: string
  distance_m: number
  duration_s: number
  activity_id: number
  activity_name: string
  start_time_local: string
}

export interface WeekSummary {
  run_distance_m: number
  total_moving_s: number
  load_trimp: number
  activities: number
  runs: number
}

export interface FormSnapshot {
  ctl: number
  atl: number
  tsb: number
}

export interface StatsSummary {
  this_week: WeekSummary
  last_week: WeekSummary
  form_trimp: FormSnapshot
  form_rtss: FormSnapshot
  total_activities: number
}

export interface Settings {
  resting_hr: number
  max_hr: number
  lthr: number
  threshold_pace_s_per_km: number
  sex: string
  zone_mode: 'max_hr' | 'lthr' | 'manual'
  manual_zone_bounds: number[] | null
  rtss_use_gap: boolean
  pace_zone_mode: 'threshold' | 'manual'
  manual_pace_zone_bounds: number[] | null
  coaching_tone: 'harsh' | 'balanced' | 'supportive'
  zones: Zone[]
  pace_zones: PaceZone[]
}

export interface PlannedWorkout {
  id: number
  day: string
  title: string
  workout_type: string
  description: string
  target_distance_m: number | null
  target_duration_s: number | null
  plan_name: string
  completed_activity_id: number | null
}

export interface PlanInfo {
  plan_name: string
  workouts: number
  first_day: string
  last_day: string
}

export interface AnalysisNote {
  id: number
  activity_id: number | null
  kind: 'session' | 'race' | 'weekly' | 'trend' | 'plan-checkin' | 'other'
  title: string
  content: string
  period_start: string | null
  period_end: string | null
  created_at: string
  updated_at: string
}

export interface SyncStatus {
  status: string
  message: string
  last_sync_at: string | null
  logged_in: boolean
  total_activities: number
}

export interface CoachMessage {
  id: number
  role: string
  content: string
  created_at: string
}

export interface CoachStatus {
  enabled: boolean
  cli_available: boolean
}

export type LoadModel = 'trimp' | 'rtss'

export async function fetchJson<T>(url: string, init?: RequestInit): Promise<T> {
  const response = await fetch(url, init)
  if (!response.ok) {
    throw new Error(`${response.status} ${response.statusText}`)
  }
  return response.json() as Promise<T>
}

export function useApi<T>(url: string | null): {
  data: T | null
  error: string | null
  loading: boolean
} {
  const [data, setData] = useState<T | null>(null)
  const [error, setError] = useState<string | null>(null)
  const [loading, setLoading] = useState(url !== null)

  useEffect(() => {
    if (url === null) return
    let cancelled = false
    setLoading(true)
    setError(null)
    fetchJson<T>(url)
      .then((result) => {
        if (!cancelled) setData(result)
      })
      .catch((err: Error) => {
        if (!cancelled) setError(err.message)
      })
      .finally(() => {
        if (!cancelled) setLoading(false)
      })
    return () => {
      cancelled = true
    }
  }, [url])

  return { data, error, loading }
}
