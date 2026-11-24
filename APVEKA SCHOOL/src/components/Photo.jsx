import './Photo.css'
// Image box. Without `src` it shows a grey placeholder with a label.
// To add a photo: put it in public/images and pass src="/images/your-photo.jpg"
export default function Photo({ src, label = 'Photo', className = '', style = {} }) {
  return (
    <div
      className={`ph ${src ? 'has-img' : ''} ${className}`.trim()}
      data-label={label}
      style={src ? { ...style, backgroundImage: `url('${src}')` } : style}
    />
  )
}
