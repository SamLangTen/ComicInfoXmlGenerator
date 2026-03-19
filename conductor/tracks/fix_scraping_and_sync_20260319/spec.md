# Bug Fix Specification: Scraper Integration & UI Synchronization

## Overview
修复 Task 系统引入后 LLM 和 博客来 (Books) 抓取器出现的集成缺陷。主要表现为：前端状态更新与后端元数据落库不一致（需要重启后端才能生效），以及博客来抓取过程中的日志捕获失效。

## Functional Requirements
1. **元数据持久化即时生效**：任务完成后，元数据应立即写入 SQLite 数据库，并确保后端后续的读取请求能拿到最新值，无需重启服务。
2. **前端数据同步**：任务状态变为 `completed` 后，前端相关的档案（Archives）列表应能展示最新的元数据（或提示用户刷新）。
3. **日志全量捕获**：
   - 修复 `BooksScraper` 的日志通过 Task 管道实时推送的功能。
   - 确保 `scrape_task_handler` 捕获并记录抓取过程中的所有关键步骤。
4. **Scraper 稳定性增强**：
   - 确保 LLM 抓取器在配置缺失（API Key）时提供明确的错误日志。
   - 优化 `BooksScraper` 的 403 错误处理和重定向逻辑。

## Acceptance Criteria
- [ ] 运行一个 LLM 抓取任务，任务完成后，刷新前端列表，元数据立即更新（无需重启 `cixg.py`）。
- [ ] 运行一个 博客来 抓取任务，在 UI 的“任务详情”模态框中能实时看到抓取进度日志。
- [ ] 单元测试验证 `scrape_task_handler` 在各种异常情况下（网络错误、元数据提取不全）能正确更新任务结果。
