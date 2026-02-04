let s=null;function a(){if(!s){const e=document.createElement("div");e.className="notification-container",e.style.cssText=`
      position: fixed;
      top: 80px;
      right: 24px;
      z-index: 9999;
      display: flex;
      flex-direction: column;
      gap: 12px;
      pointer-events: none;
    `,document.body.appendChild(e),s=e}return s}function o(e){const t=a(),n=document.createElement("div");n.style.cssText=`
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
    border-left: 3px solid ${l(e.type)};
  `;const i=document.createElement("div");i.innerHTML=f(e.type),i.style.cssText=`
    width: 20px;
    height: 20px;
    flex-shrink: 0;
    color: ${d(e.type)};
  `;const r=document.createElement("div");r.style.cssText=`
    flex: 1;
    font-size: 13px;
    color: #fff;
    line-height: 1.5;
  `,r.textContent=e.message,n.appendChild(i),n.appendChild(r),t.appendChild(n);const c=e.duration||3e3;setTimeout(()=>{n.style.animation="slideOut 0.2s ease-in",setTimeout(()=>{n.parentNode===t&&t.removeChild(n)},200)},c)}function l(e){const t={success:"#10b981",warning:"#f59e0b",error:"#ef4444",info:"#3b82f6"};return t[e]||t.info}function d(e){const t={success:"#10b981",warning:"#f59e0b",error:"#ef4444",info:"#3b82f6"};return t[e]||t.info}function f(e){const t={success:'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M20 6L9 17L4 12"/></svg>',warning:'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M12 9V12M12 17H12.01M22 12C22 16.9706 17.0706 21 12 21C6.92937 21 2 16.0706 2 12C2 7.02944 6.92937 2 12 2C16.9706 2 21 6.92944 21 12Z"/></svg>',error:'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><circle cx="12" cy="12" r="10"/><path d="M15 9L9 15M9 9L15 15"/></svg>',info:'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><circle cx="12" cy="12" r="10"/><path d="M12 16V12"/><path d="M12 8H12.01"/></svg>'};return t[e]||t.info}if(!document.getElementById("notification-styles")){const e=document.createElement("style");e.id="notification-styles",e.textContent=`
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
  `,document.head.appendChild(e)}const p={success(e,t={}){o({type:"success",message:e,...t})},warning(e,t={}){o({type:"warning",message:e,...t})},error(e,t={}){o({type:"error",message:e,...t})},info(e,t={}){o({type:"info",message:e,...t})}};export{p as n};
