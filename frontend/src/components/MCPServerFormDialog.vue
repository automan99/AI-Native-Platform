<template>
  <transition name="modal">
    <div v-if="dialogVisible" class="modal-overlay" @click.self="closeDialog">
      <div class="dialog-modal dialog-modal--wizard">
        <div class="dialog-header">
          <h3>{{ isEdit ? '编辑' : '添加' }} MCP Server</h3>
          <button class="dialog-close" @click="closeDialog">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
              <path d="M18 6L6 18M6 6l12 12"/>
            </svg>
          </button>
        </div>

        <!-- 步骤指示器 -->
        <div class="wizard-steps">
          <div
            v-for="(step, index) in steps"
            :key="index"
            class="wizard-step"
            :class="{
              'wizard-step--active': currentStep === index,
              'wizard-step--completed': currentStep > index
            }"
          >
            <div class="wizard-step__circle">
              <svg v-if="currentStep > index" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
                <path d="M5 13l4 4L19 7"/>
              </svg>
              <span v-else>{{ index + 1 }}</span>
            </div>
            <span class="wizard-step__label">{{ step }}</span>
          </div>
        </div>

        <div class="dialog-body dialog-body--wizard">
          <!-- 步骤 1: 基础信息 -->
          <div v-show="currentStep === 0" class="wizard-panel">
            <div class="wizard-panel__title">基础信息</div>
            <div class="wizard-panel__desc">配置 MCP Server 的基本识别信息</div>

            <div class="form-field">
              <label class="form-label">Server 名称 <span class="required">*</span></label>
              <input v-model="form.name" class="form-input" placeholder="例如: Filesystem MCP" />
            </div>

            <div class="form-field">
              <label class="form-label">描述</label>
              <textarea v-model="form.description" class="form-textarea" rows="5" placeholder="描述此 MCP Server 的用途和功能..."></textarea>
            </div>
          </div>

          <!-- 步骤 2: 传输配置 -->
          <div v-show="currentStep === 1" class="wizard-panel">
            <div class="wizard-panel__title">传输配置</div>
            <div class="wizard-panel__desc">选择 MCP Server 的通信方式</div>

            <div class="radio-cards">
              <label class="radio-card" :class="{ 'radio-card--active': form.transport_type === 'stdio' }">
                <input type="radio" v-model="form.transport_type" value="stdio" />
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                  <path d="M4 4v16h16V4H4z"/>
                  <path d="M9 9h6M9 13h6M9 5v14"/>
                </svg>
                <span>stdio</span>
                <small>标准输入输出</small>
              </label>
              <label class="radio-card" :class="{ 'radio-card--active': form.transport_type === 'http' }">
                <input type="radio" v-model="form.transport_type" value="http" />
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                  <circle cx="12" cy="12" r="10"/>
                  <path d="M2 12h2M20 12h2M12 2v2M12 20v2"/>
                </svg>
                <span>http</span>
                <small>HTTP 传输</small>
              </label>
            </div>
          </div>

          <!-- 步骤 3: 连接配置 -->
          <div v-show="currentStep === 2" class="wizard-panel">
            <div class="wizard-panel__title">连接配置</div>
            <div class="wizard-panel__desc">配置 {{ form.transport_type === 'stdio' ? '命令行' : 'HTTP' }} 连接参数</div>

            <!-- stdio 配置 -->
            <template v-if="form.transport_type === 'stdio'">
              <div class="form-field">
                <label class="form-label">启动命令 <span class="required">*</span></label>
                <input v-model="form.command" class="form-input form-input--mono" placeholder="npx" />
                <small class="form-hint">MCP Server 的启动命令，如 npx, node, python 等</small>
              </div>

              <div class="form-field">
                <label class="form-label">命令参数</label>
                <input v-model="form.arguments_str" class="form-input form-input--mono" placeholder="-y @modelcontextprotocol/server-filesystem /path" />
                <small class="form-hint">命令行参数，多个参数用空格分隔</small>
              </div>

              <div class="form-field">
                <label class="form-label">环境变量 (每行一个 KEY=VALUE)</label>
                <textarea v-model="form.env_str" class="form-textarea form-textarea--mono" rows="3" placeholder="NODE_ENV=production&#10;API_KEY=your_key"></textarea>
                <small class="form-hint">需要传递给 MCP Server 进程的环境变量</small>
              </div>
            </template>

            <!-- http 配置 -->
            <template v-if="form.transport_type === 'http'">
              <div class="form-field">
                <label class="form-label">Server URL <span class="required">*</span></label>
                <input v-model="form.url" class="form-input form-input--mono" placeholder="https://example.com/mcp" />
                <small class="form-hint">MCP Server 的 HTTP 服务地址</small>
              </div>
            </template>

            <div class="form-field">
              <label class="form-label">超时时间 (秒)</label>
              <input v-model.number="form.timeout" type="number" class="form-input" min="5" max="300" />
              <small class="form-hint">连接和操作的超时时间</small>
            </div>
          </div>

          <!-- 步骤 4: 同步配置 -->
          <div v-show="currentStep === 3" class="wizard-panel">
            <div class="wizard-panel__title">同步配置</div>
            <div class="wizard-panel__desc">选择 MCP Server 资源的同步方式</div>

            <div class="radio-cards">
              <label class="radio-card" :class="{ 'radio-card--active': form.sync_mode === 'manual' }">
                <input type="radio" v-model="form.sync_mode" value="manual" />
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                  <circle cx="12" cy="12" r="10"/><path d="M12 6v6l4 2"/>
                </svg>
                <span>手动同步</span>
                <small>手动触发</small>
              </label>
              <label class="radio-card" :class="{ 'radio-card--active': form.sync_mode === 'scheduled' }">
                <input type="radio" v-model="form.sync_mode" value="scheduled" />
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                  <path d="M12 2v4M12 18v4M4.93 4.93l2.83 2.83M16.24 16.24l2.83 2.83M2 12h4M18 12h4"/>
                </svg>
                <span>定时同步</span>
                <small>自动定时</small>
              </label>
              <label class="radio-card" :class="{ 'radio-card--active': form.sync_mode === 'webhook' }">
                <input type="radio" v-model="form.sync_mode" value="webhook" />
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                  <path d="M10 13a5 5 0 0 0 7.54.54l3-3a5 5 0 0 0-7.07-7.07l-1.72 1.71"/>
                </svg>
                <span>Webhook</span>
                <small>推送触发</small>
              </label>
            </div>

            <div v-if="form.sync_mode === 'scheduled'" class="form-field">
              <label class="form-label">同步间隔（分钟）<span class="required">*</span></label>
              <input v-model.number="form.sync_interval" type="number" class="form-input" min="1" placeholder="60" />
              <small class="form-hint">系统将按此间隔自动同步 MCP Server 资源</small>
            </div>

            <div v-if="form.sync_mode === 'webhook'">
              <div class="form-field">
                <label class="form-label">Webhook 密钥 <span class="required">*</span></label>
                <input v-model="form.webhook_secret" type="password" class="form-input form-input--mono" placeholder="输入密钥" />
                <small class="form-hint">用于验证 Webhook 请求的密钥</small>
              </div>
              <div class="form-field">
                <label class="form-label">Webhook 回调地址</label>
                <input v-model="form.webhook_url" class="form-input form-input--mono" placeholder="https://your-domain.com/webhook" />
                <small class="form-hint">接收 Git 推送通知的服务地址</small>
              </div>
            </div>
          </div>

          <!-- 步骤 5: 确认配置 -->
          <div v-show="currentStep === 4" class="wizard-panel">
            <div class="wizard-panel__title">确认配置</div>
            <div class="wizard-panel__desc">请确认以下配置信息无误</div>

            <div class="config-summary">
              <div class="config-section">
                <div class="config-section__title">基础信息</div>
                <div class="config-item">
                  <span class="config-item__label">Server 名称</span>
                  <span class="config-item__value">{{ form.name || '-' }}</span>
                </div>
                <div v-if="form.description" class="config-item">
                  <span class="config-item__label">描述</span>
                  <span class="config-item__value">{{ form.description }}</span>
                </div>
              </div>

              <div class="config-section">
                <div class="config-section__title">传输配置</div>
                <div class="config-item">
                  <span class="config-item__label">传输类型</span>
                  <span class="config-item__value config-item__value--badge" :class="`badge--${form.transport_type}`">{{ form.transport_type.toUpperCase() }}</span>
                </div>
              </div>

              <div class="config-section">
                <div class="config-section__title">连接配置</div>
                <template v-if="form.transport_type === 'stdio'">
                  <div class="config-item">
                    <span class="config-item__label">启动命令</span>
                    <span class="config-item__value config-item__value--mono">{{ form.command || '-' }}</span>
                  </div>
                  <div v-if="form.arguments_str" class="config-item">
                    <span class="config-item__label">命令参数</span>
                    <span class="config-item__value config-item__value--mono">{{ form.arguments_str }}</span>
                  </div>
                  <div v-if="form.env_str" class="config-item">
                    <span class="config-item__label">环境变量</span>
                    <span class="config-item__value config-item__value--mono">{{ form.env_str }}</span>
                  </div>
                </template>
                <template v-if="form.transport_type === 'http'">
                  <div class="config-item">
                    <span class="config-item__label">Server URL</span>
                    <span class="config-item__value config-item__value--mono">{{ form.url || '-' }}</span>
                  </div>
                </template>
                <div class="config-item">
                  <span class="config-item__label">超时时间</span>
                  <span class="config-item__value">{{ form.timeout }} 秒</span>
                </div>
              </div>

              <div class="config-section">
                <div class="config-section__title">同步配置</div>
                <div class="config-item">
                  <span class="config-item__label">同步方式</span>
                  <span class="config-item__value">{{ getSyncModeText(form.sync_mode) }}</span>
                </div>
                <div v-if="form.sync_mode === 'scheduled'" class="config-item">
                  <span class="config-item__label">同步间隔</span>
                  <span class="config-item__value">{{ form.sync_interval }} 分钟</span>
                </div>
                <div v-if="form.sync_mode === 'webhook' && form.webhook_url" class="config-item">
                  <span class="config-item__label">回调地址</span>
                  <span class="config-item__value config-item__value--mono">{{ form.webhook_url }}</span>
                </div>
              </div>

              <div class="config-section">
                <div class="config-section__title">状态配置</div>
                <div class="config-item">
                  <span class="config-item__label">启用状态</span>
                  <span class="config-item__value config-item__value--status" :class="form.enabled ? 'status-enabled' : 'status-disabled'">
                    {{ form.enabled ? '启用' : '禁用' }}
                  </span>
                </div>
              </div>
            </div>
          </div>
        </div>

        <div class="dialog-footer dialog-footer--wizard">
          <button v-if="currentStep > 0" class="btn btn--secondary" @click="previousStep">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M15 18l-6-6 6-6"/>
            </svg>
            上一步
          </button>
          <button v-else class="btn btn--secondary" @click="closeDialog">取消</button>
          <button v-if="currentStep < steps.length - 1" class="btn btn--primary" @click="nextStep" :disabled="!canProceed">
            下一步
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M9 18l6-6-6-6"/>
            </svg>
          </button>
          <button v-else class="btn btn--primary" @click="handleSubmit" :disabled="submitting">
            <svg v-if="!submitting" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M5 13l4 4L19 7"/>
            </svg>
            <span v-if="submitting">保存中...</span>
            <span v-else>完成</span>
          </button>
        </div>
      </div>
    </div>
  </transition>
</template>

<style>
/* 模态框动画 */
.modal-enter-active,
.modal-leave-active {
  transition: opacity 0.2s;
}

.modal-enter-from,
.modal-leave-to {
  opacity: 0;
}

.modal-enter-from .dialog-modal,
.modal-leave-to .dialog-modal {
  transform: scale(0.96);
}

/* 模态框容器 */
.modal-overlay {
  position: fixed !important;
  inset: 0 !important;
  background: rgba(0, 0, 0, 0.6);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 9999 !important;
  padding: 16px;
}

.dialog-modal {
  background: #1e1e1e;
  border: 1px solid #333333;
  border-radius: 12px;
  width: 100%;
  max-width: 560px;
  max-height: 90vh;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.dialog-modal--wizard {
  max-width: 640px;
}

.dialog-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 16px 20px;
  border-bottom: 1px solid #333;
}

.dialog-header h3 {
  font-size: 16px;
  font-weight: 600;
  color: #fff;
  margin: 0;
}

.dialog-close {
  width: 28px;
  height: 28px;
  border: none;
  background: none;
  border-radius: 6px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #888;
  cursor: pointer;
  transition: all 0.15s ease;
}

.dialog-close:hover {
  background: #222;
  color: #fff;
}

.dialog-close svg {
  width: 16px;
  height: 16px;
}

.dialog-body {
  padding: 20px;
  overflow-y: auto;
  flex: 1;
}

.dialog-body--wizard {
  padding: 0;
}

.dialog-body::-webkit-scrollbar {
  width: 6px;
}

.dialog-body::-webkit-scrollbar-track {
  background: #1e1e1e;
}

.dialog-body::-webkit-scrollbar-thumb {
  background: #333;
  border-radius: 3px;
}

.dialog-footer {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
  padding: 16px 20px;
  border-top: 1px solid #333;
  background: #1e1e1e;
}

.dialog-footer--wizard {
  justify-content: space-between;
}

/* 向导步骤 */
.wizard-steps {
  display: flex;
  gap: 8px;
  padding: 20px;
  border-bottom: 1px solid var(--color-border);
}

.wizard-step {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 6px;
  flex: 1;
  max-width: 100px;
}

.wizard-step__circle {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  background: var(--color-bg-tertiary);
  border: 2px solid var(--color-border);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 14px;
  font-weight: 500;
  color: var(--color-text-muted);
  transition: all var(--transition-base);
}

.wizard-step--active .wizard-step__circle {
  border-color: var(--color-blue);
  background: var(--color-blue-glow);
  color: var(--color-blue);
}

.wizard-step--completed .wizard-step__circle {
  border-color: var(--color-green);
  background: rgba(0, 255, 0, 0.15);
  color: var(--color-green);
}

.wizard-step--completed .wizard-step__circle svg {
  width: 16px;
  height: 16px;
}

.wizard-step__label {
  font-size: 12px;
  color: var(--color-text-muted);
  text-align: center;
}

.wizard-step--active .wizard-step__label {
  color: var(--color-text-primary);
  font-weight: 500;
}

/* 向导面板 */
.wizard-panel {
  padding: 20px;
}

.wizard-panel__title {
  font-size: 16px;
  font-weight: 600;
  color: var(--color-text-primary);
  margin-bottom: 4px;
}

.wizard-panel__desc {
  font-size: 13px;
  color: var(--color-text-secondary);
  margin-bottom: 20px;
}

/* 表单 */
.form-field {
  margin-bottom: 16px;
}

.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 12px;
}

.form-label {
  display: block;
  font-size: 13px;
  font-weight: 500;
  color: var(--color-text-secondary);
  margin-bottom: 6px;
}

.required {
  color: var(--color-red);
}

.form-input,
.form-textarea {
  width: 100%;
  box-sizing: border-box;
  padding: 10px 12px;
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
  font-size: 14px;
  color: var(--color-text-primary);
  background: var(--color-bg-primary);
  transition: border-color var(--transition-base);
}

.form-input--mono,
.form-textarea--mono {
  font-family: 'Consolas', 'Monaco', 'Courier New', monospace;
  font-size: 12px;
}

.form-input:focus,
.form-textarea:focus {
  outline: none;
  border-color: var(--color-blue);
}

.form-input::placeholder,
.form-textarea::placeholder {
  color: var(--color-text-muted);
}

.form-input:disabled {
  background: var(--color-bg-tertiary);
  cursor: not-allowed;
  color: var(--color-text-muted);
}

.form-textarea {
  resize: vertical;
  min-height: 80px;
  font-family: inherit;
}

.form-hint {
  display: block;
  font-size: 12px;
  color: var(--color-text-muted);
  margin-top: 4px;
}

/* 单选卡片 */
.radio-cards {
  display: flex;
  gap: 12px;
}

.radio-card {
  position: relative;
  flex: 1;
}

.radio-card input {
  position: absolute;
  opacity: 0;
  pointer-events: none;
}

.radio-card > span {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 6px;
  padding: 16px;
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
  cursor: pointer;
  transition: all var(--transition-base);
  text-align: center;
  background: var(--color-bg-primary);
}

.radio-card svg {
  width: 28px;
  height: 28px;
  color: var(--color-text-muted);
}

.radio-card span span {
  font-size: 14px;
  font-weight: 500;
  color: var(--color-text-secondary);
}

.radio-card small {
  font-size: 11px;
  color: var(--color-text-muted);
}

.radio-card:hover > span {
  background: var(--color-bg-hover);
  border-color: var(--color-border-light);
}

.radio-card--active > span {
  border-color: var(--color-blue);
  background: var(--color-blue-glow);
}

.radio-card--active svg {
  color: var(--color-blue);
}

.radio-card--active span span {
  color: var(--color-blue);
}

/* 配置摘要 */
.config-summary {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.config-section {
  background: #121212;
  border: 1px solid #333;
  border-radius: 8px;
  overflow: hidden;
}

.config-section__title {
  font-size: 13px;
  font-weight: 500;
  color: #888;
  padding: 10px 16px;
  background: #1a1a1a;
  border-bottom: 1px solid #333;
}

.config-item {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  padding: 12px 16px;
  border-bottom: 1px solid #222;
}

.config-item:last-child {
  border-bottom: none;
}

.config-item__label {
  font-size: 13px;
  color: #888;
  flex-shrink: 0;
  width: 80px;
}

.config-item__value {
  font-size: 13px;
  color: #fff;
  text-align: right;
  word-break: break-all;
}

.config-item__value--mono {
  font-family: 'Consolas', 'Monaco', 'Courier New', monospace;
  font-size: 12px;
}

.config-item__value--badge {
  padding: 3px 10px;
  border-radius: 4px;
  font-size: 11px;
  font-weight: 500;
}

.badge--stdio {
  background: rgba(59, 130, 246, 0.15);
  color: #3b82f6;
}

.badge--http {
  background: rgba(16, 185, 129, 0.15);
  color: #10b981;
}

.config-item__value--status {
  font-weight: 500;
}

.status-enabled {
  color: #10b981;
}

.status-disabled {
  color: #888;
}

/* 按钮 */
.btn {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 10px 16px;
  border-radius: var(--radius-md);
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  border: none;
  transition: all var(--transition-base);
}

.btn svg {
  width: 18px;
  height: 18px;
}

.btn--primary {
  background: var(--color-blue);
  color: white;
}

.btn--primary:hover:not(:disabled) {
  background: var(--color-blue-light);
}

.btn--secondary {
  background: transparent;
  color: var(--color-text-secondary);
  border: 1px solid var(--color-border);
}

.btn--secondary:hover {
  background: var(--color-bg-hover);
  border-color: var(--color-border-light);
  color: var(--color-text-primary);
}

.btn:disabled {
  opacity: 0.4;
  cursor: not-allowed;
}

/* 响应式 */
@media (max-width: 640px) {
  .dialog-modal {
    max-width: 100%;
    border-radius: 12px;
  }

  .wizard-steps {
    padding: 16px;
  }

  .wizard-step {
    max-width: 60px;
  }

  .wizard-step__label {
    font-size: 10px;
  }

  .wizard-panel {
    padding: 16px;
  }

  .radio-cards {
    flex-direction: column;
  }

  .form-row {
    grid-template-columns: 1fr;
  }
}
</style>

<script setup>
import { ref, watch, computed } from 'vue'
import { mcpApi } from '@/api/mcp'
import { notify } from '@/utils/notification'

const props = defineProps({
  visible: {
    type: Boolean,
    default: false
  },
  editServer: {
    type: Object,
    default: null
  }
})

const emit = defineEmits(['update:visible', 'success'])

const dialogVisible = ref(false)
const isEdit = ref(false)
const submitting = ref(false)
const currentEditId = ref(null)
const currentStep = ref(0)

const steps = ['基础信息', '传输配置', '连接配置', '同步配置', '确认配置']

const form = ref({
  name: '',
  description: '',
  transport_type: 'stdio',
  command: '',
  arguments_str: '',
  env_str: '',
  url: '',
  timeout: 30,
  sync_mode: 'manual',
  sync_interval: 60,
  webhook_secret: '',
  webhook_url: '',
  enabled: true
})

const hasWebhookSecret = ref(false)

// 当前步骤是否可以继续
const canProceed = computed(() => {
  switch (currentStep.value) {
    case 0:
      return form.value.name && form.value.name.trim()
    case 1:
      return form.value.transport_type
    case 2:
      if (form.value.transport_type === 'stdio' && !form.value.command) return false
      if (form.value.transport_type === 'http' && !form.value.url) return false
      if (!form.value.timeout || form.value.timeout < 5) return false
      return true
    case 3:
      if (form.value.sync_mode === 'scheduled' && !form.value.sync_interval) return false
      if (form.value.sync_mode === 'webhook' && !form.value.webhook_secret && !hasWebhookSecret.value) return false
      return true
    default:
      return true
  }
})

// 监听 visible 变化
watch(() => props.visible, (newVal) => {
  dialogVisible.value = newVal
  if (newVal) {
    if (props.editServer) {
      loadEditData(props.editServer)
    } else {
      resetForm()
    }
  }
})

// 监听 dialogVisible 变化，同步到父组件
watch(dialogVisible, (newVal) => {
  if (newVal !== props.visible) {
    emit('update:visible', newVal)
  }
})

// 将字符串参数转换为数组
function parseArguments(str) {
  if (!str || !str.trim()) return []
  return str.trim().split(/\s+/).filter(s => s.length > 0)
}

// 将数组参数转换为字符串
function stringifyArguments(arr) {
  if (!arr || !Array.isArray(arr) || arr.length === 0) return ''
  return arr.join(' ')
}

// 将 KEY=VALUE 格式的环境变量字符串转换为对象
function parseEnv(str) {
  if (!str || !str.trim()) return {}
  const env = {}
  str.trim().split('\n').forEach(line => {
    line = line.trim()
    if (line && line.includes('=')) {
      const idx = line.indexOf('=')
      const key = line.substring(0, idx).trim()
      const value = line.substring(idx + 1).trim()
      if (key) env[key] = value
    }
  })
  return env
}

// 将环境变量对象转换为字符串
function stringifyEnv(obj) {
  if (!obj || typeof obj !== 'object') return ''
  return Object.entries(obj)
    .map(([key, value]) => `${key}=${value}`)
    .join('\n')
}

function resetForm() {
  form.value = {
    name: '',
    description: '',
    transport_type: 'stdio',
    command: '',
    arguments_str: '',
    env_str: '',
    url: '',
    timeout: 30,
    sync_mode: 'manual',
    sync_interval: 60,
    webhook_secret: '',
    webhook_url: '',
    enabled: true
  }
  hasWebhookSecret.value = false
  currentStep.value = 0
  isEdit.value = false
  currentEditId.value = null
}

function loadEditData(server) {
  resetForm()
  isEdit.value = true
  currentEditId.value = server.id

  form.value = {
    name: server.name || '',
    description: server.description || '',
    transport_type: server.transport_type || 'stdio',
    command: server.command || '',
    arguments_str: stringifyArguments(server.arguments),
    env_str: stringifyEnv(server.env),
    url: server.url || '',
    timeout: server.timeout || 30,
    sync_mode: server.sync_mode || 'manual',
    sync_interval: server.sync_interval || 60,
    webhook_secret: '',
    webhook_url: server.webhook_url || '',
    enabled: server.enabled !== undefined ? server.enabled : true
  }
  hasWebhookSecret.value = server.has_webhook_secret || false
}

function closeDialog() {
  dialogVisible.value = false
}

function nextStep() {
  if (!canProceed.value) {
    return
  }
  if (currentStep.value < steps.length - 1) {
    currentStep.value++
  }
}

function previousStep() {
  if (currentStep.value > 0) {
    currentStep.value--
  }
}

async function handleSubmit() {
  if (!canProceed.value) {
    return
  }

  submitting.value = true
  try {
    const submitData = {
      name: form.value.name.trim(),
      description: form.value.description?.trim() || '',
      transport_type: form.value.transport_type,
      timeout: form.value.timeout || 30,
      sync_mode: form.value.sync_mode || 'manual',
      sync_interval: form.value.sync_interval || 60,
      webhook_secret: form.value.webhook_secret,
      webhook_url: form.value.webhook_url?.trim() || '',
      enabled: form.value.enabled !== undefined ? form.value.enabled : true
    }

    if (form.value.transport_type === 'stdio') {
      submitData.command = form.value.command.trim()
      submitData.arguments = parseArguments(form.value.arguments_str)
      submitData.env = parseEnv(form.value.env_str)
    } else if (form.value.transport_type === 'http') {
      submitData.url = form.value.url.trim()
    }

    let res
    if (isEdit.value) {
      res = await mcpApi.updateServer(currentEditId.value, submitData)
    } else {
      res = await mcpApi.createServer(submitData)
    }

    if (res.success) {
      notify.success(isEdit.value ? 'Server 更新成功' : 'Server 添加成功')
      emit('success')
      closeDialog()
    } else {
      notify.error(res.message || '操作失败')
    }
  } catch (e) {
    console.error('Failed to submit:', e)
    notify.error('操作失败')
  } finally {
    submitting.value = false
  }
}

function getSyncModeText(mode) {
  const map = { manual: '手动同步', scheduled: '定时同步', webhook: 'Webhook' }
  return map[mode] || mode
}
</script>
