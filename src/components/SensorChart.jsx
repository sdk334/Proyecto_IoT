import {
  LineChart, Line, XAxis, YAxis, CartesianGrid,
  Tooltip, ResponsiveContainer, ReferenceLine,
} from 'recharts'

const CONFIG = {
  temperatura: { label: 'Temperatura (°C)', color: '#fb923c', min: 18, max: 26 },
  humedad:     { label: 'Humedad (%)',       color: '#38bdf8', min: 50, max: 70 },
  nivel_agua:  { label: 'Nivel Agua (cm)',   color: '#4ade80', min: 10, max: 30 },
}

export default function SensorChart({ sensor, data }) {
  const cfg = CONFIG[sensor]

  if (!data || data.length === 0) {
    return (
      <div className="bg-slate-800 rounded-2xl p-5 border border-slate-700">
        <p className="text-slate-400 text-sm mb-3">{cfg.label}</p>
        <div className="h-36 flex items-center justify-center text-slate-600 text-sm">
          Sin datos históricos aún
        </div>
      </div>
    )
  }

  return (
    <div className="bg-slate-800 rounded-2xl p-5 border border-slate-700">
      <p className="text-slate-400 text-sm mb-3">{cfg.label}</p>
      <ResponsiveContainer width="100%" height={140}>
        <LineChart data={data} margin={{ top: 4, right: 8, left: -24, bottom: 0 }}>
          <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" />
          <XAxis
            dataKey="time"
            tick={{ fill: '#475569', fontSize: 9 }}
            tickLine={false}
            interval="preserveStartEnd"
          />
          <YAxis
            tick={{ fill: '#475569', fontSize: 10 }}
            tickLine={false}
            axisLine={false}
          />
          <Tooltip
            contentStyle={{
              backgroundColor: '#1e293b',
              border: '1px solid #334155',
              borderRadius: '8px',
              color: '#f1f5f9',
              fontSize: '12px',
            }}
          />
          <ReferenceLine y={cfg.min} stroke="#ef4444" strokeDasharray="4 4" strokeOpacity={0.4} />
          <ReferenceLine y={cfg.max} stroke="#ef4444" strokeDasharray="4 4" strokeOpacity={0.4} />
          <Line
            type="monotone"
            dataKey="value"
            stroke={cfg.color}
            strokeWidth={2}
            dot={false}
            activeDot={{ r: 4, fill: cfg.color }}
          />
        </LineChart>
      </ResponsiveContainer>
    </div>
  )
}
