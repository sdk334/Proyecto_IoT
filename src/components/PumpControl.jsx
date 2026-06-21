export default function PumpControl({ pump, onToggle }) {
  const isOn = pump?.valor === 'ON'
  const ts = pump?.timestamp
    ? new Date(pump.timestamp).toLocaleTimeString('es-MX')
    : '—'

  return (
    <div className={`rounded-2xl p-5 border flex flex-col gap-2 transition-colors ${
      isOn
        ? 'bg-green-950/50 border-green-600/60'
        : 'bg-slate-800 border-slate-700'
    }`}>
      <div className="flex items-center justify-between">
        <span className="text-2xl">⚡</span>
        <span className={`text-xs font-semibold px-2 py-0.5 rounded-full ${
          isOn
            ? 'bg-green-500/20 text-green-400'
            : 'bg-slate-700 text-slate-400'
        }`}>
          {isOn ? 'ACTIVA' : 'INACTIVA'}
        </span>
      </div>
      <p className="text-slate-400 text-sm">Bomba de Agua</p>
      <p className={`text-4xl font-bold ${isOn ? 'text-green-400' : 'text-slate-400'}`}>
        {pump ? (isOn ? 'ON' : 'OFF') : '—'}
      </p>

      <div className="flex gap-2 mt-2">
        <button
          onClick={() => onToggle('ON')}
          disabled={isOn}
          className="flex-1 py-2 rounded-xl font-semibold text-sm transition-all
            bg-green-600 hover:bg-green-500 active:bg-green-700
            disabled:opacity-30 disabled:cursor-not-allowed text-white"
        >
          Encender
        </button>
        <button
          onClick={() => onToggle('OFF')}
          disabled={!isOn}
          className="flex-1 py-2 rounded-xl font-semibold text-sm transition-all
            bg-slate-600 hover:bg-slate-500 active:bg-slate-700
            disabled:opacity-30 disabled:cursor-not-allowed text-white"
        >
          Apagar
        </button>
      </div>

      <p className="text-slate-600 text-xs mt-auto">Último cambio: {ts}</p>
    </div>
  )
}
