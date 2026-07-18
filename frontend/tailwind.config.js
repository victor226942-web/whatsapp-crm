/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{js,jsx}"],
  theme: {
    extend: {
      colors: {
        // Paleta baseada no WhatsApp Web: verde-escuro do header, verde-claro
        // do balão enviado, fundo bege-acinzentado do chat.
        panel: "#111b21",
        "panel-header": "#202c33",
        accent: "#00a884",
        "accent-dark": "#008069",
        "bubble-out": "#005c4b",
        "bubble-in": "#202c33",
        "chat-bg": "#0b141a",
      },
    },
  },
  plugins: [],
}
