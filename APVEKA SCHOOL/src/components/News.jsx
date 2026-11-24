import './News.css'
import Photo from './Photo.jsx'

const posts = [
  { date: '12 November 2026', title: 'PP2 graduation ceremony', text: 'Families joined us to celebrate our pupils moving up to Grade 1.' },
  { date: '28 October 2026', title: 'Annual sports day', text: 'A day of races, teamwork and school spirit across every class.' },
  { date: '5 January 2027', title: 'Term 1 opening', text: 'All pupils report by 7:30 am. Uniform and supply lists are available at the office.' },
]

export default function News() {
  return (
    <section id="news">
      <div className="wrap">
        <div className="news-head">
          <div className="sec-head">
            <span className="label">News &amp; events</span>
            <h2>Latest from the school</h2>
          </div>
          <a href="#news" className="link">View all news</a>
        </div>
        <div className="news-grid">
          {posts.map((p) => (
            <article className="post" key={p.title}>
              <Photo label="News photo" />
              <span className="date">{p.date}</span>
              <h3>{p.title}</h3>
              <p>{p.text}</p>
            </article>
          ))}
        </div>
      </div>
    </section>
  )
}
