import { useEffect, useRef, useState } from 'react'

export interface WsMessage {
  type: 'inventory_alert' | 'churn_update' | string
  [key: string]: unknown
}

export function useWebSocket(url: string) {
  const [messages, setMessages]   = useState<WsMessage[]>([])
  const [connected, setConnected] = useState(false)
  const ws              = useRef<WebSocket | null>(null)
  const shouldReconnect = useRef(true)
  const retryTimer      = useRef<ReturnType<typeof setTimeout> | null>(null)
  const pingInterval    = useRef<ReturnType<typeof setInterval> | null>(null)

  useEffect(() => {
    shouldReconnect.current = true

    const clearTimers = () => {
      if (retryTimer.current)  { clearTimeout(retryTimer.current);  retryTimer.current  = null }
      if (pingInterval.current){ clearInterval(pingInterval.current); pingInterval.current = null }
    }

    const connect = () => {
      if (!shouldReconnect.current) return
      clearTimers()

      const socket = new WebSocket(url)
      ws.current = socket

      socket.onopen = () => {
        if (ws.current !== socket) return
        setConnected(true)
        // Send a keepalive ping every 20s so the connection never idles out
        pingInterval.current = setInterval(() => {
          if (socket.readyState === WebSocket.OPEN) {
            socket.send(JSON.stringify({ type: 'ping' }))
          }
        }, 20_000)
      }

      socket.onclose = () => {
        if (ws.current !== socket) return
        clearTimers()
        setConnected(false)
        if (shouldReconnect.current) {
          retryTimer.current = setTimeout(connect, 3000)
        }
      }

      socket.onmessage = (e) => {
        try {
          const msg = JSON.parse(e.data) as WsMessage
          // Ignore server keepalive frames
          if (msg.type === 'ping' || msg.type === 'pong') return
          setMessages((prev) => [msg, ...prev].slice(0, 50))
        } catch {}
      }

      socket.onerror = () => {
        socket.close()
      }
    }

    connect()

    return () => {
      shouldReconnect.current = false
      clearTimers()
      ws.current?.close()
    }
  }, [url])

  return { messages, connected }
}
