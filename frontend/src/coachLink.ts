import { ActivityDetail } from './api'

/** Link to the Coach tab with a pre-filled (editable, not auto-sent) prompt. */
export function coachUrl(prompt: string): string {
  return `/coach?draft=${encodeURIComponent(prompt)}`
}

export function analyzePrompt(activity: ActivityDetail): string {
  const date = activity.start_time_local.slice(0, 10)
  const label = `"${activity.name}" (activity ${activity.id}, ${date})`
  if (activity.tag === 'race') {
    return `Do a full post-race analysis of my race ${label}.`
  }
  if (activity.is_workout || activity.tag === 'intervals' || activity.tag === 'tempo') {
    return `Analyze my workout ${label}.`
  }
  return `Analyze my session ${label}.`
}

export const TREND_PROMPT =
  'Review my long-term training trends: fitness and load trajectory (CTL/ATL/TSB), ' +
  'weekly volume, intensity distribution, and efficiency/decoupling. What is working, ' +
  'what is drifting, and what should change in the coming weeks?'

export const PLAN_PROMPT =
  'Build me a training plan. Start from my athlete profile, registered races and ' +
  'training data; confirm the goal and baseline with me before designing sessions, ' +
  'and show me the full plan for approval before publishing it to the calendar.'
