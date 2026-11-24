# APVEKA Nursery & Primary School website (React + Vite)

## Run it
```bash
npm install
npm run dev
```
Open the link shown in the terminal (usually http://localhost:5173).

## Add photos
1. Put images in `public/images/`
2. Hero background: in `src/components/Hero.jsx` set `HERO_IMAGE = '/images/hero.jpg'`
3. Other photos: pass `src` to `<Photo>`, e.g. `<Photo src="/images/about.jpg" label="School photo" />`

## Build for hosting
```bash
npm run build
```
Upload the `dist/` folder to Netlify, Vercel or GitHub Pages.
