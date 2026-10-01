const BASE_URL = '/api/v1'

async function request(path, options = {}) {
  const res = await fetch(`${BASE_URL}${path}`, {
    headers: { 'Content-Type': 'application/json' },
    ...options,
  })
  const data = await res.json().catch(() => null)
  if (!res.ok) {
    const detail = data?.detail
    const message = Array.isArray(detail)
      ? detail.map((item) => item.msg).join('; ')
      : detail || 'Ocurrió un error inesperado'
    throw new Error(message)
  }
  return data
}

export const api = {
  listDeliveryPoints(distrito) {
    const query = distrito ? `?distrito=${encodeURIComponent(distrito)}` : ''
    return request(`/delivery-points${query}`)
  },
  createDeliveryPoint(payload) {
    return request('/delivery-points', { method: 'POST', body: JSON.stringify(payload) })
  },
  updateDeliveryPoint(id, payload) {
    return request(`/delivery-points/${id}`, { method: 'PUT', body: JSON.stringify(payload) })
  },
  deactivateDeliveryPoint(id) {
    return request(`/delivery-points/${id}`, { method: 'DELETE' })
  },
  optimizeRoute(payload) {
    return request('/routes/optimize', { method: 'POST', body: JSON.stringify(payload) })
  },
}