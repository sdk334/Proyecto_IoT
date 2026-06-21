import { useSensors } from './hooks/useSensors'
import SensorCard from './components/SensorCard'
import PumpControl from './components/PumpControl'
import SensorChart from './components/SensorChart'

export default function App() {
  const { sensors, pump, history, connected, setPumpState } = useSensors()

  return (
    <div className="min-h-screen bg-slate-900 text-slate-100 p-6 max-w-6xl mx-auto">

      {/* Header */}
      <header className="flex items-center justify-between mb-8">
        <div>
          <h1 className="text-2xl font-bold text-white">🌿 Hidroponía IoT</h1>
          <p className="text-slate-500 text-sm">Sistema de monitoreo y control · ESCOM</p>
        </div>
        <div className="flex items-center gap-2 bg-slate-800 rounded-full px-3 py-1.5 border border-slate-700">
          <span className={`w-2 h-2 rounded-full ${connected ? 'bg-green-400 animate-pulse' : 'bg-red-400'}`} />
          <span className="text-sm text-slate-300">
            {connected ? 'Firebase conectado' : 'Conectando…'}
          </span>
        </div>
      </header>

      {/* Cards: 3 sensores + bomba */}
      <section className="grid grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
        <SensorCard sensor="temperatura" data={sensors.temperatura} />
        <SensorCard sensor="humedad"     data={sensors.humedad} />
        <SensorCard sensor="nivel_agua"  data={sensors.nivel_agua} />
        <PumpControl pump={pump} onToggle={setPumpState} />
      </section>

      {/* Gráficas historial */}
      <section>
        <h2 className="text-slate-500 text-xs font-semibold uppercase tracking-widest mb-4">
          Historial — últimas 20 lecturas
        </h2>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <SensorChart sensor="temperatura" data={history.temperatura} />
          <SensorChart sensor="humedad"     data={history.humedad} />
          <SensorChart sensor="nivel_agua"  data={history.nivel_agua} />
        </div>
      </section>

      {/* Footer */}
      <footer className="mt-10 text-center text-slate-700 text-xs">
        ESP32 → MQTT (Mosquitto) → bridge.py → Firebase → Dashboard
      </footer>
    </div>
  )
}
