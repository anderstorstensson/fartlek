import { LatLngBoundsExpression } from 'leaflet'
import { MapContainer, Polyline, TileLayer } from 'react-leaflet'
import { Streams } from '../api'

interface ActivityMapProps {
  streams: Streams
}

export default function ActivityMap({ streams }: ActivityMapProps) {
  const points: [number, number][] = []
  for (let i = 0; i < streams.lat.length; i++) {
    const lat = streams.lat[i]
    const lng = streams.lng[i]
    if (lat !== null && lng !== null) points.push([lat, lng])
  }
  if (points.length < 2) return null

  const lats = points.map((p) => p[0])
  const lngs = points.map((p) => p[1])
  const bounds: LatLngBoundsExpression = [
    [Math.min(...lats), Math.min(...lngs)],
    [Math.max(...lats), Math.max(...lngs)]
  ]

  return (
    <div className="map-card">
      <MapContainer bounds={bounds} boundsOptions={{ padding: [24, 24] }} scrollWheelZoom={false}>
        <TileLayer
          attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
          url="https://tile.openstreetmap.org/{z}/{x}/{y}.png"
        />
        <Polyline positions={points} pathOptions={{ color: '#3987e5', weight: 3 }} />
      </MapContainer>
    </div>
  )
}
