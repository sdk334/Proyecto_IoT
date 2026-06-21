const CONFIG = {
  temperatura: {
    label: 'Temperatura', unit: '°C', icon: '🌡️',
    min: 18, max: 26,
  },
  humedad: {
    label: 'Humedad', unit: '%', icon: '💧',
    min: 50, max: 70,
  },
  nivel_agua: {
    label: 'Nivel Agua', unit: 'cm', icon: '📏',
    min: 10, max: 30,
  },
}

function getStatus(cfg, value) {
  if (value === null) return { label: 'SIN DATOS', color: 'text-slate-400', dot: 'bg-slate-500' }
  if (value < cfg.min || value > cfg.max)
    return { label: 'FUERA DE RANGO', color: 'text-red-400', dot: 'bg-red-400' }
  if (value < cfg.min + 2 || value > cfg.max - 2)
    return { label: 'EN LÍMITE', color: 'text-amber-400', dot: 'bg-amber-400' }
  return { label: 'NORMAL', color: 'text-green-400', dot: 'bg-green-400' }
}

export default function SensorCard({ sensor, data }) {
  const cfg = CONFIG[sensor]
  const value = data ? parseFloat(data.valor) : null
  const status = getStatus(cfg, value)
  const ts = data?.timestamp
    ? new Date(data.timestamp).toLocaleTimeString('es-MX')
    : '—'

  return (
    <div className="bg-slate-800 rounded-2xl p-5 border border-slate-700 flex flex-col gap-2 hover:border-slate-500 transition-colors">
      <div className="flex items-center justify-between">
        <span className="text-2xl">{cfg.icon}</span>
        <div className="flex items-center gap-1.5">
          <span className={`w-1.5 h-1.5 rounded-full ${status.dot}`} />
          <span className={`text-xs font-mono ${status.color}`}>{status.label}</span>
        </div>
      </div>
      <p className="text-slate-400 text-sm">{cfg.label}</p>
      <p className={`text-4xl font-bold ${status.color}`}>
        {value !== null ? value.toFixed(1) : '—'}
        <span className="text-base font-normal text-slate-500 ml-1">{cfg.unit}</span>
      </p>
      <p className="text-slate-600 text-xs mt-auto">Última lectura: {ts}</p>
    </div>
  )
}
