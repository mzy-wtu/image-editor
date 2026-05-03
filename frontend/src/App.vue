<template>
  <div id="app-root">
    <router-view />
    <Toast />
  </div>
</template>

<script>
import Toast from './components/common/Toast.vue'

export default {
  name: 'App',
  components: { Toast }
}
</script>

<style>
*, *::before, *::after {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}
body {
  font-family: system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif;
  -webkit-font-smoothing: antialiased;
}
#app-root {
  min-height: 100vh;
}
</style>
