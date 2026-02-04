# AI Native 研发平台 - 前端设计更新

## 设计系统

### 色彩规范
| 色彩 | 用途 | 值 |
|------|------|------|
| 主色 | 品牌主色 | `#1890ff → #0050ff` (渐变) |
| 辅助色-橙 | 强调 | `#ff6b00` |
| 辅助色-绿 | 成功 | `#00d084` |
| 辅助色-紫 | 特殊 | `#722ed1` |
| 背景-主 | 主背景 | `#ffffff` |
| 背景-次 | 次背景 | `#f5f7fa` |
| 文字-主 | 主要文字 | `#1f2937` |
| 文字-次 | 次要文字 | `#6b7280` |
| 文字-辅 | 辅助文字 | `#9ca3af` |

### 设计原则
- **简约现代**: 清爽的布局，充足的留白
- **渐变效果**: 按钮和图标使用科技蓝渐变
- **微妙阴影**: 多层次阴影增加层次感
- **流畅动画**: 250ms 标准过渡，平滑的页面切换
- **圆角统一**: 10-14px 标准圆角

## 更新的组件

### 1. 主应用 (App.vue)
- 毛玻璃效果导航栏
- 渐变色 Logo 和品牌标识
- 活动状态指示器
- 平滑的页面切换动画

### 2. 首页页面 (Dashboard.vue)
- 渐变图标统计卡片
- 金银铜排行徽章
- 空状态插画
- 悬停上浮效果

### 3. 资源列表 (ResourceList.vue)
- 类型专属配色
- 现代搜索栏设计
- 卡片式资源展示
- 箭头指示器动画
- 分页组件

### 4. 仓库管理 (RepositoryManage.vue)
- 仓库卡片布局
- 同步状态标签
- 加载动画
- 模态框表单
- 确认对话框

## 文件结构
```
frontend/src/
├── styles/
│   └── design-tokens.css    # 设计变量
├── views/
│   ├── Dashboard.vue        # 首页页面
│   ├── ResourceList.vue     # 资源列表
│   ├── ResourceDetail.vue   # 资源详情
│   └── RepositoryManage.vue # 仓库管理
└── App.vue                 # 主应用
```

## 使用说明

1. 确保已导入 `design-tokens.css`:
```css
@import '@/styles/design-tokens.css';
```

2. 使用 CSS 变量:
```css
color: var(--color-text-primary);
background: var(--color-bg-primary);
border-radius: var(--radius-lg);
```

3. 图标使用内联 SVG，确保一致性:
```html
<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
  <!-- path -->
</svg>
```

## 浏览器支持
- Chrome/Edge 90+
- Firefox 88+
- Safari 14+
