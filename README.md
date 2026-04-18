# AtomGit 状态自动更新系统

一个基于 GitHub Actions 的自动化解决方案，用于自动点击 AtomGit 页面上的"免费领取"按钮。

## 🚀 核心功能

### 🔄 自动按钮点击
- **智能定位**: 自动定位并点击"免费领取"按钮
- **多种定位方式**: 支持通过 XPath、CSS选择器和文本内容等多种方式定位按钮
- **固定时间执行**: 每日凌晨4:00 (UTC+8) 自动执行
- **Cookie认证**: 自动设置登录Cookie进行身份验证

### 🌐 浏览器自动化
- **无头模式运行**: 在 GitHub Actions 环境中无界面运行
- **反检测机制**: 随机 User-Agent、操作延迟等，模拟真实用户行为
- **页面加载优化**: 增加页面加载等待时间，确保页面完全渲染

### ⚡ GitHub Actions 自动化
- **定时触发执行**: 每日固定时间执行完整流程
- **详细日志记录**: 完整的执行日志和错误追踪
- **UTC+8 时区支持**: 统一使用北京时间，确保时间准确性

## 📁 项目结构

```
atomgit_api/
├── .github/
│   └── workflows/
│       └── auto-update-api.yml    # GitHub Actions 工作流配置
├── update_status.py              # 主程序 - 自动点击"免费领取"按钮
├── requirements.txt              # Python 依赖包列表
├── LICENSE                      # MIT 许可证
└── README.md                   # 项目说明文档
```

## 🛠️ 快速开始

### 1. 环境准备

#### 克隆项目
```bash
git clone <your-repo-url>
cd atomgit_api
```

#### 安装依赖
```bash
# 创建虚拟环境
python -m venv .venv

# 激活虚拟环境
# Windows
.venv\Scripts\activate
# Linux/Mac
source .venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

### 2. 环境变量配置

#### 必需环境变量
```bash
# AtomGit 平台认证
ATOMGIT_COOKIE=your_atomgit_cookie_here
```

### 3. GitHub Secrets 配置

在 GitHub 仓库的 **Settings > Secrets and variables > Actions** 中配置：

| Secret Name | Description | Required | Example |
|-------------|-------------|----------|----------|
| `ATOMGIT_COOKIE` | AtomGit 平台登录 Cookie | ✅ Yes | `your_cookie_here` |

## 🔧 核心模块详解

### update_status.py - 主程序

**主要功能**:
- 自动访问 AtomGit 页面 (https://ai.atomgit.com/serverless-api)
- 自动设置登录Cookie进行身份验证
- 智能定位"免费领取"按钮
- 自动点击按钮完成领取操作
- UTC+8 时区时间处理

**按钮定位策略**:
1. 首先尝试通过 XPath 文本内容定位
2. 然后尝试 CSS 选择器定位
3. 最后遍历所有按钮元素查找匹配文本

**执行流程**:
1. 获取Cookie认证信息
2. 访问AtomGit页面
3. 设置Cookie并刷新页面
4. 等待页面完全加载
5. 查找"免费领取"按钮
6. 点击按钮
7. 等待操作完成
8. 记录执行结果

## ⚙️ GitHub Actions 工作流

### 执行策略

#### 直接执行 (update-status)
- **简单直接**: 每日固定时间执行完整流程
- **完整流程**: 包含所有功能模块
- **稳定可靠**: 移除复杂调度逻辑

### 执行频率

- **定时触发**: 每日凌晨4:00 (UTC+8) 执行 (`0 20 * * *` UTC时间)
- **固定执行**: 每次都会完整执行

### 环境变量

| Secret Name | Description | Required |
|-------------|-------------|----------|
| `ATOMGIT_COOKIE` | AtomGit 平台登录 Cookie | ✅ Yes |

## 🔍 使用示例

### 本地测试

```bash
# 设置环境变量
export ATOMGIT_COOKIE="your_cookie_here"

# 运行主程序
python update_status.py
```

### 手动触发

在 GitHub Actions 页面手动触发工作流运行。

## 🐛 故障排除

### 常见问题

#### 1. 环境变量未设置
**症状**: `ATOMGIT_COOKIE环境变量未设置`
**解决**: 检查 GitHub Secrets 或本地环境变量配置

#### 2. Cookie认证失败
**症状**: `Cookie认证失败` 或页面显示未登录
**解决**:
- 更新 ATOMGIT_COOKIE 值
- 检查Cookie是否过期
- 确保Cookie格式正确

#### 3. 按钮未找到
**症状**: `未找到'免费领取'按钮`
**解决**:
- 检查 AtomGit 页面结构是否发生变化
- 查看日志中的调试信息
- 可能需要更新按钮定位选择器

#### 4. 按钮点击失败
**症状**: `点击按钮时出错`
**解决**:
- 检查按钮是否可点击
- 增加等待时间确保页面完全加载
- 查看错误日志详情

### 日志分析

程序提供详细的日志输出，包括：
- 执行时间点（UTC+8）
- Cookie设置状态
- 页面访问状态
- 按钮定位步骤
- 点击操作结果
- 执行结果状态

## 📈 监控和维护

### 执行状态监控

GitHub Actions 提供完整的执行历史：
- 成功/失败状态
- 执行时间统计
- 详细的日志输出

### 定期维护

1. **Cookie更新**: 定期检查并更新 ATOMGIT_COOKIE
2. **依赖更新**: 定期更新 Python 依赖包
3. **页面结构监控**: 关注 AtomGit 页面结构变化，及时调整选择器

## 🔒 安全考虑

### 隐私保护
- 所有敏感信息通过环境变量管理
- GitHub Secrets 提供安全的机密存储
- 代码中无硬编码的隐私信息

### 反检测机制
- 随机 User-Agent 轮换
- 操作延迟模拟人类行为
- 无头模式运行避免检测

### 最佳实践
- 使用虚拟环境隔离依赖
- 不要在代码中硬编码敏感信息
- 定期更新Cookie和依赖包版本

## 📄 许可证

本项目采用 [MIT 许可证](LICENSE)，允许自由使用、修改和分发。

## 🤝 贡献指南

欢迎提交 Issue 和 Pull Request 来改进项目！

### 开发环境设置

1. Fork 项目仓库
2. 创建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 创建 Pull Request

## 📞 支持

如果您遇到问题或有建议：

1. 查看 [故障排除](#故障排除) 部分
2. 检查 GitHub Issues 是否有类似问题
3. 创建新的 Issue 描述您的问题

---

**注意**: 使用本项目需要遵守 AtomGit 平台的使用条款和相关法律法规。