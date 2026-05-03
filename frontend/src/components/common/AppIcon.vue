<template>
  <svg
    :width="size"
    :height="size"
    :class="className"
    viewBox="0 0 24 24"
    fill="none"
    stroke="currentColor"
    stroke-width="2"
    stroke-linecap="round"
    stroke-linejoin="round"
  >
    <component :is="iconPath" v-if="iconPath" />
  </svg>
</template>

<script>
import { h, computed } from 'vue'

const ICONS = {
  image: () => [h('rect', { x: '3', y: '3', width: '18', height: '18', rx: '2' }), h('circle', { cx: '8.5', cy: '8.5', r: '1.5' }), h('path', { d: 'M21 15l-5-5L5 21' })],
  generate: () => [h('path', { d: 'M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z' }), h('path', { d: 'M3.27 6.96L12 12.01l8.73-5.05M12 22.08V12' })],
  plus: () => [h('path', { d: 'M12 3v18M3 12h18' })],
  edit: () => [h('path', { d: 'M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7' }), h('path', { d: 'M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z' })],
  sun: () => [h('circle', { cx: '12', cy: '12', r: '5' }), h('path', { d: 'M12 1v2M12 21v2M4.22 4.22l1.42 1.42M18.36 18.36l1.42 1.42M1 12h2M21 12h2M4.22 19.78l1.42-1.42M18.36 5.64l1.42-1.42' })],
  moon: () => [h('path', { d: 'M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z' })],
  history: () => [h('path', { d: 'M3 3v5h5M3.05 13A9 9 0 1 0 6 5.3L3 8M12 7v5l4 2' })],
  admin: () => [h('path', { d: 'M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2' }), h('circle', { cx: '9', cy: '7', r: '4' }), h('path', { d: 'M23 21v-2a4 4 0 0 0-3-3.87M16 3.13a4 4 0 0 1 0 7.75' })],
  logout: () => [h('path', { d: 'M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4M16 17l5-5-5-5M21 12H9' })],
  upload: () => [h('path', { d: 'M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4' }), h('polyline', { points: '17 8 12 3 7 8' }), h('line', { x1: '12', y1: '3', x2: '12', y2: '15' })],
  download: () => [h('path', { d: 'M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4' }), h('polyline', { points: '7 10 12 15 17 10' }), h('line', { x1: '12', y1: '15', x2: '12', y2: '3' })],
  search: () => [h('circle', { cx: '11', cy: '11', r: '8' }), h('path', { d: 'M21 21l-4.35-4.35' })],
  close: () => [h('line', { x1: '18', y1: '6', x2: '6', y2: '18' }), h('line', { x1: '6', y1: '6', x2: '18', y2: '18' })],
  template: () => [h('path', { d: 'M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z' }), h('path', { d: 'M14 2v6h6M16 13H8M16 17H8M10 9H8' })],
  star: () => [h('polygon', { points: '12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2' })],
  delete: () => [h('polyline', { points: '3 6 5 6 21 6' }), h('path', { d: 'M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2' })],
  info: () => [h('circle', { cx: '12', cy: '12', r: '10' }), h('path', { d: 'M12 8v4M12 16h.01' })],
  user: () => [h('path', { d: 'M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2' }), h('circle', { cx: '12', cy: '7', r: '4' })],
  lock: () => [h('rect', { x: '3', y: '11', width: '18', height: '11', rx: '2', ry: '2' }), h('path', { d: 'M7 11V7a5 5 0 0 1 10 0v4' })],
  mail: () => [h('path', { d: 'M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z' }), h('polyline', { points: '22,6 12,13 2,6' })],
  home: () => [h('path', { d: 'M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z' }), h('polyline', { points: '9 22 9 12 15 12 15 22' })],
  sketch: () => [h('path', { d: 'M12 20h9' }), h('path', { d: 'M16.5 3.5a2.121 2.121 0 0 1 3 3L7 19l-4 1 1-4L16.5 3.5z' })],
  check: () => [h('polyline', { points: '20 6 9 17 4 12' })],
  alert: () => [h('circle', { cx: '12', cy: '12', r: '10' }), h('line', { x1: '12', y1: '8', x2: '12', y2: '12' }), h('line', { x1: '12', y1: '16', x2: '12.01', y2: '16' })],
  'chevron-left': () => [h('polyline', { points: '15 18 9 12 15 6' })],
  'chevron-right': () => [h('polyline', { points: '9 18 15 12 9 6' })],
  ban: () => [h('circle', { cx: '12', cy: '12', r: '10' }), h('line', { x1: '4.93', y1: '4.93', x2: '19.07', y2: '19.07' })],
  eye: () => [h('path', { d: 'M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z' }), h('circle', { cx: '12', cy: '12', r: '3' })],
  'arrow-left': () => [h('line', { x1: '19', y1: '12', x2: '5', y2: '12' }), h('polyline', { points: '12 19 5 12 12 5' })],
  clock: () => [h('circle', { cx: '12', cy: '12', r: '10' }), h('polyline', { points: '12 6 12 12 16 14' })],
}

export default {
  name: 'AppIcon',
  props: {
    name: { type: String, required: true },
    size: { type: [Number, String], default: 24 },
    className: { type: String, default: '' }
  },
  computed: {
    iconPath() {
      return ICONS[this.name] || null
    }
  }
}
</script>
