# Railway 部署指南

## 项目结构
```
RAG_model-dev/
├── frontend/           # React + TypeScript 前端
├── python-backend/     # FastAPI 后端
├── package.json        # 根目录配置
├── railway.json        # Railway 配置
├── nixpacks.toml      # 构建配置
└── DEPLOYMENT.md       # 部署说明
```

## Railway 部署步骤

### 1. 准备代码
确保所有文件都已提交到 GitHub：
```bash
git add .
git commit -m "Ready for Railway deployment"
git push origin main
```

### 2. 创建 Railway 项目
1. 访问 [Railway.app](https://railway.app)
2. 使用 GitHub 账号登录
3. 点击 "New Project"
4. 选择 "Deploy from GitHub repo"
5. 选择您的仓库

### 3. 配置环境变量
在 Railway 项目设置中添加：
```
OPENAI_API_KEY=your-openai-api-key
```

### 4. 部署
Railway 会自动：
1. 检测到 `package.json` 和 `requirements.txt`
2. 安装 Node.js 和 Python 依赖
3. 运行构建命令：`npm run build`
4. 启动应用：`npm run start`

### 5. 获取部署 URL
部署完成后，Railway 会提供一个 URL，例如：
```
https://your-app-name.railway.app
```

## 技术栈识别

Railway 通过以下文件自动识别技术栈：

### 检测到的技术栈
- **Node.js**: 检测到 `package.json`
- **Python**: 检测到 `requirements.txt`
- **前端构建**: 检测到 `vite.config.ts`
- **后端 API**: 检测到 `main.py`

### 构建过程
1. **安装阶段**: 安装 Node.js 和 Python 依赖
2. **构建阶段**: 构建前端静态文件
3. **启动阶段**: 启动 FastAPI 服务器

## 故障排除

### 常见问题

#### 1. 构建失败
- 检查 `package.json` 中的脚本是否正确
- 确保所有依赖都已正确安装

#### 2. 端口问题
- Railway 会自动设置 `PORT` 环境变量
- 后端代码已配置为使用 `os.getenv("PORT", 3000)`

#### 3. 环境变量
- 确保 `OPENAI_API_KEY` 已正确设置
- 可以在 Railway 控制台查看环境变量

#### 4. 健康检查
- 应用启动后会自动检查 `/health` 端点
- 如果健康检查失败，应用会重启

### 调试方法
1. 查看 Railway 日志
2. 检查构建输出
3. 验证环境变量设置
4. 测试 API 端点

## 本地测试

在部署前，可以在本地测试：
```bash
# 安装依赖
npm run install-deps

# 构建前端
npm run build

# 启动应用
npm run start
```

访问 `http://localhost:3000` 测试应用。 