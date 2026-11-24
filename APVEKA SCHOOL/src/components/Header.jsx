import './Header.css'
import { useEffect, useState } from 'react'
import Logo from './Logo.jsx'

const links = [
  { href: '#about', label: 'About' },
  { href: '#academics', label: 'Academics' },
  { href: '#admissions', label: 'Admissions' },
  { href: '#news', label: 'News' },
  { href: '#gallery', label: 'Gallery' },
  { href: '#contact', label: 'Contact' },
]

export default function Header() {
  const [scrolled, setScrolled] = useState(false)
  const [open, setOpen] = useState(false)

  useEffect(() => {
    const onScroll = () => setScrolled(window.scrollY > 40)
    onScroll()
    window.addEventListener('scroll', onScroll)
    return () => window.removeEventListener('scroll', onScroll)
  }, [])

  const close = () => setOpen(false)

  return (
    <header className={scrolled || open ? 'solid' : ''}>
      <div className="wrap nav">
        <Logo />
        <button
          className="burger"
          aria-label="Open menu"
          aria-expanded={open}
          onClick={() => setOpen(!open)}
        >
          <span></span><span></span><span></span>
        </button>
        <ul className={`menu ${open ? 'open' : ''}`}>
          {links.map((l) => (
            <li key={l.href}><a href={l.href} onClick={close}>{l.label}</a></li>
          ))}
          <li><a href="#apply" className="btn btn-primary" onClick={close}>Apply now</a></li>
        </ul>
      </div>
    </header>
  )
}
