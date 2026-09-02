import { useEffect, useRef, useState } from 'react'

export default function useInView(options = { threshold: 0.15 }) {
  const ref = useRef(null)
  const [visible, setVisible] = useState(false)
  useEffect(() => {
    const el = ref.current
    if (!el) return
    const obs = new IntersectionObserver(([e]) => setVisible(e.isIntersecting), options)
    obs.observe(el)
    return () => obs.disconnect()
  }, [options.threshold])
  return [ref, visible]
}
