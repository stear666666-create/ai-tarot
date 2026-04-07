<template>
  <view class="container">
    <view class="header">
      <text class="title">✨ AI 灵眸塔罗</text>
      <text class="subtitle">结合MBTI性格的AI占卜</text>
    </view>

    <!-- 主题选择 -->
    <view class="section">
      <view class="section-title">🎯 选择占卜主题</view>
      <view class="theme-grid">
        <view
          v-for="theme in themes"
          :key="theme.id"
          class="theme-card"
          :class="{ active: selectedTheme === theme.id }"
          @click="selectTheme(theme.id)"
        >
          <text class="theme-icon">{{ theme.icon }}</text>
          <text class="theme-name">{{ theme.name }}</text>
          <text class="theme-desc">{{ theme.desc }}</text>
        </view>
      </view>
    </view>

    <!-- MBTI选择 -->
    <view class="section">
      <view class="section-title">🧭 选择你的MBTI</view>
      <view class="mbti-grid">
        <view
          v-for="mbti in mbtiList"
          :key="mbti"
          class="mbti-item"
          :class="{ active: selectedMbti === mbti }"
          @click="selectedMbti = mbti"
        >
          {{ mbti }}
        </view>
      </view>
    </view>

    <!-- 自定义问题 -->
    <view class="section">
      <view class="section-title">❓ 具体问题（选填）</view>
      <textarea
        v-model="userQuestion"
        class="question-input"
        placeholder="可以写下你具体想知道的问题，让解读更精准..."
        maxlength="200"
      />
    </view>

    <!-- 免责声明 -->
    <view class="disclaimer">
      <text>⚠️ 本内容仅供娱乐参考，不构成决策建议</text>
    </view>

    <!-- 开始按钮 -->
    <button
      class="start-btn"
      :disabled="!canStart"
      @click="startDivination"
    >
      开始占卜 ✨
    </button>

    <view class="remaining">
      <text>今日剩余免费次数：{{ remaining }}/{{ dailyLimit }}</text>
    </view>
  </view>
</template>

<script setup>
import { ref, computed } from 'vue'
import { onLoad } from '@dcloudio/uni-app'

const themes = ref([
  { id: 'daily', name: '每日一签', desc: '一日运势指引', icon: '🔮', cardCount: 1 },
  { id: 'love', name: '感情走向', desc: '你的情感关系', icon: '❤️', cardCount: 3 },
  { id: 'career', name: '事业发展', desc: '工作学业前途', icon: '💼', cardCount: 3 },
  { id: 'relation', name: '人际关系', desc: '人际相处分析', icon: '👥', cardCount: 3 }
])

const mbtiList = [
  'INTJ', 'INTP', 'ENTJ', 'ENTP',
  'INFJ', 'INFP', 'ENFJ', 'ENFP',
  'ISTJ', 'ISFJ', 'ESTJ', 'ESFJ',
  'ISTP', 'ISFP', 'ESTP', 'ESFP'
]

const selectedTheme = ref(null)
const selectedMbti = ref(null)
const userQuestion = ref('')
const remaining = ref(9999)
const dailyLimit = ref(9999)

const canStart = computed(() => {
  return selectedTheme.value !== null && selectedMbti.value !== null
})

function selectTheme(id) {
  selectedTheme.value = id
}

function startDivination() {
  if (!canStart.value) return

  const theme = themes.value.find(t => t.id === selectedTheme.value)

  uni.navigateTo({
    url: `/pages/draw/draw?cardCount=${theme.cardCount}&theme=${theme.name}&mbti=${selectedMbti.value}&question=${encodeURIComponent(userQuestion.value)}`
  })
}

onLoad(() => {
  // 从本地存储读取今日剩余次数
  const today = new Date().toDateString()
  const lastDate = uni.getStorageSync('lastDate')
  const count = uni.getStorageSync('usedCount')

  if (lastDate !== today) {
    remaining.value = dailyLimit.value
    uni.setStorageSync('lastDate', today)
    uni.setStorageSync('usedCount', 0)
  } else {
    remaining.value = Math.max(0, dailyLimit.value - (count || 0))
  }
})
</script>

<style lang="scss" scoped>
.container {
  min-height: 100vh;
  padding: 20rpx;
  background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
}

.header {
  text-align: center;
  padding: 60rpx 0 40rpx;
}

.title {
  display: block;
  font-size: 48rpx;
  font-weight: bold;
  background: linear-gradient(90deg, #e8d5b7, #f4e4c1);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  margin-bottom: 10rpx;
}

.subtitle {
  display: block;
  font-size: 28rpx;
  color: #a8a8b8;
}

.section {
  margin: 30rpx 0;
}

.section-title {
  font-size: 32rpx;
  color: #e8e8f0;
  margin-bottom: 20rpx;
  padding-left: 10rpx;
}

.theme-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 20rpx;
}

.theme-card {
  background: rgba(255, 255, 255, 0.08);
  border: 2rpx solid rgba(255, 255, 255, 0.15);
  border-radius: 16rpx;
  padding: 30rpx 20rpx;
  text-align: center;
  transition: all 0.3s;

  &.active {
    background: rgba(167, 139, 250, 0.3);
    border-color: #a78bfa;
    box-shadow: 0 0 20rpx rgba(167, 139, 250, 0.4);
  }
}

.theme-icon {
  display: block;
  font-size: 48rpx;
  margin-bottom: 10rpx;
}

.theme-name {
  display: block;
  font-size: 30rpx;
  color: #fff;
  font-weight: 500;
  margin-bottom: 6rpx;
}

.theme-desc {
  display: block;
  font-size: 24rpx;
  color: #a8a8b8;
}

.mbti-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 16rpx;
}

.mbti-item {
  background: rgba(255, 255, 255, 0.08);
  border: 2rpx solid rgba(255, 255, 255, 0.15);
  border-radius: 12rpx;
  padding: 20rpx 10rpx;
  text-align: center;
  font-size: 28rpx;
  color: #d0d0e0;
  transition: all 0.3s;

  &.active {
    background: rgba(167, 139, 250, 0.3);
    border-color: #a78bfa;
    color: #fff;
  }
}

.question-input {
  width: 100%;
  min-height: 120rpx;
  background: rgba(255, 255, 255, 0.08);
  border: 2rpx solid rgba(255, 255, 255, 0.15);
  border-radius: 12rpx;
  padding: 20rpx;
  color: #fff;
  font-size: 28rpx;
  box-sizing: border-box;
}

.disclaimer {
  text-align: center;
  margin: 20rpx 0;
}

.disclaimer text {
  font-size: 24rpx;
  color: #888899;
}

.start-btn {
  width: 100%;
  height: 90rpx;
  background: linear-gradient(135deg, #a78bfa 0%, #8b5cf6 100%);
  color: #fff;
  border: none;
  border-radius: 45rpx;
  font-size: 32rpx;
  font-weight: bold;
  margin-top: 20rpx;
  box-shadow: 0 8rpx 20rpx rgba(167, 139, 250, 0.4);

  &:disabled {
    opacity: 0.5;
  }
}

.remaining {
  text-align: center;
  margin-top: 20rpx;
}

.remaining text {
  font-size: 24rpx;
  color: #888899;
}
</style>
