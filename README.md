# AI灵眸塔罗 - AI塔罗+MBTI占卜应用

基于大语言模型的个性化塔罗占卜应用，结合MBTI性格特质提供有温度的解读。

## 项目结构

```
├── frontend/          # Uni-app + Vue3 前端
├── backend/           # Python FastAPI 后端
└── README.md
```

## 快速开始

### 1. 配置API Key

复制 `backend/.env.example` 到 `backend/.env` 并填写你的LLM API Key:

```bash
cd backend
cp .env.example .env
# 编辑 .env 文件，填入 ZHIPU_API_KEY 或者 MOONSHOT_API_KEY
```

支持的LLM提供商：
- 智谱GLM (推荐，中文理解好，价格便宜)
- Kimi MoonShot

### 2. 启动后端

```bash
cd backend
pip install -r requirements.txt
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

后端API文档访问: http://localhost:8000/docs

### 3. 启动前端开发

```bash
cd frontend
npm install
npm run dev:h5
```

前端访问: http://localhost:3000

## 功能特性

- ✅ 首页主题选择 + MBTI选择
- ✅ 洗牌抽牌动画（核心体验）
- ✅ AI生成个性化解读（结合MBTI）
- ✅ 结果展示 + 分享海报生成
- ✅ 每日免费次数限制
- ✅ 支持微信小程序打包

## MVP功能范围

- 22张大阿卡纳牌
- 支持单张牌/三张牌牌阵
- 基础商业化限流预留

## 技术栈

- **前端**: Uni-app + Vue 3 + SCSS
- **后端**: Python FastAPI + Uvicorn
- **AI API**: 智谱GLM / Kimi MoonShot
- **限流缓存**: Redis

## 打包发布

### 微信小程序

```bash
cd frontend
npm run build:mp-weixin
```

然后用微信开发者工具导入 `dist/build/mp-weixin` 目录发布。

### H5

```bash
cd frontend
npm run build:h5
```

将 `dist/build/h5` 部署到你的服务器。

## 合规说明

项目已经按照微信小程序要求做好合规处理：
- 文案强调"娱乐仅供参考"
- 避免封建迷信词汇
- 定位为AI心理分析娱乐应用

## 后续扩展

- [ ] 添加完整78张韦特塔罗牌
- [ ] 添加复杂牌阵（塞尔特十字）
- [ ] 用户系统与历史记录
- [ ] 支付/广告变现集成
- [ ] 更多主题选择
