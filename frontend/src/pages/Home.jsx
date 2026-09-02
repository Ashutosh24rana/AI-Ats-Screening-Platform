import { useEffect, useState } from 'react'

import HomeNavbar from '../components/home/HomeNavbar.jsx'
import Hero from '../components/home/Hero.jsx'
import HowItWorks from '../components/home/HowItWorks.jsx'
import Features from '../components/home/Features.jsx'
import useInView from '../hooks/useInView'

function ScrollProgress() {
  const [w, setW] = useState(0)
  useEffect(() => {
    const onScroll = () => {
      const max = document.documentElement.scrollHeight - window.innerHeight
      setW(max > 0 ? (window.scrollY / max) * 100 : 0)
    }
    window.addEventListener('scroll', onScroll, { passive: true })
    onScroll()
    return () => window.removeEventListener('scroll', onScroll)
  }, [])
  return <div className="fixed left-0 top-0 z-50 h-0.5 bg-gradient-to-r from-amber-400 to-orange-500 transition-all duration-150" style={{ width: `${w}%` }} />
}

export default function Home() {
  const [heroRef, heroVisible] = useInView({ threshold: 0.1 })
  const [stepsRef, stepsVisible] = useInView({ threshold: 0.15 })
  const [featuresRef, featuresVisible] = useInView({ threshold: 0.15 })

  return (
    <div className="min-h-screen bg-slate-950">
      <style>{`html{scroll-behavior:smooth} body{background:#020617}`}</style>
      <ScrollProgress />
      <HomeNavbar />
      <Hero heroRef={heroRef} visible={heroVisible} />
      <HowItWorks stepsRef={stepsRef} visible={stepsVisible} />
      <div ref={featuresRef} className={`transition-all duration-700 ${featuresVisible ? 'translate-y-0 opacity-100' : 'translate-y-8 opacity-0'}`}>
        <Features />
      </div>
      <footer className="border-t border-white/10 bg-slate-950 py-8 text-center text-xs text-slate-500">
        © {new Date().getFullYear()} AI ATS Platform · All rights reserved
      </footer>
    </div>
  )
}
