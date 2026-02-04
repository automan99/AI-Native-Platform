/**
 * 扁平化暗黑风格通知系统
 */

let notificationContainer = null

function getContainer() {
  if (!notificationContainer) {
    const container = document.createElement('div')
    container.className = 'notification-container'
    container.style.cssText = `
      position: fixed;
      top: 80px;
      right: 24px;
      z-index: 9999;
      display: flex;
      flex-direction: column;
      gap: 12px;
      pointer-events: none;
    `
    document.body.appendChild(container)
    notificationContainer = container
  }
  return notificationContainer
}

function createNotification(options) {
  const container = getContainer()

  const wrapper = document.createElement('div')
  wrapper.style.cssText = `
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 12px 16px;
    background: #1e1e1e;
    border: 1px solid #333;
    border-radius: 8px;
    pointer-events: auto;
    min-width: 280px;
    max-width: 360px;
    animation: slideIn 0.2s ease-out;
    border-left: 3px solid ${getBorderColor(options.type)};
  `

  const icon = document.createElement('div')
  icon.innerHTML = getIcon(options.type)
  icon.style.cssText = `
    width: 20px;
    height: 20px;
    flex-shrink: 0;
    color: ${getIconColor(options.type)};
  `

  const content = document.createElement('div')
  content.style.cssText = `
    flex: 1;
    font-size: 13px;
    color: #fff;
    line-height: 1.5;
  `
  content.textContent = options.message

  wrapper.appendChild(icon)
  wrapper.appendChild(content)
  container.appendChild(wrapper)

  // 自动移除
  const duration = options.duration || 3000
  setTimeout(() => {
    wrapper.style.animation = 'slideOut 0.2s ease-in'
    setTimeout(() => {
      if (wrapper.parentNode === container) {
        container.removeChild(wrapper)
      }
    }, 200)
  }, duration)
}

function getBorderColor(type) {
  const colors = {
    success: '#10b981',
    warning: '#f59e0b',
    error: '#ef4444',
    info: '#3b82f6'
  }
  return colors[type] || colors.info
}

function getIconColor(type) {
  const colors = {
    success: '#10b981',
    warning: '#f59e0b',
    error: '#ef4444',
    info: '#3b82f6'
  }
  return colors[type] || colors.info
}

function getIcon(type) {
  const icons = {
    success: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M20 6L9 17L4 12"/></svg>`,
    warning: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M12 9V12M12 17H12.01M22 12C22 16.9706 17.0706 21 12 21C6.92937 21 2 16.0706 2 12C2 7.02944 6.92937 2 12 2C16.9706 2 21 6.92944 21 12Z"/></svg>`,
    error: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><circle cx="12" cy="12" r="10"/><path d="M15 9L9 15M9 9L15 15"/></svg>`,
    info: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><circle cx="12" cy="12" r="10"/><path d="M12 16V12"/><path d="M12 8H12.01"/></svg>`
  }
  return icons[type] || icons.info
}

// 添加动画样式
if (!document.getElementById('notification-styles')) {
  const style = document.createElement('style')
  style.id = 'notification-styles'
  style.textContent = `
    @keyframes slideIn {
      from {
        opacity: 0;
        transform: translateX(100%);
      }
      to {
        opacity: 1;
        transform: translateX(0);
      }
    }
    @keyframes slideOut {
      from {
        opacity: 1;
        transform: translateX(0);
      }
      to {
        opacity: 0;
        transform: translateX(100%);
      }
    }
  `
  document.head.appendChild(style)
}

export const notify = {
  success(message, options = {}) {
    createNotification({ type: 'success', message, ...options })
  },
  warning(message, options = {}) {
    createNotification({ type: 'warning', message, ...options })
  },
  error(message, options = {}) {
    createNotification({ type: 'error', message, ...options })
  },
  info(message, options = {}) {
    createNotification({ type: 'info', message, ...options })
  }
}

// 确认对话框
export function confirm(options) {
  return new Promise((resolve, reject) => {
    const overlay = document.createElement('div')
    overlay.className = 'confirm-overlay'
    overlay.style.cssText = `
      position: fixed;
      inset: 0;
      background: rgba(0, 0, 0, 0.6);
      display: flex;
      align-items: center;
      justify-content: center;
      z-index: 10000;
      padding: 20px;
      animation: fadeIn 0.15s ease-out;
    `

    const modal = document.createElement('div')
    modal.className = 'confirm-modal'
    modal.style.cssText = `
      background: #1e1e1e;
      border: 1px solid #333;
      border-radius: 12px;
      padding: 20px;
      max-width: 380px;
      width: 100%;
      animation: scaleIn 0.15s ease-out;
    `

    modal.innerHTML = `
      <div style="font-size: 15px; font-weight: 500; color: #fff; margin-bottom: 12px;">
        ${options.title || '确认'}
      </div>
      <div style="font-size: 13px; color: #ccc; margin-bottom: 20px; line-height: 1.6;">
        ${options.message || ''}
      </div>
      <div style="display: flex; gap: 8px; justify-content: flex-end;">
        <button class="confirm-btn cancel" style="
          padding: 8px 16px;
          border: 1px solid #333;
          background: #333;
          color: #ccc;
          border-radius: 6px;
          font-size: 13px;
          font-weight: 500;
          cursor: pointer;
          transition: all 0.15s;
        ">取消</button>
        <button class="confirm-btn ok" style="
          padding: 8px 16px;
          border: none;
          background: #3b82f6;
          color: white;
          border-radius: 6px;
          font-size: 13px;
          font-weight: 500;
          cursor: pointer;
          transition: all 0.15s;
        ">确定</button>
      </div>
    `

    overlay.appendChild(modal)
    document.body.appendChild(overlay)

    // 添加动画样式
    if (!document.getElementById('confirm-styles')) {
      const style = document.createElement('style')
      style.id = 'confirm-styles'
      style.textContent = `
        @keyframes fadeIn {
          from { opacity: 0; }
          to { opacity: 1; }
        }
        @keyframes scaleIn {
          from { opacity: 0; transform: scale(0.95); }
          to { opacity: 1; transform: scale(1); }
        }
        .confirm-btn.ok:hover {
          background: #2563eb;
        }
        .confirm-btn.cancel:hover {
          background: #444;
        }
      `
      document.head.appendChild(style)
    }

    const cancelBtn = modal.querySelector('.confirm-btn.cancel')
    const okBtn = modal.querySelector('.confirm-btn.ok')

    const cleanup = () => {
      overlay.style.animation = 'fadeOut 0.15s ease-in'
      modal.style.animation = 'scaleOut 0.15s ease-in'
      setTimeout(() => {
        if (overlay.parentNode === document.body) {
          document.body.removeChild(overlay)
        }
      }, 150)
    }

    // 添加淡出动画
    const fadeOutStyle = document.createElement('style')
    fadeOutStyle.textContent = `
      @keyframes fadeOut {
        from { opacity: 1; }
        to { opacity: 0; }
      }
      @keyframes scaleOut {
        from { opacity: 1; transform: scale(1); }
        to { opacity: 0; transform: scale(0.95); }
      }
    `
    document.head.appendChild(fadeOutStyle)

    cancelBtn.addEventListener('click', () => {
      cleanup()
      reject('cancel')
    })

    okBtn.addEventListener('click', () => {
      cleanup()
      resolve()
    })

    overlay.addEventListener('click', (e) => {
      if (e.target === overlay) {
        cleanup()
        reject('cancel')
      }
    })
  })
}

export const ElMessage = {
  success: notify.success,
  warning: notify.warning,
  error: notify.error,
  info: notify.info
}

export const ElMessageBox = {
  confirm: (options) => {
    if (typeof options === 'string') {
      options = { message: options }
    }
    return confirm(options)
  }
}
