import './Admissions.css'
import { useState } from 'react'

const steps = [
  { title: 'Send an enquiry', text: 'Fill in the form or call the school office.' },
  { title: 'Visit the school', text: 'Tour our classrooms and meet the teachers.' },
  { title: 'Assessment', text: 'A short, friendly interview to place your child.' },
  { title: 'Registration', text: 'Complete the forms and get ready for day one.' },
]

const classes = ['Playgroup', 'PP1', 'PP2', 'Grade 1', 'Grade 2', 'Grade 3', 'Grade 4', 'Grade 5', 'Grade 6']

const empty = { pname: '', phone: '', cname: '', cls: '', msg: '' }

function validate(f) {
  const e = {}
  if (!f.pname.trim()) e.pname = 'Enter your name'
  if (!/^[+0-9\s]{9,15}$/.test(f.phone.trim())) e.phone = 'Enter a valid phone number'
  if (!f.cname.trim()) e.cname = "Enter your child's name"
  if (!f.cls) e.cls = 'Choose a class'
  return e
}

export default function Admissions() {
  const [form, setForm] = useState(empty)
  const [errors, setErrors] = useState({})
  const [sent, setSent] = useState(false)

  const update = (key) => (e) => {
    setForm({ ...form, [key]: e.target.value })
    setErrors({ ...errors, [key]: undefined })
  }

  const onSubmit = (e) => {
    e.preventDefault()
    const errs = validate(form)
    setErrors(errs)
    if (Object.keys(errs).length === 0) {
      // TODO: send `form` to your backend or email service here
      setSent(true)
      setForm(empty)
    }
  }

  const errStyle = (key) => (errors[key] ? { borderColor: '#B42318' } : undefined)
  const Err = ({ k }) => errors[k] ? <div className="err" style={{ display: 'block' }}>{errors[k]}</div> : null

  return (
    <section className="admissions" id="admissions">
      <div className="wrap">
        <div className="adm-grid">
          <div>
            <span className="label">Admissions</span>
            <h2 style={{ fontSize: 'clamp(32px,4vw,44px)', marginBottom: 18 }}>Join the APVEKA family</h2>
            <p style={{ color: 'rgba(255,255,255,.75)', marginBottom: 44 }}>We welcome new pupils throughout the year, subject to space in each class.</p>
            <ol className="steps">
              {steps.map((s) => (
                <li key={s.title}><div><h3>{s.title}</h3><p>{s.text}</p></div></li>
              ))}
            </ol>
            <div className="docs">
              <b>Documents required</b>
              Birth certificate, two passport photos, parent's ID, immunisation card (nursery), and last report form (transfers).
            </div>
          </div>

          <form className="form" id="apply" noValidate onSubmit={onSubmit}>
            <h3>Admission enquiry</h3>
            <p>Share a few details and our office will contact you.</p>
            <div className="f-grid">
              <div>
                <label htmlFor="pname">Parent's name</label>
                <input id="pname" placeholder="Jane Wanjiru" value={form.pname} onChange={update('pname')} style={errStyle('pname')} />
                <Err k="pname" />
              </div>
              <div>
                <label htmlFor="phone">Phone number</label>
                <input id="phone" type="tel" placeholder="0712 345 678" value={form.phone} onChange={update('phone')} style={errStyle('phone')} />
                <Err k="phone" />
              </div>
              <div>
                <label htmlFor="cname">Child's name</label>
                <input id="cname" placeholder="Amani" value={form.cname} onChange={update('cname')} style={errStyle('cname')} />
                <Err k="cname" />
              </div>
              <div>
                <label htmlFor="cls">Class</label>
                <select id="cls" value={form.cls} onChange={update('cls')} style={errStyle('cls')}>
                  <option value="">Choose a class</option>
                  {classes.map((c) => <option key={c}>{c}</option>)}
                </select>
                <Err k="cls" />
              </div>
              <div className="full">
                <label htmlFor="msg">Message (optional)</label>
                <textarea id="msg" placeholder="Any questions about the school" value={form.msg} onChange={update('msg')} />
              </div>
              <div className="full">
                <button type="submit" className="btn btn-navy" style={{ width: '100%' }}>Send enquiry</button>
              </div>
            </div>
            {sent && (
              <div className="form-msg" style={{ display: 'block' }}>
                Thank you. This is a preview, so the form isn't sending yet. Once the site is live, enquiries will reach the school office.
              </div>
            )}
          </form>
        </div>
      </div>
    </section>
  )
}
