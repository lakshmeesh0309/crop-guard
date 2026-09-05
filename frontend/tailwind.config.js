/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html','./src/**/*.{js,jsx}'],
  theme: {
    extend: {
      fontFamily: {
        display: ['"Plus Jakarta Sans"','sans-serif'],
        body:    ['"Inter"','sans-serif'],
      },
      colors: {
        brand: {
          50:'#f0fdf4', 100:'#dcfce7', 200:'#bbf7d0',
          300:'#86efac', 400:'#4ade80', 500:'#22c55e',
          600:'#16a34a', 700:'#15803d', 800:'#166534', 900:'#14532d', 950:'#052e16',
        },
        earth: { 50:'#fefce8',100:'#fef9c3',400:'#facc15',600:'#ca8a04',800:'#713f12' },
        leaf:  { 400:'#4ade80', 600:'#16a34a' },
      },
      backgroundImage: {
        'hero-gradient': 'linear-gradient(135deg, #052e16 0%, #14532d 40%, #166534 70%, #15803d 100%)',
        'card-gradient': 'linear-gradient(135deg, rgba(255,255,255,0.08) 0%, rgba(255,255,255,0.02) 100%)',
        'glow-green':    'radial-gradient(ellipse at center, rgba(34,197,94,0.15) 0%, transparent 70%)',
      },
      boxShadow: {
        'card':   '0 1px 3px rgba(0,0,0,0.06), 0 4px 16px rgba(0,0,0,0.04)',
        'card-hover':'0 4px 12px rgba(0,0,0,0.10), 0 8px 32px rgba(0,0,0,0.06)',
        'glow':   '0 0 40px rgba(34,197,94,0.25)',
        'inner-glow':'inset 0 1px 0 rgba(255,255,255,0.1)',
      },
      animation: {
        'fade-in':  'fadeIn 0.4s ease-out',
        'slide-up': 'slideUp 0.4s ease-out',
        'float':    'float 6s ease-in-out infinite',
        'pulse-slow':'pulse 4s ease-in-out infinite',
        'shimmer':  'shimmer 2s linear infinite',
      },
      keyframes: {
        fadeIn:  { from:{opacity:0},          to:{opacity:1} },
        slideUp: { from:{opacity:0,transform:'translateY(16px)'}, to:{opacity:1,transform:'translateY(0)'} },
        float:   { '0%,100%':{transform:'translateY(0)'}, '50%':{transform:'translateY(-10px)'} },
        shimmer: { '0%':{backgroundPosition:'-200% 0'}, '100%':{backgroundPosition:'200% 0'} },
      },
    },
  },
  plugins: [],
}
