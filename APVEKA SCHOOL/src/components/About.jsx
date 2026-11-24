import './About.css'
import Photo from './Photo.jsx'

export default function About() {
  return (
    <section className="about" id="about">
      <div className="wrap">
        <div className="split">
          <Photo label="School photo · 800 × 1000" />
          <div>
            <span className="label">About us</span>
            <h2>Nurturing learners from their first step</h2>
            <p>APVEKA Nursery &amp; Primary School is a community of teachers, parents and pupils working together to give every child a quality education and a happy childhood.</p>
            <p>Our approach balances strong academics with creativity, sport and character, so children grow in confidence as well as knowledge.</p>
            <div className="vm">
              <div><h4>Our vision</h4><p>To raise confident, responsible and lifelong learners.</p></div>
              <div><h4>Our mission</h4><p>To provide holistic, quality education in a safe and loving environment.</p></div>
            </div>
            <a href="#contact" className="link">Visit the school</a>
          </div>
        </div>

        <div className="quote">
          <Photo label="Head teacher" />
          <div>
            <blockquote>"Every child who walks through our gate is seen, valued and supported. We look forward to welcoming your family."</blockquote>
            <cite><b>[Head Teacher's Name]</b> · Head Teacher</cite>
          </div>
        </div>
      </div>
    </section>
  )
}
