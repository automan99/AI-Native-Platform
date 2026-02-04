<template>
  <transition name="modal">
    <div v-if="dialogVisible" class="modal-overlay" @click.self="closeDialog">
      <div class="dialog-modal dialog-modal--wizard">
        <div class="dialog-header">
          <h3>{{ isEdit ? '编辑' : '添加' }} Skills 仓库</h3>
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
            <div class="wizard-panel__desc">配置 Skills 仓库的基本识别信息</div>

            <div class="form-field">
              <label class="form-label">仓库名称 <span class="required">*</span></label>
              <input v-model="form.name" class="form-input" placeholder="例如：AI Skills Repository" />
            </div>

            <div class="form-field">
              <label class="form-label">仓库地址 <span class="required">*</span></label>
              <input v-model="form.url" class="form-input form-input--mono" placeholder="https://gitlab.com/group/project" :disabled="isEdit" />
              <small v-if="isEdit" class="form-hint">仓库地址不可修改</small>
              <small v-else class="form-hint">Git 仓库的 HTTP 或 HTTPS 地址</small>
            </div>

            <div class="form-field">
              <label class="form-label">描述</label>
              <textarea v-model="form.description" class="form-textarea" rows="3" placeholder="简要描述仓库用途..."></textarea>
            </div>

            <div class="form-row">
              <div class="form-field">
                <label class="form-label">分支</label>
                <input v-model="form.branch" class="form-input form-input--mono" placeholder="main" />
                <small class="form-hint">默认为 main</small>
              </div>
              <div class="form-field">
                <label class="form-label">代码路径</label>
                <input v-model="form.path" class="form-input form-input--mono" placeholder="src/skills" />
                <small class="form-hint">Skills 在仓库中的路径</small>
              </div>
            </div>
          </div>

          <!-- 步骤 2: 认证配置 -->
          <div v-show="currentStep === 1" class="wizard-panel">
            <div class="wizard-panel__title">认证配置</div>
            <div class="wizard-panel__desc">选择访问仓库所需的认证方式</div>

            <div class="radio-cards">
              <label class="radio-card" :class="{ 'radio-card--active': form.auth_type === 'public' }">
                <input type="radio" v-model="form.auth_type" value="public" />
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                  <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/>
                </svg>
                <span>公开仓库</span>
                <small>无需认证</small>
              </label>
              <label class="radio-card" :class="{ 'radio-card--active': form.auth_type === 'token' }">
                <input type="radio" v-model="form.auth_type" value="token" />
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                  <rect x="3" y="11" width="18" height="11" rx="2"/>
                  <path d="M7 11V7a5 5 0 0 1 10 0v4"/>
                </svg>
                <span>Token 认证</span>
                <small>访问令牌</small>
              </label>
              <label class="radio-card" :class="{ 'radio-card--active': form.auth_type === 'ssh' }">
                <input type="radio" v-model="form.auth_type" value="ssh" />
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                  <path d="M4 17l6-6-6-6M12 19h8"/>
                </svg>
                <span>SSH 密钥</span>
                <small>SSH私钥</small>
              </label>
            </div>

            <div v-if="form.auth_type === 'token'" class="form-field">
              <label class="form-label">访问令牌 <span class="required">*</span></label>
              <input v-model="form.auth_token" type="password" class="form-input form-input--mono" placeholder="glpat-xxxxxxxxxxxxxx" />
              <small class="form-hint">Git 仓库的访问令牌（Personal Access Token）</small>
            </div>

            <div v-if="form.auth_type === 'ssh'" class="form-field">
              <label class="form-label">SSH 私钥 <span class="required">*</span></label>
              <textarea v-model="form.ssh_key" class="form-textarea form-textarea--mono" rows="5" placeholder="-----BEGIN RSA PRIVATE KEY-----"></textarea>
              <small class="form-hint">用于访问 Git 仓库的 SSH 私钥</small>
            </div>
          </div>

          <!-- 步骤 3: 同步配置 -->
          <div v-show="currentStep === 2" class="wizard-panel">
            <div class="wizard-panel__title">同步配置</div>
            <div class="wizard-panel__desc">选择仓库内容的同步方式</div>

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
              <small class="form-hint">系统将按此间隔自动同步仓库内容</small>
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

          <!-- 步骤 4: 确认配置 -->
          <div v-show="currentStep === 3" class="wizard-panel">
            <div class="wizard-panel__title">确认配置</div>
            <div class="wizard-panel__desc">请确认以下配置信息无误</div>

            <div class="config-summary">
              <div class="config-section">
                <div class="config-section__title">基础信息</div>
                <div class="config-item">
                  <span class="config-item__label">仓库名称</span>
                  <span class="config-item__value">{{ form.name || '-' }}</span>
                </div>
                <div class="config-item">
                  <span class="config-item__label">仓库地址</span>
                  <span class="config-item__value config-item__value--mono">{{ form.url || '-' }}</span>
                </div>
                <div v-if="form.description" class="config-item">
                  <span class="config-item__label">描述</span>
                  <span class="config-item__value">{{ form.description }}</span>
                </div>
                <div class="config-item">
                  <span class="config-item__label">分支</span>
                  <span class="config-item__value config-item__value--mono">{{ form.branch || 'main' }}</span>
                </div>
                <div v-if="form.path" class="config-item">
                  <span class="config-item__label">代码路径</span>
                  <span class="config-item__value config-item__value--mono">{{ form.path }}</span>
                </div>
              </div>

              <div class="config-section">
                <div class="config-section__title">认证配置</div>
                <div class="config-item">
                  <span class="config-item__label">认证方式</span>
                  <span class="config-item__value config-item__value--badge" :class="`badge--${form.auth_type}`">{{ getAuthTypeText(form.auth_type) }}</span>
                </div>
                <div v-if="form.auth_type === 'token'" class="config-item">
                  <span class="config-item__label">访问令牌</span>
                  <span class="config-item__value">{{ isEdit && hasAuthToken ? '*** 已设置 ***' : (form.auth_token ? '*** 已填写 ***' : '-') }}</span>
                </div>
                <div v-if="form.auth_type === 'ssh'" class="config-item">
                  <span class="config-item__label">SSH密钥</span>
                  <span class="config-item__value">{{ isEdit && hasSshKey ? '*** 已设置 ***' : (form.ssh_key ? '*** 已填写 ***' : '-') }}</span>
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
                <div class="config-item">
                  <span class="config-item__label">启用状态</span>
                  <span class="config-item__value config-item__value--status" :class="form.enabled ? 'status-enabled' : 'status-disabled'">
                    {{ form.enabled ? '启用' : '禁用' }}
                  </span>
                </div>
              </div>
            </div>

            <div class="form-field" style="margin-top: 16px;">
              <label class="checkbox checkbox--large">
                <input type="checkbox" v-model="form.enabled" />
                <div class="checkbox-content">
                  <strong>启用此仓库</strong>
                  <small>启用后将自动同步仓库中的 Skills 资源</small>
                </div>
              </label>
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
          <button v-if="currentStep < steps.length - 1" class="btn btn--primary" @click="nextStep">
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
  background: var(--color-bg-secondary);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-lg);
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
  border-bottom: 1px solid var(--color-border);
}

.dialog-header h3 {
  font-size: 16px;
  font-weight: 600;
  color: var(--color-text-primary);
  margin: 0;
}

.dialog-close {
  width: 28px;
  height: 28px;
  border: none;
  background: none;
  border-radius: var(--radius-sm);
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--color-text-muted);
  cursor: pointer;
  transition: all var(--transition-fast);
}

.dialog-close:hover {
  background: var(--color-bg-hover);
  color: var(--color-text-primary);
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
  background: var(--color-bg-primary);
}

.dialog-body::-webkit-scrollbar-thumb {
  background: var(--color-border);
  border-radius: 3px;
}

.dialog-footer {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
  padding: 16px 20px;
  border-top: 1px solid var(--color-border);
  background: var(--color-bg-secondary);
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
  background: var(--color-bg-tertiary);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
  overflow: hidden;
}

.config-section__title {
  font-size: 13px;
  font-weight: 500;
  color: var(--color-text-secondary);
  padding: 10px 16px;
  background: var(--color-bg-hover);
  border-bottom: 1px solid var(--color-border);
}

.config-item {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  padding: 12px 16px;
  border-bottom: 1px solid var(--color-border);
}

.config-item:last-child {
  border-bottom: none;
}

.config-item__label {
  font-size: 13px;
  color: var(--color-text-secondary);
  flex-shrink: 0;
  width: 80px;
}

.config-item__value {
  font-size: 13px;
  color: var(--color-text-primary);
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

.badge--public {
  background: rgba(0, 255, 0, 0.15);
  color: var(--color-green);
}

.badge--token {
  background: var(--color-blue-glow);
  color: var(--color-blue);
}

.badge--ssh {
  background: rgba(245, 158, 11, 0.15);
  color: #f59e0b;
}

.config-item__value--status {
  font-weight: 500;
}

.status-enabled {
  color: var(--color-green);
}

.status-disabled {
  color: var(--color-text-muted);
}

/* 复选框 */
.checkbox {
  display: flex;
  align-items: center;
  gap: 8px;
  cursor: pointer;
  font-size: 14px;
  color: var(--color-text-secondary);
}

.checkbox input[type="checkbox"] {
  width: 16px;
  height: 16px;
  cursor: pointer;
  accent-color: var(--color-blue);
}

.checkbox--large {
  padding: 12px;
  background: var(--color-bg-primary);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
  flex-direction: column;
  align-items: flex-start;
  gap: 4px;
}

.checkbox--large input[type="checkbox"] {
  width: 18px;
  height: 18px;
}

.checkbox-content strong {
  display: block;
  font-size: 14px;
  font-weight: 500;
  color: var(--color-text-primary);
}

.checkbox-content small {
  display: block;
  font-size: 12px;
  color: var(--color-text-secondary);
  margin-top: 2px;
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
import { ref, computed, watch } from 'vue'
import { repositoryApi } from '@/api/repositories'
import { notify } from '@/utils/notification'

const props = defineProps({
  visible: {
    type: Boolean,
    default: false
  },
  editRepo: {
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

const steps = ['基础信息', '认证配置', '同步配置', '确认配置']

const form = ref({
  name: '',
  description: '',
  url: '',
  branch: 'main',
  path: '',
  auth_type: 'public',
  auth_token: '',
  ssh_key: '',
  sync_mode: 'manual',
  sync_interval: 60,
  sync_enabled: true,
  enabled: true,
  webhook_secret: '',
  webhook_url: ''
})

const hasAuthToken = ref(false)
const hasSshKey = ref(false)
const hasWebhookSecret = ref(false)

// 当前步骤是否可以继续
const canProceed = computed(() => {
  switch (currentStep.value) {
    case 0:
      return form.value.name && form.value.url
    case 1:
      if (form.value.auth_type === 'token' && !form.value.auth_token && !hasAuthToken.value) return false
      if (form.value.auth_type === 'ssh' && !form.value.ssh_key && !hasSshKey.value) return false
      return true
    case 2:
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
    if (props.editRepo) {
      loadEditData(props.editRepo)
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

function resetForm() {
  form.value = {
    name: '',
    description: '',
    url: '',
    branch: 'main',
    path: '',
    auth_type: 'public',
    auth_token: '',
    ssh_key: '',
    sync_mode: 'manual',
    sync_interval: 60,
    sync_enabled: true,
    enabled: true,
    webhook_secret: '',
    webhook_url: ''
  }
  hasAuthToken.value = false
  hasSshKey.value = false
  hasWebhookSecret.value = false
  currentStep.value = 0
  isEdit.value = false
  currentEditId.value = null
}

async function loadEditData(repo) {
  resetForm()
  isEdit.value = true
  currentEditId.value = repo.id

  try {
    const res = await repositoryApi.getDetail(repo.id, true)
    if (res.success) {
      const data = res.data
      form.value = {
        name: data.name || '',
        description: data.description || '',
        url: data.url || '',
        branch: data.branch || 'main',
        path: data.path || '',
        auth_type: data.auth_type || 'public',
        auth_token: '',
        ssh_key: '',
        sync_mode: data.sync_mode || 'manual',
        sync_interval: data.sync_interval || 60,
        sync_enabled: data.sync_enabled !== undefined ? data.sync_enabled : true,
        enabled: data.enabled !== undefined ? data.enabled : true,
        webhook_secret: '',
        webhook_url: data.webhook_url || ''
      }
      hasAuthToken.value = data.has_auth_token || false
      hasSshKey.value = data.has_ssh_key || false
      hasWebhookSecret.value = data.has_webhook_secret || false
    }
  } catch (e) {
    console.error('Failed to load repository detail:', e)
    notify.error('加载仓库详情失败')
  }
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
  if (!form.value.name || !form.value.url) {
    notify.warning('请填写仓库名称和地址')
    currentStep.value = 0
    return
  }

  if (form.value.auth_type === 'token' && !form.value.auth_token && !hasAuthToken.value) {
    notify.warning('请提供访问令牌')
    currentStep.value = 1
    return
  }
  if (form.value.auth_type === 'ssh' && !form.value.ssh_key && !hasSshKey.value) {
    notify.warning('请提供SSH密钥')
    currentStep.value = 1
    return
  }
  if (form.value.sync_mode === 'webhook' && !form.value.webhook_secret && !hasWebhookSecret.value) {
    notify.warning('请提供Webhook密钥')
    currentStep.value = 2
    return
  }

  submitting.value = true
  try {
    const submitData = { ...form.value }

    if (isEdit.value) {
      if (!submitData.auth_token && hasAuthToken.value) delete submitData.auth_token
      if (!submitData.ssh_key && hasSshKey.value) delete submitData.ssh_key
      if (!submitData.webhook_secret && hasWebhookSecret.value) delete submitData.webhook_secret
    }

    let res
    if (isEdit.value) {
      res = await repositoryApi.update(currentEditId.value, submitData)
    } else {
      res = await repositoryApi.create(submitData)
    }

    if (res.success) {
      notify.success(isEdit.value ? '仓库更新成功' : '仓库添加成功')
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

function getAuthTypeText(type) {
  const map = { public: '公开仓库', token: 'Token 认证', ssh: 'SSH 密钥' }
  return map[type] || type
}

function getSyncModeText(mode) {
  const map = { manual: '手动同步', scheduled: '定时同步', webhook: 'Webhook' }
  return map[mode] || mode
}
</script>
