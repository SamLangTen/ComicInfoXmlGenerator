<script setup lang="ts">
import { ref } from 'vue'

const props = defineProps<{
  files: string[],
  activeTasks: Record<string, any>
}>()

const emit = defineEmits<{
  (e: 'selection-changed', paths: string[]): void
}>()

const selectedPaths = ref<Set<string>>(new Set())

const toggleSelection = (event: MouseEvent, path: string) => {
  const isMulti = event.ctrlKey || event.metaKey
  
  if (!isMulti) {
    selectedPaths.value = new Set([path])
  } else {
    if (selectedPaths.value.has(path)) {
      selectedPaths.value.delete(path)
    } else {
      selectedPaths.value.add(path)
    }
  }
  
  emit('selection-changed', Array.from(selectedPaths.value))
}

const getBaseName = (path: string) => {
  return path.split(/[\/]/).pop() || path
}
</script>

<template>
  <div class="flex flex-col space-y-1">
    <div
      v-for="file in props.files"
      :key="file"
      class="file-item px-3 py-2 text-sm rounded cursor-pointer transition-colors duration-150 flex items-center justify-between"
      :class="[
        selectedPaths.has(file)
          ? 'bg-blue-600 text-white'
          : 'text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-800'
      ]"
      @click="toggleSelection($event, file)"
      :title="file"
    >
      <span class="truncate">{{ getBaseName(file) }}</span>
      <div v-if="props.activeTasks[file]" class="ml-2 shrink-0">
        <div class="w-3 h-3 border-2 border-current border-t-transparent rounded-full animate-spin opacity-60"></div>
      </div>
    </div>
  </div>
</template>

<style scoped>
</style>
