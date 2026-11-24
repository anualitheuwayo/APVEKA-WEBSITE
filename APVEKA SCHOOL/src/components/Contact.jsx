import './Contact.css'

const details = [
  { title: 'Address', value: 'Karenge, Rwanda' },
  { title: 'Phone / WhatsApp', value: '+250 783 108 365' },
  { title: 'Email', value: 'info@apveka.school' },
  { title: 'Office hours', value: 'Mon – Fri, 7:00 am – 5:00 pm' },
]

const MAP_URL =
  'https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d32796.608132246045!2d30.295133028711422!3d-2.0710324953408787!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x19db530028d3301d%3A0xd407d008fb66cf87!2sAPVEKA%20school!5e0!3m2!1sen!2snl!4v1794814632654!5m2!1sen!2snl'

export default function Contact() {
  return (
    <section id="contact">
      <div className="wrap">
        <div className="c-grid">
          <div>
            <span className="label">Contact</span>
            <h2 style={{ fontSize: 'clamp(32px,4vw,44px)', marginBottom: 30 }}>Get in touch</h2>
            <div className="c-list">
              {details.map((d) => (
                <div key={d.title}><h4>{d.title}</h4><p>{d.value}</p></div>
              ))}
            </div>
          </div>

          <div className="map">
            <iframe
              src={MAP_URL}
              title="APVEKA School location on Google Maps"
              width="100%"
              height="100%"
              style={{ border: 0, minHeight: 420, display: 'block' }}
              allowFullScreen
              loading="lazy"
              referrerPolicy="strict-origin-when-cross-origin"
            />
          </div>
        </div>
      </div>
    </section>
  )
}
