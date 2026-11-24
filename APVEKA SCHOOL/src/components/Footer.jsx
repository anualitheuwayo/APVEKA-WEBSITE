import './Footer.css'
import Logo from './Logo.jsx'

export default function Footer() {
  return (
    <footer>
      <div className="wrap">
        <div className="f-cols">
          <div>
            <Logo />
            <p style={{ maxWidth: 280 }}>A strong foundation for a bright future.</p>
          </div>
          <div>
            <h4>School</h4>
            <ul><li><a href="#about">About</a></li><li><a href="#academics">Academics</a></li><li><a href="#gallery">Gallery</a></li></ul>
          </div>
          <div>
            <h4>Parents</h4>
            <ul><li><a href="#admissions">Admissions</a></li><li><a href="#news">News &amp; events</a></li><li><a href="#contact">Fee structure</a></li></ul>
          </div>
          <div>
            <h4>Follow us</h4>
            <ul><li><a href="#">Facebook</a></li><li><a href="#">Instagram</a></li><li><a href="#">YouTube</a></li></ul>
          </div>
        </div>
      </div>
      <div className="wrap f-bottom">
        <span>© {new Date().getFullYear()} APVEKA Nursery &amp; Primary School</span>
        <span>All rights reserved</span>
      </div>
    </footer>
  )
}
