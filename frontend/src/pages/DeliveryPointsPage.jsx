import { useEffect, useState } from 'react'
import { api } from '../api/client.js'

const DISTRITOS = ['EL TAMBO', 'HUANCAYO', 'CHILCA']

const EMPTY_FORM = {
  nombre: '',
  direccion: '',
  latitud: '',
  longitud: '',
  distrito: 'EL TAMBO',
}

function formatNumber(value) {
  return typeof value === 'number' ? value.toFixed(6) : value
}

function DeliveryPointsPage() {
  const [points, setPoints] = useState([])
  const [form, setForm] = useState(EMPTY_FORM)
  const [editingId, setEditingId] = useState(null)
  const [filter, setFilter] = useState('')
  const [error, setError] = useState('')
  const [success, setSuccess] = useState('')

  async function load(filterValue = filter) {
    try {
      const data = await api.listDeliveryPoints(filterValue || undefined)
      setPoints(data)
    } catch (err) {
      setError(err.message)
      setPoints([])
    }
  }

  useEffect(() => {
    load()
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [])

  function setField(field, value) {
    setForm((prev) => ({ ...prev, [field]: value }))
  }

  function validate() {
    const latitud = Number(form.latitud)
    const longitud = Number(form.longitud)
    if (!form.nombre.trim() || !form.direccion.trim()) {
      return 'Todos los campos son obligatorios.'
    }
    if (!DISTRITOS.includes(form.distrito.toUpperCase())) {
      return 'El distrito debe ser El Tambo, Huancayo o Chilca.'
    }
    if (Number.isNaN(latitud) || latitud < -90 || latitud > 90) {
      return 'La latitud debe estar entre -90 y 90.'
    }
    if (Number.isNaN(longitud) || longitud < -180 || longitud > 180) {
      return 'La longitud debe estar entre -180 y 180.'
    }
    return ''
  }

  async function handleSubmit(event) {
    event.preventDefault()
    setSuccess('')
    setError('')
    const validationError = validate()
    if (validationError) {
      setError(validationError)
      return
    }
    const payload = {
      nombre: form.nombre.trim(),
      direccion: form.direccion.trim(),
      latitud: Number(form.latitud),
      longitud: Number(form.longitud),
      distrito: form.distrito.toUpperCase(),
    }
    try {
      if (editingId) {
        await api.updateDeliveryPoint(editingId, payload)
        setSuccess('Punto de entrega actualizado correctamente.')
        setEditingId(null)
      } else {
        await api.createDeliveryPoint(payload)
        setSuccess('Punto de entrega registrado correctamente.')
      }
      setForm(EMPTY_FORM)
      await load()
    } catch (err) {
      setError(err.message)
    }
  }

  function startEdit(point) {
    setEditingId(point.punto_id)
    setError('')
    setSuccess('')
    setForm({
      nombre: point.nombre,
      direccion: point.direccion,
      latitud: formatNumber(point.latitud),
      longitud: formatNumber(point.longitud),
      distrito: point.distrito,
    })
  }

  function cancelEdit() {
    setEditingId(null)
    setForm(EMPTY_FORM)
    setError('')
    setSuccess('')
  }

  async function handleDeactivate(point) {
    setError('')
    setSuccess('')
    if (!window.confirm(`¿Desactivar el punto "${point.nombre}"?`)) {
      return
    }
    try {
      await api.deactivateDeliveryPoint(point.punto_id)
      setSuccess('Punto de entrega desactivado. Ya no aparece en la planificación de rutas.')
      await load()
    } catch (err) {
      setError(err.message)
    }
  }

  async function handleFilterChange(value) {
    setFilter(value)
    await load(value)
  }

  return (
    <section>
      <h2>Puntos de entrega</h2>
      <p>
        Ámbito geográfico: <strong>El Tambo, Huancayo y Chilca</strong>.
      </p>

      {error && <div className="alert error">{error}</div>}
      {success && <div className="alert success">{success}</div>}

      <form className="card" onSubmit={handleSubmit}>
        <h3>{editingId ? 'Editar punto de entrega' : 'Registrar punto de entrega'}</h3>
        <div className="row">
          <label>
            Nombre
            <input
              type="text"
              value={form.nombre}
              onChange={(event) => setField('nombre', event.target.value)}
              placeholder="Nombre del establecimiento"
            />
          </label>
          <label>
            Dirección
            <input
              type="text"
              value={form.direccion}
              onChange={(event) => setField('direccion', event.target.value)}
              placeholder="Dirección del punto"
            />
          </label>
        </div>
        <div className="row">
          <label>
            Latitud
            <input
              type="number"
              step="any"
              value={form.latitud}
              onChange={(event) => setField('latitud', event.target.value)}
              placeholder="-12.0667"
            />
          </label>
          <label>
            Longitud
            <input
              type="number"
              step="any"
              value={form.longitud}
              onChange={(event) => setField('longitud', event.target.value)}
              placeholder="-75.2260"
            />
          </label>
          <label>
            Distrito
            <select
              value={form.distrito}
              onChange={(event) => setField('distrito', event.target.value)}
            >
              {DISTRITOS.map((distrito) => (
                <option key={distrito} value={distrito}>
                  {distrito}
                </option>
              ))}
            </select>
          </label>
        </div>
        <div className="actions">
          {editingId && (
            <button type="button" className="secondary" onClick={cancelEdit}>
              Cancelar
            </button>
          )}
          <button type="submit">{editingId ? 'Guardar cambios' : 'Registrar'}</button>
        </div>
      </form>

      <div className="card">
        <div className="list-header">
          <h3>Listado</h3>
          <label>
            Filtrar por distrito
            <select value={filter} onChange={(event) => handleFilterChange(event.target.value)}>
              <option value="">Todos</option>
              {DISTRITOS.map((distrito) => (
                <option key={distrito} value={distrito}>
                  {distrito}
                </option>
              ))}
            </select>
          </label>
        </div>
        {points.length === 0 ? (
          <p className="empty">No hay puntos de entrega registrados.</p>
        ) : (
          <table>
            <thead>
              <tr>
                <th>Nombre</th>
                <th>Dirección</th>
                <th>Latitud</th>
                <th>Longitud</th>
                <th>Distrito</th>
                <th>Acciones</th>
              </tr>
            </thead>
            <tbody>
              {points.map((point) => (
                <tr key={point.punto_id}>
                  <td>{point.nombre}</td>
                  <td>{point.direccion}</td>
                  <td>{formatNumber(point.latitud)}</td>
                  <td>{formatNumber(point.longitud)}</td>
                  <td>{point.distrito}</td>
                  <td className="actions">
                    <button type="button" className="secondary" onClick={() => startEdit(point)}>
                      Editar
                    </button>
                    <button type="button" className="danger" onClick={() => handleDeactivate(point)}>
                      Desactivar
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>
    </section>
  )
}

export default DeliveryPointsPage