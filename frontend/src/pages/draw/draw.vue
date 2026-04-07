<template>
  <view class="container">
    <!-- 洗牌动画阶段 -->
    <view v-if="stage === 'shuffling'" class="shuffling-stage">
      <view class="title">🔮 塔罗牌正在洗牌中...</view>
      <view class="deck-container">
        <view
          v-for="(card, index) in shufflingCards"
          :key="index"
          class="shuffle-card"
          :style="getShuffleStyle(index)"
        >
          <view class="card-back">
            <view class="back-pattern">⭐</view>
          </view>
        </view>
      </view>
      <view class="hint">请稍候，塔罗牌正在排列...</view>
    </view>

    <!-- 抽牌阶段 -->
    <view v-if="stage === 'drawing'" class="drawing-stage">
      <view class="title">🎴 请抽取{{ cardCount }}张牌</view>
      <view class="cards-container">
        <view
          v-for="(card, index) in shuffledCards"
          :key="card.id"
          class="face-down-card"
          :class="{ flipped: card.selected }"
          @click="selectCard(index)"
        >
          <view class="card-inner">
            <!-- 背面 -->
            <view class="card-back">
              <view class="back-pattern">🔮</view>
            </view>
            <!-- 正面 -->
            <view class="card-front">
              <view class="card-content">
                <text class="card-name">{{ card.name }}</text>
              </view>
            </view>
          </view>
        </view>
      </view>
      <view class="hint">点击牌面翻开</view>
      <button
        v-if="selectedCount === cardCount"
        class="confirm-btn"
        @click="confirmDraw"
      >
        开始解读 ✨
      </button>
    </view>

    <!-- Loading 阶段 -->
    <view v-if="stage === 'loading'" class="loading-stage">
      <view class="loading-content">
        <view class="crystal-ball">🔮</view>
        <view class="loading-text">
          <text>塔罗师正在感应中</text>
          <text class="dots">{{ loadingDots }}</text>
        </view>
        <view class="hint">AI正在为你生成专属解读...</view>
      </view>
    </view>
  </view>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { onLoad } from '@dcloudio/uni-app'
import { divinate } from '@/utils/api.js'
import tarotData from '@/static/data/tarot.json'

const props = defineProps({})

const stage = ref('shuffling') // shuffling | drawing | loading
const cardCount = ref(1)
const theme = ref('')
const mbti = ref('')
const userQuestion = ref('')
const shuffledCards = ref([])
const selectedCount = computed(() => shuffledCards.value.filter(c => c.selected).length)
const loadingDots = ref('')
const shufflingCards = ref(new Array(10))

// 洗牌动画
function getShuffleStyle(index) {
  const angle = (index - 5) * 15
  const delay = index * 100
  return {
    '--rotation': `${angle}deg`,
    transform: `rotate(${angle}deg) translateX(${index * 15}rpx)`,
    animationDelay: `${delay}ms`
  }
}

// Fisher-Yates 洗牌
function shuffleCards() {
  const cards = [...tarotData]
  for (let i = cards.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1))
    ;[cards[i], cards[j]] = [cards[j], cards[i]]
  }
  // 取需要的数量 + 多几张供选择
  const selected = cards.slice(0, 10).map(card => ({
    ...card,
    selected: false,
    reversed: Math.random() < 0.5 // 50% 正逆位
  }))
  shuffledCards.value = selected
}

function selectCard(index) {
  if (shuffledCards.value[index].selected) return
  if (selectedCount.value >= cardCount.value) return

  shuffledCards.value[index].selected = true
}

async function confirmDraw() {
  stage.value = 'loading'

  // 收集选中的牌
  const drawnCards = shuffledCards.value.filter(c => c.selected).map(c => ({
    id: c.id,
    name: c.name,
    reversed: c.reversed
  }))

  try {
    const result = await divinate({
      theme: theme.value,
      mbti: mbti.value,
      question: userQuestion.value || null,
      cards: drawnCards
    })

    if (result.success) {
      // 增加使用次数
      const today = new Date().toDateString()
      const count = uni.getStorageSync('usedCount') || 0
      uni.setStorageSync('usedCount', count + 1)

      // 跳转结果页
      uni.redirectTo({
        url: `/pages/result/result?theme=${encodeURIComponent(theme.value)}&mbti=${mbti.value}&cards=${encodeURIComponent(JSON.stringify(drawnCards))}&interpretation=${encodeURIComponent(result.interpretation)}&quote=${encodeURIComponent(result.quote)}`
      })
    } else {
      uni.showToast({
        title: result.error || '生成失败，请重试',
        icon: 'none'
      })
      stage.value = 'drawing'
    }
  } catch (e) {
    console.error(e)
    uni.showToast({
      title: '网络错误，请重试',
      icon: 'none'
    })
    stage.value = 'drawing'
  }
}

onLoad((options) => {
  cardCount.value = parseInt(options.cardCount || 1)
  theme.value = options.theme
  mbti.value = options.mbti
  userQuestion.value = decodeURIComponent(options.question || '')

  // 开始洗牌动画
  shuffleCards()

  setTimeout(() => {
    stage.value = 'drawing'
  }, 3000)
})

// Loading dots animation
onMounted(() => {
  let dotCount = 0
  setInterval(() => {
    if (stage.value === 'loading') {
      dotCount = (dotCount + 1) % 4
      loadingDots.value = '.'.repeat(dotCount)
    }
  }, 500)
})
</script>

<style lang="scss" scoped>
.container {
  min-height: 100vh;
  background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
  padding: 40rpx 20rpx;
}

.title {
  text-align: center;
  font-size: 36rpx;
  color: #e8e8f0;
  margin-bottom: 60rpx;
}

/* 洗牌阶段 */
.shuffling-stage {
  .deck-container {
    position: relative;
    height: 500rpx;
    margin: 60rpx 0;
    display: flex;
    justify-content: center;
    align-items: center;
  }

  .shuffle-card {
    position: absolute;
    width: 280rpx;
    height: 480rpx;
    animation: shuffleDance 2s infinite ease-in-out;
    transform-origin: center center;
  }

  .card-back {
    width: 100%;
    height: 100%;
    background: linear-gradient(135deg, #6d28d9 0%, #4c1d95 100%);
    border-radius: 16rpx;
    display: flex;
    align-items: center;
    justify-content: center;
    border: 4rpx solid rgba(255, 255, 255, 0.3);
    box-shadow: 0 8rpx 24rpx rgba(0, 0, 0, 0.4);
  }

  .back-pattern {
    font-size: 60rpx;
  }

  .hint {
    text-align: center;
    color: #a8a8b8;
    font-size: 28rpx;
    margin-top: 40rpx;
  }
}

@keyframes shuffleDance {
  0%, 100% {
    transform: translateY(0) rotate(var(--rotation));
  }
  50% {
    transform: translateY(-20rpx) rotate(var(--rotation));
  }
}

/* 抽牌阶段 */
.drawing-stage {
  .cards-container {
    display: flex;
    flex-wrap: wrap;
    justify-content: center;
    gap: 20rpx;
  }

  .face-down-card {
    width: 180rpx;
    height: 300rpx;
    perspective: 1000rpx;

    &.flipped .card-inner {
      transform: rotateY(180deg);
    }
  }

  .card-inner {
    position: relative;
    width: 100%;
    height: 100%;
    transition: transform 0.6s;
    transform-style: preserve-3d;
  }

  .card-back, .card-front {
    position: absolute;
    width: 100%;
    height: 100%;
    backface-visibility: hidden;
    -webkit-backface-visibility: hidden;
    border-radius: 12rpx;
    overflow: hidden;
  }

  .card-back {
    background: linear-gradient(135deg, #6d28d9 0%, #4c1d95 100%);
    display: flex;
    align-items: center;
    justify-content: center;
    border: 3rpx solid rgba(255, 255, 255, 0.3);
    box-shadow: 0 4rpx 12rpx rgba(0, 0, 0, 0.3);
  }

  .back-pattern {
    font-size: 48rpx;
  }

  .card-front {
    background: linear-gradient(135deg, #fef3c7 0%, #f59e0b 100%);
    transform: rotateY(180deg);
    display: flex;
    align-items: center;
    justify-content: center;
    border: 3rpx solid #fbbf24;
  }

  .card-content {
    text-align: center;
  }

  .card-name {
    font-size: 28rpx;
    font-weight: bold;
    color: #1f2937;
  }
}

.hint {
  text-align: center;
  color: #a8a8b8;
  font-size: 26rpx;
  margin-top: 40rpx;
}

.confirm-btn {
  display: block;
  width: 80%;
  height: 90rpx;
  background: linear-gradient(135deg, #a78bfa 0%, #8b5cf6 100%);
  color: #fff;
  border: none;
  border-radius: 45rpx;
  font-size: 32rpx;
  font-weight: bold;
  margin: 40rpx auto 0;
  box-shadow: 0 8rpx 20rpx rgba(167, 139, 250, 0.4);
}

/* Loading阶段 */
.loading-stage {
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 80vh;

  .loading-content {
    text-align: center;
  }

  .crystal-ball {
    font-size: 160rpx;
    animation: pulse 2s infinite ease-in-out;
    margin-bottom: 40rpx;
  }

  .loading-text {
    font-size: 36rpx;
    color: #e8e8f0;
    margin-bottom: 20rpx;
  }

  .dots {
    color: #a8a8b8;
  }

  .hint {
    font-size: 28rpx;
    color: #888899;
  }
}

@keyframes pulse {
  0%, 100% {
    transform: scale(1);
    opacity: 1;
  }
  50% {
    transform: scale(1.1);
    opacity: 0.8;
  }
}
</style>
