import { useEffect, useState } from 'react'
import { api } from '../api/client.js'

function RouteOptimizationPage() {
  const [points, setPoints] = useState([])
  const [selected, setSelected] = useState([])
  const [originLat, setOriginLat] = useState('-12.0650')
  const [originLng, setOriginLng] = useState('-75.2050')
  const [result, setResult] = useState(null)
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)

  useEffect(() => {
    api
      .listDeliveryPoints()
      .then(setPoints)
      .catch((err) => setError(err.message))
  }, [])

  function togglePoint(pointId) {
    setSelected((prev) =>
      prev.includes(pointId) ? prev.filter((id) => id !== pointId) : [...prev, pointId],
    )
  }

  async function handleOptimize(event) {
    event.preventDefault()
    setError('')
    setResult(null)
    const lat = Number(originLat)
    const lng = Number(originLng)
    if (Number.isNaN(lat) || lat < -90 || lat > 90) {
      setError('La latitud del origen debe estar entre -90 y 90.')
      return
    }
    if (Number.isNaN(lng) || lng < -180 || lng > 180) {
      setError('La longitud del origen debe estar entre -180 y 180.')
      return
    }
    if (selected.length === 0) {
      setError('Seleccione al menos un destino habilitado.')
      return
    }
    setLoading(true)
    try {
      const data = await api.optimizeRoute({
        origin: { lat, lng },
        delivery_point_ids: selected,
      })
      setResult(data)
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  return (
    <section>
      <h2>Optimización de rutas</h2>
      <p>
        Genere una ruta sostenible seleccionando los puntos de entrega habilitados e indicando el
        origen. La ruta minimiza la distancia recorrida y estima las emisiones de CO₂.
      </p>

      {error && <div className="alert error">{error}</div>}

      <form className="card" onSubmit={handleOptimize}>
        <h3>Parámetros</h3>
        <div className="row">
          <label>
            Latitud del origen
            <input
              type="number"
              step="any"
              value={originLat}
              onChange={(event) => setOriginLat(event.target.value)}
            />
          </label>
          <label>
            Longitud del origen
            <input
              type="number"
              step="any"
              value={originLng}
              onChange={(event) => setOriginLng(event.target.value)}
            />
          </label>
        </div>
        <h4>Destinos (solo puntos habilitados)</h4>
        {points.length === 0 ? (
          <p className="empty">
            No hay puntos de entrega habilitados. Regístrelos en la vista de puntos de entrega.
          </p>
        ) : (
          <ul className="destinations">
            {points.map((point) => (
              <li key={point.punto_id}>
                <label>
                  <input
                    type="checkbox"
                    checked={selected.includes(point.punto_id)}
                    onChange={() => togglePoint(point.punto_id)}
                  />
                  {point.nombre} <span className="muted">({point.distrito})</span>
                </label>
              </li>
            ))}
          </ul>
        )}
        <div className="actions">
          <button type="submit" disabled={loading}>
            {loading ? 'Optimizando…' : 'Generar ruta'}
          </button>
        </div>
      </form>

      {result && (
        <div className="card">
          <h3>Ruta generada</h3>
          <div className="summary">
            <div>
              <strong>Distancia total: </strong>
              {result.total_distance_km} km
            </div>
            <div>
              <strong>Emisiones de CO₂: </strong>
              {result.co2_emissions_kg} kg
            </div>
          </div>
          <h4>Orden de visita</h4>
          <ol>
            {result.order.map((point, index) => (
              <li key={point.punto_id}>
                <strong>{index + 1}.</strong> {point.nombre} — {point.direccion} (
                {point.distrito})
              </li>
            ))}
          </ol>
        </div>
      )}
    </section>
  )
}

export default RouteOptimizationPage