import './Academics.css'
import Photo from './Photo.jsx'

const levels = [
  {
    name: 'Nursery',
    ages: 'Ages 3 – 5',
    classes: 'Playgroup, PP1, PP2',
    text: 'A gentle, play-based start that builds language, early numeracy and social skills.',
    points: ['Early reading and writing', 'Number work and problem solving', 'Creative arts, music and outdoor play'],
    photo: 'Nursery photo · 1200 × 675',
  },
  {
    name: 'Primary',
    ages: 'Ages 6 – 12',
    classes: 'Grade 1 – Grade 6',
    text: 'A solid academic foundation with room to discover talents and build character.',
    points: ['English, Kiswahili and Mathematics', 'Science, Social Studies and Religious Education', 'ICT, sports, music and clubs'],
    photo: 'Primary photo · 1200 × 675',
  },
]

export default function Academics() {
  return (
    <section id="academics">
      <div className="wrap">
        <div className="sec-head">
          <span className="label">Academics</span>
          <h2>Two stages, one journey</h2>
          <p>Our programmes are designed around how children learn best at every age.</p>
        </div>
        <div className="levels">
          {levels.map((l) => (
            <div className="level" key={l.name}>
              <Photo label={l.photo} />
              <div className="level-body">
                <span className="meta">{l.ages}</span>
                <h3>{l.name}</h3>
                <p className="classes"><b>Classes:</b> {l.classes}</p>
                <p>{l.text}</p>
                <ul>{l.points.map((p) => <li key={p}>{p}</li>)}</ul>
              </div>
            </div>
          ))}
        </div>
      </div>
    </section>
  )
}
