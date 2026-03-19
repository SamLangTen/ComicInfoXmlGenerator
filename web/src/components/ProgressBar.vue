<script setup lang="ts">
const props = defineProps<{
  value: number
  max: number
  color?: string
  animated?: boolean
}>()

const percentage = Math.min(100, Math.max(0, (props.value / props.max) * 100))
</script>

<template>
  <div class="w-full bg-gray-100 dark:bg-gray-800 rounded-full h-1.5 overflow-hidden">
    <div 
      class="h-full transition-all duration-500 ease-out rounded-full"
      :class="[
        color || 'bg-blue-600',
        { 'animate-pulse': animated }
      ]"
      :style="{ width: `${percentage}%` }"
    ></div>
  </div>
</template>
