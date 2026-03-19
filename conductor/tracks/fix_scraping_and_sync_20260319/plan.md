# Implementation Plan: Scraper Fix & UI Metadata Sync

## Phase 1: Task Logger and Error Handling
- [x] Task: 修复 `scrape_task_handler` 的日志捕获器（logger），确保它将所有抓取器的 `log_callback` 转发至 UI 任务详情。 (767f5a6)
- [x] Task: 为 `BooksScraper` 引入详细的异常捕获日志（捕获 403, 503 等 HTTP 状态码并在任务结果中反馈）。 (767f5a6)
- [x] Task: 修复 `LlmFilenameScraper` 在任务线程中的环境变量加载逻辑，防止 API Key 丢失。 (767f5a6)
- [x] Task: **Write Tests**: `test/test_task_logging.py` 验证任务完成后，其结果（Result）字段包含完整的运行日志。 (767f5a6)
- [ ] Task: Conductor - User Manual Verification 'Phase 1' (Protocol in workflow.md)

## Phase 2: Database Persistence and State Sync
- [x] Task: 调查并修复 `DatabaseManager` 的数据持久化和锁机制，确保写入操作立即生效。 (ff6d765)
- [x] Task: 引入“库管理器（LibraryManager）同步协议”：任务完成后，自动触发后端内存状态的刷新，或让 API 直接查询数据库而非内存缓存。 (ff6d765)
- [x] Task: 修复 `src/task_manager.py` 中的 `scrape_task_handler` 对元数据变更的提交（Commit）时机。 (ff6d765)
- [x] Task: **Write Tests**: `test/test_db_sync.py` 模拟多线程环境下，Task 完成后的即时读取。 (ff6d765)
- [ ] Task: Conductor - User Manual Verification 'Phase 2' (Protocol in workflow.md)

## Phase 3: Frontend Polling and Refresh Logic
- [x] Task: 优化 Vue 前端的任务轮询（Polling）或 WebSocket 回调：当检测到任务 `completed` 时，自动触发档案（Archive）列表的数据重新拉取。 (6ab677f)
- [x] Task: 改进 Web UI 的 `ArchiveDetails` 组件，支持在打开状态下响应元数据的动态变化。 (6ab677f)
- [ ] Task: Conductor - User Manual Verification 'Phase 3' (Protocol in workflow.md)
