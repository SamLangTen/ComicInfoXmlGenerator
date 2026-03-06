<script setup lang="ts">
import { ref, watch, onMounted, onUnmounted, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { apiService } from './services/api'
import ArchiveList from './components/ArchiveList.vue'
import MetadataEditor from './components/MetadataEditor.vue'
import SeriesView from './components/SeriesView.vue'

const route = useRoute()
const router = useRouter()

const activeTab = computed({
  get: () => {
    const path = route.path.substring(1)
    return (['library', 'editor', 'settings'].includes(path) ? path : 'library') as 'library' | 'editor' | 'settings'
  },
  set: (val) => {
    router.push(`/${val}`)
  }
})

const config = ref<any>({})
const libraryStatus = ref<any>({})
const seriesList = ref<any[]>([])
const currentSeries = ref<any>(null)

const directory = ref('')
const archives = ref<string[]>([])
const selectedPaths = ref<string[]>([])
const currentComic = ref<any>(null)
const logs = ref<{time: string, type: 'info' | 'error' | 'warn' | 'tech', msg: string}[]>([])
const isProcessing = ref(false)
const scraperStrategy = ref('local')

const isSetupRequired = computed(() => !config.value.manga_root_directory)

const addLog = (msg: string, type: 'info' | 'error' | 'warn' | 'tech' = 'info') => {
  logs.value.push({
    time: new Date().toLocaleTimeString(),
    type,
    msg
  })
}

const fetchStatus = async () => {
  try {
    config.value = await apiService.getConfig()
    libraryStatus.value = await apiService.getLibraryStatus()
    if (config.value.manga_root_directory) {
      seriesList.value = await apiService.getLibrarySeries()
    }
  } catch (err) {
    console.error('Failed to fetch status', err)
  }
}

const handleSaveConfig = async () => {
  try {
    await apiService.updateConfig(config.value)
    addLog('Configuration saved.', 'info')
    await fetchStatus()
    if (config.value.manga_root_directory) {
        handleLibraryScan()
    }
  } catch (err: any) {
    addLog(`Error saving config: ${err.message}`, 'error')
  }
}

const handleLibraryScan = async () => {
  try {
    addLog('Triggering library scan...', 'info')
    await apiService.triggerLibraryScan()
    // Poll for status or wait for WS
  } catch (err: any) {
    addLog(`Error scanning library: ${err.message}`, 'error')
  }
}

const handleScan = async () => {
  if (!directory.value) return
  try {
    addLog(`Scanning directory: ${directory.value}`)
    const response = await apiService.scanDirectory(directory.value)
    archives.value = response.files
    addLog(`Found ${archives.value.length} archives.`)
  } catch (err: any) {
    addLog(`Error scanning directory: ${err.message}`, 'error')
  }
}

const handleSelectionChanged = async (paths: string[]) => {
  selectedPaths.value = paths
  if (paths.length === 1 && paths[0]) {
    addLog(`Loading metadata: ${paths[0].split(/[\\/]/).pop()}`)
    try {
      currentComic.value = await apiService.getMetadata(paths[0])
    } catch (err: any) {
      addLog(`Error loading metadata: ${err.message}`, 'error')
    }
  } else {
    currentComic.value = null
  }
}

const handleSelectSeries = (series: any) => {
    currentSeries.value = series
    archives.value = series.paths
    activeTab.value = 'editor'
    selectedPaths.value = []
    currentComic.value = null
}

// Auto-save metadata when it changes
watch(currentComic, async (newVal) => {
  if (newVal && selectedPaths.value.length === 1) {
    try {
      await apiService.updateMetadata(newVal)
    } catch (err: any) {
      console.error('Failed to auto-save metadata', err)
    }
  }
}, { deep: true })

const handleScrape = async () => {
  if (selectedPaths.value.length === 0) return
  isProcessing.value = true
  addLog(`Running ${scraperStrategy.value} scraper on ${selectedPaths.value.length} files...`)
  try {
    await apiService.triggerScrape(selectedPaths.value, scraperStrategy.value)
    addLog(`Scraping triggered successfully.`, 'info')
    if (selectedPaths.value.length === 1 && selectedPaths.value[0]) {
       currentComic.value = await apiService.getMetadata(selectedPaths.value[0])
    }
  } catch (err: any) {
    addLog(`Error during scraping: ${err.message}`, 'error')
  } finally {
    isProcessing.value = false
  }
}

const handleInject = async () => {
  if (selectedPaths.value.length === 0) return
  isProcessing.value = true
  try {
    addLog(`Injecting metadata into ${selectedPaths.value.length} file(s)...`)
    const response = await apiService.triggerInject(selectedPaths.value)
    addLog(`Injection process finished.`, 'info')
    Object.entries(response.results).forEach(([path, status]) => {
      const name = path.split(/[\\/]/).pop()
      const type = String(status).includes('error') ? 'error' : 'info'
      addLog(`${name}: ${status}`, type)
    })
  } catch (err: any) {
    addLog(`Error injecting metadata: ${err.message}`, 'error')
  } finally {
    isProcessing.value = false
  }
}

// WebSocket for live logs
let socket: WebSocket | null = null

const connectWebSocket = () => {
  const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:'
  const host = window.location.host
  const wsUrl = `${protocol}//${host}/api/logs`
  
  socket = new WebSocket(wsUrl)
  
  socket.onmessage = (event) => {
    addLog(event.data, 'tech')
    // If it's a scan complete message, refresh library
    if (event.data.includes('Scan complete')) {
        fetchStatus()
    }
  }
  
  socket.onclose = () => {
    setTimeout(connectWebSocket, 5000)
  }
}

onMounted(() => {
  fetchStatus()
  connectWebSocket()
})

onUnmounted(() => {
  if (socket) socket.close()
})
</script>

<template>
  <div class="min-h-screen flex flex-col bg-gray-50 dark:bg-gray-950 text-gray-900 dark:text-gray-100 font-sans">
    <!-- Navbar -->
    <header class="h-16 flex items-center justify-between px-6 border-b bg-white dark:bg-gray-900 dark:border-gray-800 shrink-0 shadow-sm z-20">
      <div class="flex items-center space-x-8">
        <h1 class="text-xl font-black tracking-tighter text-blue-600 dark:text-blue-400">CIXG <span class="text-gray-400 font-light">Service</span></h1>
        
        <nav class="flex items-center space-x-1">
          <button 
            @click="activeTab = 'library'"
            class="px-4 py-2 rounded-lg text-sm font-bold transition-all"
            :class="activeTab === 'library' ? 'bg-blue-50 dark:bg-blue-900/30 text-blue-600 dark:text-blue-400' : 'text-gray-500 hover:bg-gray-100 dark:hover:bg-gray-800'"
          >
            Library
          </button>
          <button 
            @click="activeTab = 'editor'"
            class="px-4 py-2 rounded-lg text-sm font-bold transition-all"
            :class="activeTab === 'editor' ? 'bg-blue-50 dark:bg-blue-900/30 text-blue-600 dark:text-blue-400' : 'text-gray-500 hover:bg-gray-100 dark:hover:bg-gray-800'"
          >
            Editor
          </button>
          <button 
            @click="activeTab = 'settings'"
            class="px-4 py-2 rounded-lg text-sm font-bold transition-all"
            :class="activeTab === 'settings' ? 'bg-blue-50 dark:bg-blue-900/30 text-blue-600 dark:text-blue-400' : 'text-gray-500 hover:bg-gray-100 dark:hover:bg-gray-800'"
          >
            Settings
          </button>
        </nav>
      </div>

      <div class="flex items-center space-x-4">
        <div v-if="libraryStatus.is_scanning" class="flex items-center space-x-2 text-xs font-bold text-blue-600 animate-pulse">
            <div class="w-2 h-2 bg-blue-600 rounded-full"></div>
            <span>SCANNING LIBRARY...</span>
        </div>
        <button 
          @click="handleLibraryScan"
          :disabled="libraryStatus.is_scanning"
          class="p-2 hover:bg-gray-100 dark:hover:bg-gray-800 rounded-full transition-colors"
          title="Rescan Library"
        >
          <svg class="w-5 h-5 text-gray-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
          </svg>
        </button>
      </div>
    </header>

    <!-- Content Area -->
    <div class="flex-1 flex overflow-hidden relative">
      
      <!-- Setup Overlay -->
      <div v-if="isSetupRequired" class="absolute inset-0 bg-white/90 dark:bg-gray-950/90 backdrop-blur-sm z-50 flex items-center justify-center p-6">
        <div class="max-w-md w-full bg-white dark:bg-gray-900 rounded-3xl shadow-2xl border dark:border-gray-800 p-10 text-center space-y-8 animate-in zoom-in-95 duration-500">
           <div class="w-24 h-24 bg-blue-600 rounded-3xl flex items-center justify-center mx-auto rotate-12 shadow-xl shadow-blue-500/20">
              <svg class="w-12 h-12 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M3 7v10a2 2 0 002 2h14a2 2 0 002-2V9a2 2 0 00-2-2h-6l-2-2H5a2 2 0 00-2 2z" />
              </svg>
           </div>
           <div>
             <h2 class="text-3xl font-black tracking-tight mb-3">Welcome to CIXG</h2>
             <p class="text-gray-500 text-sm">Please set your manga root directory to begin managing your library.</p>
           </div>
           <div class="space-y-4">
             <input 
               v-model="config.manga_root_directory"
               type="text" 
               placeholder="Absolute path to manga folder..." 
               class="w-full px-6 py-4 bg-gray-50 dark:bg-gray-800 border-2 border-transparent focus:border-blue-600 rounded-2xl outline-none transition-all font-medium"
             />
             <button 
               @click="handleSaveConfig"
               class="w-full bg-blue-600 hover:bg-blue-700 text-white font-black py-4 rounded-2xl shadow-xl shadow-blue-500/30 active:scale-[0.98] transition-all"
             >
               Get Started
             </button>
           </div>
        </div>
      </div>

      <!-- Library Tab -->
      <main v-if="activeTab === 'library'" class="flex-1 overflow-y-auto p-10 custom-scrollbar">
        <div class="max-w-7xl mx-auto space-y-10">
            <header class="flex justify-between items-end">
                <div>
                    <h2 class="text-4xl font-black tracking-tighter">Your Library</h2>
                    <p class="text-gray-500 font-medium mt-2">{{ seriesList.length }} Series found in {{ libraryStatus.manga_root }}</p>
                </div>
            </header>
            
            <SeriesView :seriesList="seriesList" @select-series="handleSelectSeries" />
            
            <div v-if="seriesList.length === 0 && !libraryStatus.is_scanning" class="flex flex-col items-center justify-center py-20 text-center opacity-30">
                <svg class="w-20 h-20 mb-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10" />
                </svg>
                <p class="text-xl font-bold">No series found yet.</p>
                <p class="text-sm">Try rescanning your library.</p>
            </div>
        </div>
      </main>

      <!-- Editor Tab -->
      <div v-if="activeTab === 'editor'" class="flex-1 flex overflow-hidden">
        <!-- Sidebar -->
        <aside class="w-80 border-r bg-white dark:bg-gray-900 dark:border-gray-800 flex flex-col shrink-0">
          <div class="p-4 border-b dark:border-gray-800 bg-gray-50 dark:bg-gray-900/50">
            <div v-if="currentSeries" class="mb-4">
                <button @click="currentSeries = null; archives = []" class="text-[10px] font-bold text-blue-600 uppercase hover:underline mb-1 flex items-center">
                    <svg class="w-3 h-3 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path d="M15 19l-7-7 7-7" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>
                    Back to Library
                </button>
                <h3 class="font-black text-sm truncate">{{ currentSeries.name }}</h3>
            </div>
            <div v-else class="flex items-center space-x-2">
                <input 
                    v-model="directory"
                    type="text" 
                    placeholder="Quick scan path..." 
                    class="flex-1 text-xs px-3 py-2 border rounded-lg dark:bg-gray-800 dark:border-gray-700 outline-none"
                    @keyup.enter="handleScan"
                />
                <button @click="handleScan" class="p-2 bg-blue-600 text-white rounded-lg"><svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg></button>
            </div>
          </div>
          <div class="flex-1 overflow-y-auto p-3 custom-scrollbar">
            <ArchiveList 
              v-if="archives.length > 0"
              :files="archives" 
              @selection-changed="handleSelectionChanged"
            />
            <div v-else class="h-full flex flex-col items-center justify-center text-center p-8 opacity-20">
              <p class="text-xs font-bold uppercase tracking-widest">No files loaded</p>
            </div>
          </div>
        </aside>

        <!-- Main Editor -->
        <main class="flex-1 overflow-y-auto p-8 custom-scrollbar">
            <div class="max-w-4xl mx-auto h-full">
                <!-- Single selection editor -->
                <div v-if="currentComic && selectedPaths.length === 1" class="bg-white dark:bg-gray-900 rounded-3xl border dark:border-gray-800 shadow-xl flex flex-col overflow-hidden animate-in fade-in slide-in-from-bottom-4 duration-500">
                    <div class="px-8 py-6 border-b dark:border-gray-800 flex justify-between items-center bg-gray-50/50 dark:bg-gray-900/50">
                        <div class="min-w-0">
                            <h2 class="text-2xl font-black truncate">{{ currentComic.Title || 'Untitled' }}</h2>
                            <p class="text-[10px] text-gray-400 font-mono mt-1 truncate">{{ selectedPaths[0] }}</p>
                        </div>
                        <div class="flex items-center space-x-3 shrink-0 ml-4">
                            <div class="flex items-center border dark:border-gray-700 rounded-xl overflow-hidden bg-white dark:bg-gray-800">
                                <select v-model="scraperStrategy" class="bg-transparent text-[10px] font-black px-3 py-2 outline-none border-r dark:border-gray-700">
                                    <option value="local">LOCAL</option>
                                    <option value="llm">LLM</option>
                                </select>
                                <button @click="handleScrape" :disabled="isProcessing" class="text-[10px] bg-blue-50 dark:bg-blue-900/20 text-blue-600 dark:text-blue-400 px-4 py-2 font-black uppercase transition-all">SCRAPE</button>
                            </div>
                            <button @click="handleInject" :disabled="isProcessing" class="text-[10px] bg-green-600 hover:bg-green-700 text-white px-6 py-2 rounded-xl font-black uppercase shadow-lg shadow-green-500/20 transition-all">INJECT</button>
                        </div>
                    </div>
                    <div class="p-8">
                        <MetadataEditor v-model="currentComic" />
                    </div>
                </div>

                <!-- Multi-select / Empty states ... (simplified for brevity) -->
                <div v-else class="h-full flex flex-col items-center justify-center text-center opacity-20">
                    <h3 class="text-xl font-black">Select an archive to edit</h3>
                </div>
            </div>
        </main>
      </div>

      <!-- Settings Tab -->
      <main v-if="activeTab === 'settings'" class="flex-1 overflow-y-auto p-10 custom-scrollbar">
        <div class="max-w-2xl mx-auto space-y-12">
            <header>
                <h2 class="text-4xl font-black tracking-tighter">Settings</h2>
                <p class="text-gray-500 font-medium mt-2">Configure service behavior and scrapers.</p>
            </header>

            <section class="space-y-6">
                <div class="bg-white dark:bg-gray-900 rounded-3xl p-8 border dark:border-gray-800 shadow-sm space-y-6">
                    <h3 class="text-lg font-black flex items-center"><span class="w-8 h-8 bg-blue-100 dark:bg-blue-900/30 text-blue-600 rounded-lg flex items-center justify-center mr-3 text-sm">01</span> Project Paths</h3>
                    <div class="space-y-4">
                        <div class="space-y-2">
                            <label class="text-[10px] font-black uppercase tracking-widest text-gray-400">Manga Root Directory</label>
                            <input v-model="config.manga_root_directory" type="text" class="w-full px-4 py-3 bg-gray-50 dark:bg-gray-800 border-transparent rounded-xl outline-none focus:ring-2 focus:ring-blue-600 transition-all font-medium" />
                        </div>
                        <div class="space-y-2">
                            <label class="text-[10px] font-black uppercase tracking-widest text-gray-400">Data Directory (Database, Cache, Config)</label>
                            <input v-model="config.data_directory" type="text" class="w-full px-4 py-3 bg-gray-50 dark:bg-gray-800 border-transparent rounded-xl outline-none focus:ring-2 focus:ring-blue-600 transition-all font-medium" />
                        </div>
                    </div>
                </div>

                <div class="bg-white dark:bg-gray-900 rounded-3xl p-8 border dark:border-gray-800 shadow-sm space-y-6">
                    <h3 class="text-lg font-black flex items-center"><span class="w-8 h-8 bg-purple-100 dark:bg-purple-900/30 text-purple-600 rounded-lg flex items-center justify-center mr-3 text-sm">02</span> LLM Configuration</h3>
                    <div class="grid grid-cols-2 gap-4">
                        <div class="space-y-2 col-span-2">
                            <label class="text-[10px] font-black uppercase tracking-widest text-gray-400">Base URL</label>
                            <input v-model="config.llm_base_url" type="text" class="w-full px-4 py-3 bg-gray-50 dark:bg-gray-800 border-transparent rounded-xl outline-none focus:ring-2 focus:ring-blue-600 transition-all font-medium" />
                        </div>
                        <div class="space-y-2">
                            <label class="text-[10px] font-black uppercase tracking-widest text-gray-400">Model Name</label>
                            <input v-model="config.llm_model" type="text" class="w-full px-4 py-3 bg-gray-50 dark:bg-gray-800 border-transparent rounded-xl outline-none focus:ring-2 focus:ring-blue-600 transition-all font-medium" />
                        </div>
                        <div class="space-y-2">
                            <label class="text-[10px] font-black uppercase tracking-widest text-gray-400">API Key</label>
                            <input v-model="config.llm_api_key" type="password" class="w-full px-4 py-3 bg-gray-50 dark:bg-gray-800 border-transparent rounded-xl outline-none focus:ring-2 focus:ring-blue-600 transition-all font-medium" />
                        </div>
                    </div>
                </div>

                <div class="bg-white dark:bg-gray-900 rounded-3xl p-8 border dark:border-gray-800 shadow-sm space-y-6">
                    <h3 class="text-lg font-black flex items-center"><span class="w-8 h-8 bg-green-100 dark:bg-green-900/30 text-green-600 rounded-lg flex items-center justify-center mr-3 text-sm">03</span> Library Automation</h3>
                    <div class="flex items-center justify-between p-4 bg-gray-50 dark:bg-gray-800 rounded-2xl">
                        <div>
                            <p class="font-bold">Background Scanning</p>
                            <p class="text-[10px] text-gray-500 font-medium">Periodically scan for new archives</p>
                        </div>
                        <label class="relative inline-flex items-center cursor-pointer">
                            <input type="checkbox" v-model="config.auto_scan_enabled" class="sr-only peer">
                            <div class="w-11 h-6 bg-gray-200 peer-focus:outline-none rounded-full peer dark:bg-gray-700 peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all dark:border-gray-600 peer-checked:bg-blue-600"></div>
                        </label>
                    </div>
                    <div v-if="config.auto_scan_enabled" class="space-y-2">
                        <label class="text-[10px] font-black uppercase tracking-widest text-gray-400">Scan Interval (Minutes)</label>
                        <input v-model.number="config.auto_scan_interval_minutes" type="number" min="1" class="w-full px-4 py-3 bg-gray-50 dark:bg-gray-800 border-transparent rounded-xl outline-none focus:ring-2 focus:ring-blue-600 transition-all font-medium" />
                    </div>
                </div>

                <button 
                  @click="handleSaveConfig"
                  class="w-full bg-blue-600 hover:bg-blue-700 text-white font-black py-4 rounded-2xl shadow-xl shadow-blue-500/20 active:scale-[0.98] transition-all"
                >
                  Save Settings
                </button>
            </section>
        </div>
      </main>

      <!-- Log Panel Overlay (Sticky Bottom) -->
      <section class="absolute bottom-0 left-0 right-0 flex justify-center p-6 pointer-events-none z-30">
        <div class="w-full max-w-4xl bg-black/90 backdrop-blur-xl border border-white/10 rounded-t-3xl rounded-b-xl shadow-2xl flex flex-col overflow-hidden pointer-events-auto transition-all duration-500 ease-in-out h-10 hover:h-64 opacity-40 hover:opacity-100 group translate-y-2 hover:translate-y-0">
          <div class="h-10 px-6 flex justify-between items-center bg-white/5 shrink-0 cursor-pointer">
            <div class="flex items-center space-x-3">
              <div class="w-1.5 h-1.5 bg-blue-500 rounded-full animate-pulse"></div>
              <h3 class="text-[10px] font-black uppercase tracking-[0.2em] text-gray-400">Live Service Console</h3>
            </div>
            <button @click.stop="logs = []" class="text-[10px] uppercase font-bold text-gray-500 hover:text-white transition-colors">Flush Output</button>
          </div>
          <div class="flex-1 overflow-y-auto p-6 font-mono text-[11px] leading-relaxed text-gray-400 custom-scrollbar border-t border-white/5">
            <div v-for="(log, i) in logs" :key="i" class="mb-1.5 flex items-start group/line">
              <span class="text-blue-500/30 mr-3 shrink-0 select-none">{{ log.time }}</span>
              <span :class="{ 'text-green-400': log.type === 'info', 'text-red-400': log.type === 'error', 'text-yellow-400': log.type === 'warn', 'text-blue-400': log.type === 'tech' }" class="break-all">
                {{ log.msg }}
              </span>
            </div>
            <div v-if="logs.length === 0" class="text-gray-700 italic h-32 flex items-center justify-center">Waiting for system events...</div>
          </div>
        </div>
      </section>

    </div>
  </div>
</template>

<style>
/* Custom animations and scrollbars ... */
.custom-scrollbar::-webkit-scrollbar { width: 4px; }
.custom-scrollbar::-webkit-scrollbar-track { background: transparent; }
.custom-scrollbar::-webkit-scrollbar-thumb { background: rgba(156, 163, 175, 0.2); border-radius: 10px; }
</style>
