import { useEffect, useRef, useState } from 'react'

export default function useInViewOnce(options = { threshold: 0.2 }) {
  const ref = useRef(null)
  const [visible, setVisible] = useState(false)
  useEffect(() => {
    const el = ref.current
    if (!el) return
    const obs = new IntersectionObserver(([e]) => e.isIntersecting && setVisible(true), options)
    obs.observe(el)
    return () => obs.disconnect()
  }, [options.threshold])
  return [ref, visible]
}
