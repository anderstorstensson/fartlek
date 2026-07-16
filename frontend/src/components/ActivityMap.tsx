import { LatLngBoundsExpression } from 'leaflet'
import { useMemo } from 'react'
import { CircleMarker, MapContainer, Polyline, TileLayer } from 'react-leaflet'
import { Streams } from '../api'

interface ActivityMapProps {
  streams: Streams
  /** Position to highlight (chart hover), or null for no marker. */
  hoverPoint?: [number, number] | null
}

export default function ActivityMap({ streams, hoverPoint = null }: ActivityMapProps) {
  // Memoized so hover re-renders don't force Leaflet to re-draw the track.
  const { points, bounds } = useMemo(() => {
    const pts: [number, number][] = []
    for (let i = 0; i < streams.lat.length; i++) {
      const lat = streams.lat[i]
      const lng = streams.lng[i]
      if (lat !== null && lng !== null) pts.push([lat, lng])
    }
    if (pts.length < 2) return { points: pts, bounds: null }
    const lats = pts.map((p) => p[0])
    const lngs = pts.map((p) => p[1])
    const box: LatLngBoundsExpression = [
      [Math.min(...lats), Math.min(...lngs)],
      [Math.max(...lats), Math.max(...lngs)]
    ]
    return { points: pts, bounds: box }
  }, [streams])

  if (bounds === null) return null

  return (
    <div className="map-card">
      <MapContainer bounds={bounds} boundsOptions={{ padding: [24, 24] }} scrollWheelZoom={false}>
        <TileLayer
          attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
          url="https://tile.openstreetmap.org/{z}/{x}/{y}.png"
        />
        <Polyline positions={points} pathOptions={{ color: '#3987e5', weight: 3 }} />
        {hoverPoint && (
          <CircleMarker
            center={hoverPoint}
            radius={7}
            pathOptions={{ color: '#ffffff', weight: 2, fillColor: '#d95926', fillOpacity: 1 }}
          />
        )}
      </MapContainer>
    </div>
  )
}
