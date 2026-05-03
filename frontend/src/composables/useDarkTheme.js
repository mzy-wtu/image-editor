import { ref } from 'vue'

const isDarkTheme = ref(false)

function loadTheme() {
  const saved = localStorage.getItem('theme')
  if (saved === 'dark') {
    isDarkTheme.value = true
    document.documentElement.setAttribute('data-theme', 'dark')
  } else if (saved === 'light') {
    isDarkTheme.value = false
    document.documentElement.setAttribute('data-theme', 'light')
  } else {
    const prefers = window.matchMedia('(prefers-color-scheme: dark)').matches
    isDarkTheme.value = prefers
    document.documentElement.setAttribute('data-theme', prefers ? 'dark' : 'light')
  }
}

function toggleTheme() {
  isDarkTheme.value = !isDarkTheme.value
  const theme = isDarkTheme.value ? 'dark' : 'light'
  document.documentElement.setAttribute('data-theme', theme)
  localStorage.setItem('theme', theme)
}

loadTheme()

export function useDarkTheme() {
  return { isDarkTheme, toggleTheme }
}
