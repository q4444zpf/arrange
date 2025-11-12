<template>
  <div :class="['custom-node', `node-${data.type}`]" @click.stop>
    <Handle type="target" :position="Position.Top" />
    
    <div class="node-header">
      <component :is="getIcon()" class="node-icon" />
      <span class="node-label">{{ data.label }}</span>
    </div>
    
    <div v-if="data.config && Object.keys(data.config).length > 0" class="node-content">
      <div v-if="data.type === 'condition'" class="config-item">
        条件: {{ data.config.condition || '未设置' }}
      </div>
      <div v-if="data.type === 'loop'" class="config-item">
        循环: {{ data.config.loop_type || 'for' }}
      </div>
    </div>
    
    <Handle 
      v-if="data.type === 'condition'" 
      id="true" 
      type="source" 
      :position="Position.Right" 
      style="top: 40%; background: #52c41a;"
    />
    <Handle 
      v-if="data.type === 'condition'" 
      id="false" 
      type="source" 
      :position="Position.Right" 
      style="top: 60%; background: #ff4d4f;"
    />
    <Handle 
      v-if="data.type !== 'condition' && data.type !== 'end'" 
      type="source" 
      :position="Position.Bottom" 
    />
  </div>
</template>

<script setup>
import { Handle, Position } from '@vueflow/core'
import { 
  PlayCircleOutlined, 
  StopOutlined,
  BranchesOutlined,
  ReloadOutlined,
  CodeOutlined,
  ApiOutlined
} from '@ant-design/icons-vue'

const props = defineProps({
  data: Object,
  id: String
})

const getIcon = () => {
  const iconMap = {
    start: PlayCircleOutlined,
    end: StopOutlined,
    condition: BranchesOutlined,
    loop: ReloadOutlined,
    code: CodeOutlined,
    tool: ApiOutlined
  }
  return iconMap[props.data.type] || ApiOutlined
}
</script>

<style scoped>
.custom-node {
  padding: 12px 16px;
  border-radius: 8px;
  background: white;
  border: 2px solid #d9d9d9;
  min-width: 150px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  transition: all 0.3s;
}

.custom-node:hover {
  border-color: #1890ff;
  box-shadow: 0 4px 12px rgba(24, 144, 255, 0.3);
}

.node-start {
  border-color: #52c41a;
  background: linear-gradient(135deg, #f6ffed 0%, #ffffff 100%);
}

.node-end {
  border-color: #ff4d4f;
  background: linear-gradient(135deg, #fff1f0 0%, #ffffff 100%);
}

.node-condition {
  border-color: #faad14;
  background: linear-gradient(135deg, #fffbe6 0%, #ffffff 100%);
}

.node-loop {
  border-color: #13c2c2;
  background: linear-gradient(135deg, #e6fffb 0%, #ffffff 100%);
}

.node-code {
  border-color: #722ed1;
  background: linear-gradient(135deg, #f9f0ff 0%, #ffffff 100%);
}

.node-tool {
  border-color: #1890ff;
  background: linear-gradient(135deg, #e6f7ff 0%, #ffffff 100%);
}

.node-header {
  display: flex;
  align-items: center;
  gap: 8px;
  font-weight: 500;
}

.node-icon {
  font-size: 16px;
}

.node-label {
  font-size: 14px;
}

.node-content {
  margin-top: 8px;
  padding-top: 8px;
  border-top: 1px solid #f0f0f0;
  font-size: 12px;
  color: #666;
}

.config-item {
  margin: 4px 0;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}
</style>
