import { useApi } from '../api'

const WIDTH = 88
const HEIGHT = 56
const PAD = 5

interface RouteThumbProps {
  activityId: number
  hasGps: boolean
}

export default function RouteThumb({ activityId, hasGps }: RouteThumbProps) {
  const track = useApi<number[][]>(hasGps ? `/api/activities/${activityId}/track` : null)

  if (!hasGps || !track.data || track.data.length < 2) {
    return <div className="route-thumb empty" />
  }

  const lats = track.data.map((p) => p[0])
  const lngs = track.data.map((p) => p[1])
  const minLat = Math.min(...lats)
  const maxLat = Math.max(...lats)
  const minLng = Math.min(...lngs)
  const maxLng = Math.max(...lngs)

  // Equirectangular projection: shrink longitude by cos(latitude) so the
  // route keeps its real-world proportions.
  const lngScale = Math.cos(((minLat + maxLat) / 2) * (Math.PI / 180))
  const spanX = Math.max((maxLng - minLng) * lngScale, 1e-6)
  const spanY = Math.max(maxLat - minLat, 1e-6)
  const scale = Math.min((WIDTH - 2 * PAD) / spanX, (HEIGHT - 2 * PAD) / spanY)
  const offsetX = (WIDTH - spanX * scale) / 2
  const offsetY = (HEIGHT - spanY * scale) / 2

  const path = track.data
    .map((p, i) => {
      const x = offsetX + (p[1] - minLng) * lngScale * scale
      const y = offsetY + (maxLat - p[0]) * scale
      return `${i === 0 ? 'M' : 'L'}${x.toFixed(1)},${y.toFixed(1)}`
    })
    .join(' ')

  return (
    <div className="route-thumb">
      <svg width={WIDTH} height={HEIGHT} viewBox={`0 0 ${WIDTH} ${HEIGHT}`} aria-hidden="true">
        <path
          d={path}
          fill="none"
          stroke="var(--series-fitness)"
          strokeWidth={1.8}
          strokeLinejoin="round"
          strokeLinecap="round"
        />
      </svg>
    </div>
  )
}
