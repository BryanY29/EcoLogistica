import { useState } from 'react'
import DeliveryPointsPage from './pages/DeliveryPointsPage.jsx'
import RouteOptimizationPage from './pages/RouteOptimizationPage.jsx'

function App() {
  const [view, setView] = useState('delivery-points')

  return (
    <div className="app">
      <header>
        <h1>EcoLogística</h1>
        <nav>
          <button
            className={view === 'delivery-points' ? 'active' : ''}
            onClick={() => setView('delivery-points')}
          >
            Puntos de entrega
          </button>
          <button
            className={view === 'routes' ? 'active' : ''}
            onClick={() => setView('routes')}
          >
            Optimización de rutas
          </button>
        </nav>
      </header>
      <main>
        {view === 'delivery-points' ? <DeliveryPointsPage /> : <RouteOptimizationPage />}
      </main>
    </div>
  )
}

export default App