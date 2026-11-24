import './Hero.css'
// To add the background photo: put it in public/images (e.g. hero.jpg)
// and set HERO_IMAGE = '/images/hero.jpg'
const HERO_IMAGE = ''

export default function Hero() {
  return (
    <section className="hero" id="home">
      <div
        className={`hero-bg ${HERO_IMAGE ? 'has-img' : ''}`}
        style={HERO_IMAGE ? { backgroundImage: `url('${HERO_IMAGE}')` } : undefined}
      />
      <div className="wrap">
        <div className="hero-content">
          <span className="label">Nursery &amp; Primary School</span>
          <h1>A strong foundation for a bright future</h1>
          <p>At APVEKA, every child learns in a safe, caring environment that builds knowledge, character and confidence.</p>
          <div className="hero-ctas">
            <a href="#apply" className="btn btn-primary">Apply for admission</a>
            <a href="#contact" className="btn btn-outline">Book a visit</a>
          </div>
        </div>
      </div>
      <div className="hero-bar">
        <i style={{ background: 'var(--navy-2)' }}></i>
        <i style={{ background: 'var(--green)' }}></i>
        <i style={{ background: 'var(--sun)' }}></i>
      </div>
    </section>
  )
}
