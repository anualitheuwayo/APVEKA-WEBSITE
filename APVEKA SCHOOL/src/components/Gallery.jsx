import './Gallery.css'
import Photo from './Photo.jsx'

const photos = [
  { size: 'tall' },
  { size: 'wide' },
  { size: '' },
  { size: '' },
  { size: '' },
  { size: 'wide' },
]

export default function Gallery() {
  return (
    <section className="gallery" id="gallery">
      <div className="wrap">
        <div className="sec-head">
          <span className="label">Gallery</span>
          <h2>Life at APVEKA</h2>
        </div>
        <div className="g-grid">
          {photos.map((p, i) => (
            <Photo key={i} className={p.size} src={p.src} label="Photo" />
          ))}
        </div>
      </div>
    </section>
  )
}
