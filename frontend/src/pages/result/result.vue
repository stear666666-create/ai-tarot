<template>
  <view class="container">
    <!-- 结果卡片 -->
    <view class="result-card">
      <!-- 头部信息 -->
      <view class="result-header">
        <view class="theme-info">
          <text class="theme-text">{{ theme }}</text>
          <text class="mbti-tag">MBTI: {{ mbti }}</text>
        </view>
      </view>

      <!-- 抽到的牌 -->
      <view class="cards-section">
        <view class="section-title">你抽到的牌</view>
        <view class="cards-list">
          <view
            v-for="card in drawnCards"
            :key="card.id"
            class="result-card-item"
          >
            <view class="card-display">
              <text class="card-name">{{ card.name }}</text>
              <text class="card-position">{{ card.reversed ? '逆位' : '正位' }}</text>
            </view>
          </view>
        </view>
      </view>

      <!-- AI解读 -->
      <view class="interpretation-section">
        <view class="section-title">🔮 AI解读</view>
        <view class="interpretation-text">
          <text>{{ interpretation }}</text>
        </view>
      </view>

      <!-- 箴言 -->
      <view v-if="quote" class="quote-section">
        <view class="quote-box">
          <text class="quote-text">“{{ quote }}”</text>
        </view>
      </view>
    </view>

    <!-- 分享海报生成 -->
    <view v-if="quote" class="share-section">
      <button class="generate-btn" @click="generatePoster">
        生成分享海报 📷
      </button>
    </view>

    <!-- 海报预览 -->
    <view v-if="showPoster" class="poster-modal" @tap="closeModal">
      <view class="poster-container" catchtap @tap.stop>
        <canvas
          canvas-id="posterCanvas"
          :style="{ width: canvasWidth + 'px', height: canvasHeight + 'px' }"
          class="poster-canvas"
        ></canvas>
        <view class="poster-actions">
          <button v-if="posterUrl" class="save-btn" @click="savePoster">
            保存图片到相册
          </button>
          <button class="close-btn" @click="closeModal">关闭</button>
        </view>
      </view>
    </view>

    <!-- 底部操作 -->
    <view class="actions">
      <button class="back-btn" @click="goHome">
        返回首页
      </button>
    </view>

    <!-- 免责声明 -->
    <view class="disclaimer">
      <text>本内容仅供娱乐参考，不构成任何决策建议</text>
    </view>
  </view>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { onLoad } from '@dcloudio/uni-app'
import tarotData from '@/static/data/tarot.json'

const theme = ref('')
const mbti = ref('')
const drawnCards = ref([])
const interpretation = ref('')
const quote = ref('')
const showPoster = ref(false)
const posterUrl = ref('')
const canvasWidth = 300
const canvasHeight = 500

function getCardInfo(id) {
  return tarotData.find(c => c.id === id) || { name: '未知' }
}

onLoad((options) => {
  theme.value = decodeURIComponent(options.theme)
  mbti.value = options.mbti
  drawnCards.value = JSON.parse(decodeURIComponent(options.cards))
  interpretation.value = decodeURIComponent(options.interpretation)
  quote.value = decodeURIComponent(options.quote || '')
})

function goHome() {
  uni.switchTab({
    url: '/pages/index/index'
  })
}

function generatePoster() {
  showPoster.value = true
  // Next tick draw canvas
  setTimeout(() => {
    drawPoster()
  }, 100)
}

function drawPoster() {
  const ctx = uni.createCanvasContext('posterCanvas')

  // Background gradient (simulate with solid purple for simplicity)
  ctx.fillStyle = '#1a1a2e'
  ctx.fillRect(0, 0, canvasWidth, canvasHeight)

  // Title
  ctx.fillStyle = '#e8d5b7'
  ctx.font = 'bold 20px sans-serif'
  ctx.textAlign = 'center'
  ctx.fillText('AI灵眸塔罗', canvasWidth / 2, 40)

  // Subtitle
  ctx.fillStyle = '#a8a8b8'
  ctx.font = '14px sans-serif'
  ctx.fillText(`${theme.value} · MBTI: ${mbti.value}`, canvasWidth / 2, 65)

  // Card info
  let y = 100
  drawnCards.value.forEach(card => {
    const info = getCardInfo(card.id)
    ctx.fillStyle = '#fff'
    ctx.font = '16px sans-serif'
    ctx.textAlign = 'left'
    ctx.fillText(`${info.name} (${card.reversed ? '逆位' : '正位'})`, 20, y)
    y += 30
  })

  // Quote
  ctx.fillStyle = '#a78bfa'
  ctx.font = 'italic 18px sans-serif'
  ctx.textAlign = 'center'
  // Wrap quote text (simplified)
  const quoteText = `"${quote.value}"`
  ctx.fillText(quoteText, canvasWidth / 2, y + 40)

  // Footer
  ctx.fillStyle = '#888'
  ctx.font = '12px sans-serif'
  ctx.textAlign = 'center'
  ctx.fillText('AI灵眸塔罗 · 仅供娱乐', canvasWidth / 2, canvasHeight - 30)

  ctx.draw(false, () => {
    // Convert to image
    uni.canvasToTempFilePath({
      canvasId: 'posterCanvas',
      success: (res) => {
        posterUrl.value = res.tempFilePath
      },
      fail: (err) => {
        console.error('Generate poster failed:', err)
        uni.showToast({
          title: '生成失败',
          icon: 'none'
        })
      }
    })
  })
}

function savePoster() {
  if (!posterUrl.value) return

  uni.saveImageToPhotosAlbum({
    filePath: posterUrl.value,
    success: () => {
      uni.showToast({
        title: '保存成功',
        icon: 'success'
      })
    },
    fail: () => {
      uni.showToast({
        title: '保存失败，请检查权限',
        icon: 'none'
      })
    }
  })
}

function closeModal() {
  showPoster.value = false
  posterUrl.value = ''
}
</script>

<style lang="scss" scoped>
.container {
  min-height: 100vh;
  background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
  padding: 20rpx;
}

.result-card {
  background: rgba(255, 255, 255, 0.08);
  border: 2rpx solid rgba(255, 255, 255, 0.15);
  border-radius: 20rpx;
  padding: 30rpx;
  margin-bottom: 30rpx;
}

.result-header {
  margin-bottom: 30rpx;
}

.theme-info {
  text-align: center;
}

.theme-text {
  display: block;
  font-size: 36rpx;
  color: #fff;
  font-weight: bold;
  margin-bottom: 10rpx;
}

.mbti-tag {
  display: inline-block;
  padding: 8rpx 20rpx;
  background: rgba(167, 139, 250, 0.3);
  border-radius: 20rpx;
  font-size: 24rpx;
  color: #e0d0ff;
}

.section-title {
  font-size: 30rpx;
  color: #e8e8f0;
  margin-bottom: 20rpx;
  font-weight: 500;
}

.cards-section {
  margin-bottom: 30rpx;
}

.cards-list {
  display: flex;
  flex-wrap: wrap;
  gap: 16rpx;
}

.result-card-item {
  flex: 1;
  min-width: 140rpx;
}

.card-display {
  background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
  border-radius: 12rpx;
  padding: 20rpx 16rpx;
  text-align: center;
}

.card-name {
  display: block;
  font-size: 28rpx;
  font-weight: bold;
  color: #1f2937;
  margin-bottom: 6rpx;
}

.card-position {
  font-size: 22rpx;
  color: rgba(31, 41, 55, 0.7);
}

.interpretation-section {
  margin-bottom: 30rpx;
}

.interpretation-text {
  line-height: 2;
  font-size: 28rpx;
  color: #d0d0e0;
}

.quote-section {
  margin-top: 20rpx;
}

.quote-box {
  background: rgba(167, 139, 250, 0.2);
  border-left: 8rpx solid #a78bfa;
  padding: 24rpx;
  border-radius: 8rpx;
}

.quote-text {
  display: block;
  font-size: 32rpx;
  font-style: italic;
  color: #e0d0ff;
  text-align: center;
  line-height: 1.6;
}

.share-section {
  margin-bottom: 30rpx;
}

.generate-btn {
  width: 100%;
  height: 80rpx;
  background: linear-gradient(135deg, #10b981 0%, #059669 100%);
  color: #fff;
  border: none;
  border-radius: 40rpx;
  font-size: 30rpx;
  font-weight: bold;
  box-shadow: 0 6rpx 16rpx rgba(16, 185, 129, 0.4);
}

.actions {
  margin-bottom: 20rpx;
}

.back-btn {
  width: 100%;
  height: 80rpx;
  background: rgba(255, 255, 255, 0.15);
  color: #fff;
  border: 2rpx solid rgba(255, 255, 255, 0.3);
  border-radius: 40rpx;
  font-size: 30rpx;
}

.disclaimer {
  text-align: center;
  padding: 20rpx 0;
}

.disclaimer text {
  font-size: 22rpx;
  color: #777788;
}

/* Poster Modal */
.poster-modal {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.8);
  z-index: 999;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 40rpx;
  box-sizing: border-box;
}

.poster-container {
  background: #fff;
  border-radius: 16rpx;
  padding: 30rpx;
  max-width: 90%;
}

.poster-canvas {
  border-radius: 8rpx;
  display: block;
  margin: 0 auto 20rpx;
}

.poster-actions {
  display: flex;
  gap: 20rpx;
}

.save-btn, .close-btn {
  flex: 1;
  height: 70rpx;
  border-radius: 35rpx;
  font-size: 28rpx;
}

.save-btn {
  background: linear-gradient(135deg, #a78bfa 0%, #8b5cf6 100%);
  color: #fff;
  border: none;
}

.close-btn {
  background: #f3f4f6;
  color: #374151;
  border: none;
}
</style>
