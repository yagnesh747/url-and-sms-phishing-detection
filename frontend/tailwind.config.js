module.exports = {
    content: [
        "./index.html",
        "./src/**/*.{js,ts,jsx,tsx}",
    ],
    theme: {
        extend: {
            fontFamily: {
                sans: ['Outfit', 'sans-serif'],
                mono: ['Inter', 'monospace'],
            },
            colors: {
                cyber: {
                    900: '#070b19',
                    800: '#0c132c',
                    700: '#141f45',
                    blue: '#00f0ff',
                    purple: '#b300ff',
                    pink: '#ff007f'
                }
            },
            animation: {
                'blob': 'blob 7s infinite',
                'pulse-slow': 'pulse 4s cubic-bezier(0.4, 0, 0.6, 1) infinite',
                'float': 'float 6s ease-in-out infinite',
            },
            keyframes: {
                blob: {
                    '0%': { transform: 'translate(0px, 0px) scale(1)' },
                    '33%': { transform: 'translate(30px, -50px) scale(1.1)' },
                    '66%': { transform: 'translate(-20px, 20px) scale(0.9)' },
                    '100%': { transform: 'translate(0px, 0px) scale(1)' }
                },
                float: {
                    '0%, 100%': { transform: 'translateY(0)' },
                    '50%': { transform: 'translateY(-10px)' },
                }
            }
        },
    },
    plugins: [
        // a custom utility for hiding scrollbars while keeping functionality
        function({ addUtilities }) {
            addUtilities({
                '.no-scrollbar::-webkit-scrollbar': {
                    'display': 'none'
                },
                '.no-scrollbar': {
                    '-ms-overflow-style': 'none',
                    'scrollbar-width': 'none' // Firefox
                }
            })
        }
    ],
}
