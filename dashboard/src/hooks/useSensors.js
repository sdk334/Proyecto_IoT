import { useEffect, useState, useCallback } from 'react'
import { ref, onValue, set } from 'firebase/database'
import { db } from '../firebase'

const HISTORY_LIMIT = 20

export function useSensors() {
  const [sensors, setSensors] = useState({
    temperatura: null,
    humedad: null,
    nivel_agua: null,
  })
  const [pump, setPump] = useState(null)
  const [history, setHistory] = useState({
    temperatura: [],
    humedad: [],
    nivel_agua: [],
  })
  const [connected, setConnected] = useState(false)

  useEffect(() => {
    const unsubs = []
    let hits = 0
    const markConnected = () => { if (++hits >= 4) setConnected(true) }

    // Valores actuales de sensores
    ;['temperatura', 'humedad', 'nivel_agua'].forEach(sensor => {
      unsubs.push(
        onValue(ref(db, `sensores/${sensor}`), snap => {
          markConnected()
          const d = snap.val()
          if (d) setSensors(prev => ({ ...prev, [sensor]: d }))
        })
      )
    })

    // Estado de la bomba
    unsubs.push(
      onValue(ref(db, 'actuadores/bomba'), snap => {
        markConnected()
        setPump(snap.val())
      })
    )

    // Historial para gráficas
    ;['temperatura', 'humedad', 'nivel_agua'].forEach(sensor => {
      unsubs.push(
        onValue(ref(db, `historial/${sensor}`), snap => {
          const d = snap.val()
          if (!d) return
          const arr = Object.values(d)
            .sort((a, b) => new Date(a.timestamp) - new Date(b.timestamp))
            .slice(-HISTORY_LIMIT)
            .map(d => ({
              time: new Date(d.timestamp).toLocaleTimeString('es-MX', {
                hour: '2-digit', minute: '2-digit', second: '2-digit',
              }),
              value: parseFloat(d.valor),
            }))
          setHistory(prev => ({ ...prev, [sensor]: arr }))
        })
      )
    })

    return () => unsubs.forEach(fn => fn())
  }, [])

  const setPumpState = useCallback(async estado => {
    await set(ref(db, 'actuadores/bomba'), {
      valor: estado,
      timestamp: new Date().toISOString(),
    })
  }, [])

  return { sensors, pump, history, connected, setPumpState }
}
