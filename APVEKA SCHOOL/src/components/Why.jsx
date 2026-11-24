import './Why.css'
const items = [
  { title: 'Dedicated teachers', text: 'Qualified, caring teachers who know each child and support them to reach their potential.' },
  { title: 'Safe environment', text: 'A secure, clean and well-supervised compound where children feel at home.' },
  { title: 'Strong values', text: 'We raise pupils who are respectful, disciplined and ready for the next stage of life.' },
]

export default function Why() {
  return (
    <section id="why">
      <div className="wrap">
        <div className="sec-head">
          <span className="label">Why APVEKA</span>
          <h2>Education that shapes the whole child</h2>
        </div>
        <div className="intro-grid">
          {items.map((i) => (
            <div className="intro-item" key={i.title}>
              <h3>{i.title}</h3>
              <p>{i.text}</p>
            </div>
          ))}
        </div>
      </div>
    </section>
  )
}
