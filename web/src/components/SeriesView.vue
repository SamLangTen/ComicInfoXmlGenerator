<script setup lang="ts">
const props = defineProps<{
  seriesList: any[],
  activeTasks: Record<string, any>
}>()

const getActiveTaskCount = (series: any) => {
  if (!series.paths) return 0
  return series.paths.filter((p: string) => !!props.activeTasks[p]).length
}

const emit = defineEmits<{
  (e: 'select-series', series: any): void
}>()

const getSeriesName = (series: any) => series.name || 'Unknown Series'

const getCoverUrl = (path: string) => {
  if (!path) return ''
  return `/api/cover?path=${encodeURIComponent(path)}`
}

const handleImageError = (e: Event) => {
  const target = e.target as HTMLImageElement
  target.style.display = 'none'
}
</script>

<template>
  <div class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 xl:grid-cols-5 gap-6">
    <div 
      v-for="series in props.seriesList" 
      :key="series.name"
      class="group relative bg-white dark:bg-gray-900 rounded-xl overflow-hidden border dark:border-gray-800 shadow-sm hover:shadow-xl hover:-translate-y-1 transition-all duration-300 cursor-pointer flex flex-col"
      @click="emit('select-series', series)"
    >
      <!-- Cover -->
      <div class="aspect-[3/4] bg-gray-200 dark:bg-gray-800 flex items-center justify-center relative overflow-hidden">
        <!-- Actual Cover Image -->
        <img 
          v-if="series.cover_path" 
          :src="getCoverUrl(series.cover_path)" 
          @error="handleImageError"
          loading="lazy"
          class="absolute inset-0 w-full h-full object-cover z-10 transition-transform duration-500 group-hover:scale-105" 
          alt="Cover"
        />
        
        <!-- Placeholder (shows if image fails or isn't there) -->
        <svg class="w-12 h-12 text-gray-400 opacity-20" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
        </svg>
        
        <!-- Badge for count -->
        <div class="absolute top-2 right-2 bg-black/60 backdrop-blur-md text-white text-[10px] font-bold px-2 py-0.5 rounded-full z-20 shadow-sm border border-white/10">
          {{ series.count }}
        </div>

        <!-- Active Tasks Indicator -->
        <div v-if="getActiveTaskCount(series) > 0" class="absolute inset-0 bg-blue-600/20 backdrop-blur-[2px] z-15 flex items-center justify-center pointer-events-none">
          <div class="bg-white dark:bg-gray-900 rounded-full p-2 shadow-xl animate-bounce">
            <div class="w-4 h-4 border-2 border-blue-600 border-t-transparent rounded-full animate-spin"></div>
          </div>
          <div class="absolute bottom-2 left-2 bg-blue-600 text-white text-[8px] font-black px-1.5 py-0.5 rounded-md shadow-lg uppercase tracking-tighter">
            Scraping {{ getActiveTaskCount(series) }}...
          </div>
        </div>
      </div>
      
      <!-- Info -->
      <div class="p-4 border-t dark:border-gray-800 bg-white dark:bg-gray-900 z-20 flex-1">
        <h3 class="font-bold text-sm truncate group-hover:text-blue-600 dark:group-hover:text-blue-400 transition-colors" :title="getSeriesName(series)">
          {{ getSeriesName(series) }}
        </h3>
        <p class="text-[10px] text-gray-500 mt-1 uppercase tracking-wider font-semibold">
          {{ series.count }} {{ series.count === 1 ? 'Volume' : 'Volumes' }}
        </p>
      </div>
    </div>
  </div>
</template>
