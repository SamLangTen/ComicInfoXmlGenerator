<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { apiService } from '../services/api'
import ProgressBar from './ProgressBar.vue'

const tasks = ref<any[]>([])
const filter = ref<string>('')
const isLoading = ref(false)

const fetchTasks = async () => {
  isLoading.value = true
  try {
    tasks.value = await apiService.getTasks(filter.value || undefined)
  } catch (err) {
    console.error('Failed to fetch tasks', err)
  } finally {
    isLoading.value = false
  }
}

const handleRetry = async (taskId: number) => {
  try {
    await apiService.retryTask(taskId)
    await fetchTasks()
  } catch (err) {
    console.error('Failed to retry task', err)
  }
}

const handleClearCompleted = async () => {
  try {
    await apiService.clearCompletedTasks()
    await fetchTasks()
  } catch (err) {
    console.error('Failed to clear completed tasks', err)
  }
}

const getStatusColor = (status: string) => {
  switch (status) {
    case 'pending': return 'text-gray-400 bg-gray-100 dark:bg-gray-800'
    case 'running': return 'text-blue-600 bg-blue-50 dark:bg-blue-900/30'
    case 'completed': return 'text-green-600 bg-green-50 dark:bg-green-900/30'
    case 'failed': return 'text-red-600 bg-red-50 dark:bg-red-900/30'
    default: return 'text-gray-400 bg-gray-100'
  }
}

// Global event bus or just listen to the same socket?
// For now, let's just listen to a simple custom event if we implement one, 
// or tell the parent to notify us.
// But to keep it simple, let's expose a refresh method.
defineExpose({
  refresh: fetchTasks,
  handleTaskUpdate: (updatedTask: any) => {
    const index = tasks.value.findIndex(t => t.id === updatedTask.id)
    if (index !== -1) {
      tasks.value[index] = updatedTask
    } else {
      // If it's a new task and we're showing all or pending, add it to the top
      if (!filter.value || filter.value === updatedTask.status) {
        tasks.value.unshift(updatedTask)
        if (tasks.value.length > 100) tasks.value.pop()
      }
    }
  }
})

onMounted(fetchTasks)
</script>

<template>
  <div class="space-y-10">
    <header class="flex justify-between items-end">
      <div>
        <h2 class="text-4xl font-black tracking-tighter">Background Tasks</h2>
        <p class="text-gray-500 font-medium mt-2">Monitor and manage metadata scraping jobs.</p>
      </div>
      <div class="flex items-center space-x-4">
        <button 
          @click="handleClearCompleted"
          class="px-6 py-3 bg-gray-100 dark:bg-gray-800 hover:bg-gray-200 dark:hover:bg-gray-700 rounded-2xl font-bold text-xs transition-all"
        >
          Clear Completed
        </button>
        <button 
          @click="fetchTasks"
          :disabled="isLoading"
          class="p-3 bg-blue-600 text-white rounded-2xl shadow-lg shadow-blue-500/20 hover:scale-105 active:scale-95 transition-all"
        >
          <svg class="w-5 h-5" :class="{ 'animate-spin': isLoading }" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
          </svg>
        </button>
      </div>
    </header>

    <!-- Filters -->
    <div class="flex items-center space-x-2">
      <button 
        v-for="f in ['', 'pending', 'running', 'completed', 'failed']" 
        :key="f"
        @click="filter = f; fetchTasks()"
        class="px-4 py-2 rounded-xl text-xs font-black uppercase tracking-widest transition-all border-2"
        :class="filter === f ? 'bg-blue-600 border-blue-600 text-white shadow-lg shadow-blue-500/20' : 'border-transparent text-gray-500 hover:bg-gray-100 dark:hover:bg-gray-800'"
      >
        {{ f || 'All' }}
      </button>
    </div>

    <!-- Task List -->
    <div class="bg-white dark:bg-gray-900 rounded-3xl border dark:border-gray-800 shadow-sm overflow-hidden">
      <table class="w-full text-left border-collapse">
        <thead>
          <tr class="text-[10px] font-black uppercase tracking-[0.2em] text-gray-400 border-b dark:border-gray-800">
            <th class="px-8 py-6">Task</th>
            <th class="px-8 py-6">Target</th>
            <th class="px-8 py-6">Status</th>
            <th class="px-8 py-6 text-right">Actions</th>
          </tr>
        </thead>
        <tbody class="divide-y dark:divide-gray-800">
          <tr v-for="task in tasks" :key="task.id" class="group hover:bg-gray-50/50 dark:hover:bg-gray-800/30 transition-colors">
            <td class="px-8 py-6">
              <div class="font-bold text-sm">#{{ task.id }} {{ task.type }}</div>
              <div class="text-[10px] text-gray-400 font-mono mt-1">{{ task.created_at }}</div>
            </td>
            <td class="px-8 py-6">
              <div class="text-xs font-medium truncate max-w-xs" :title="task.target">
                {{ task.target.split(/[\/]/).pop() }}
              </div>
              <div class="text-[10px] text-gray-400 truncate max-w-xs mt-1">{{ task.target }}</div>
            </td>
            <td class="px-8 py-6">
              <div class="flex flex-col space-y-2">
                <span class="px-3 py-1 rounded-full text-[10px] font-black uppercase tracking-wider w-fit" :class="getStatusColor(task.status)">
                  {{ task.status }}
                </span>
                <ProgressBar 
                  :value="task.status === 'completed' ? 100 : (task.status === 'running' ? 50 : 0)" 
                  :max="100" 
                  :color="task.status === 'failed' ? 'bg-red-500' : (task.status === 'completed' ? 'bg-green-500' : 'bg-blue-600')"
                  :animated="task.status === 'running'"
                />
              </div>
              <div v-if="task.retries > 0" class="text-[10px] text-orange-500 font-bold mt-1">
                Retry: {{ task.retries }}
              </div>
            </td>
            <td class="px-8 py-6 text-right">
              <div v-if="task.status === 'failed'" class="flex justify-end space-x-2 opacity-0 group-hover:opacity-100 transition-opacity">
                <button 
                  @click="handleRetry(task.id)"
                  class="p-2 text-blue-600 hover:bg-blue-50 dark:hover:bg-blue-900/30 rounded-lg transition-colors"
                  title="Retry Task"
                >
                  <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
                  </svg>
                </button>
              </div>
              <div v-if="task.status === 'running'" class="flex justify-end">
                <div class="w-4 h-4 border-2 border-blue-600 border-t-transparent rounded-full animate-spin"></div>
              </div>
            </td>
          </tr>
          <tr v-if="tasks.length === 0">
            <td colspan="4" class="px-8 py-20 text-center text-gray-400 italic">
              No tasks found.
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>
