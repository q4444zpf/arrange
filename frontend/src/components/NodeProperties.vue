<template>
  <div v-if="selectedNode">
    <a-form layout="vertical">
      <a-form-item label="节点标签">
        <a-input v-model:value="selectedNode.data.label" @change="updateNode" />
      </a-form-item>

      <a-divider />

      <!-- 工具节点配置 -->
      <template v-if="selectedNode.data.type === 'tool'">
        <a-form-item label="工具">
          <a-select v-model:value="selectedNode.data.tool_id" @change="updateNode">
            <a-select-option v-for="tool in tools" :key="tool.id" :value="tool.id">
              {{ tool.name }}
            </a-select-option>
          </a-select>
        </a-form-item>

        <a-form-item label="输入参数">
          <div v-for="(value, key) in selectedNode.data.config.inputs" :key="key" style="margin-bottom: 8px;">
            <a-input
              v-model:value="selectedNode.data.config.inputs[key]"
              :placeholder="`${key} (支持 {{变量名}})`"
              @change="updateNode"
            >
              <template #addonBefore>{{ key }}</template>
            </a-input>
          </div>
          <a-button type="dashed" block @click="addInput">
            <template #icon><PlusOutlined /></template>
            添加参数
          </a-button>
        </a-form-item>

        <a-form-item label="输出变量名">
          <a-input 
            v-model:value="selectedNode.data.config.output_key" 
            placeholder="保存结果的变量名"
            @change="updateNode"
          />
        </a-form-item>
      </template>

      <!-- 条件节点配置 -->
      <template v-if="selectedNode.data.type === 'condition'">
        <a-form-item label="条件表达式">
          <a-textarea
            v-model:value="selectedNode.data.config.condition"
            :rows="3"
            placeholder="例如: {{score}} > 60"
            @change="updateNode"
          />
          <div style="margin-top: 8px; font-size: 12px; color: #999;">
            支持Python表达式，使用 {{变量名}} 引用变量
          </div>
        </a-form-item>
      </template>

      <!-- 循环节点配置 -->
      <template v-if="selectedNode.data.type === 'loop'">
        <a-form-item label="循环类型">
          <a-select v-model:value="selectedNode.data.config.loop_type" @change="updateNode">
            <a-select-option value="for">for循环</a-select-option>
            <a-select-option value="while">while循环</a-select-option>
          </a-select>
        </a-form-item>

        <template v-if="selectedNode.data.config.loop_type === 'for'">
          <a-form-item label="迭代变量">
            <a-input
              v-model:value="selectedNode.data.config.items_key"
              placeholder="要迭代的数组变量名"
              @change="updateNode"
            />
          </a-form-item>
          <a-form-item label="循环变量">
            <a-input
              v-model:value="selectedNode.data.config.item_var"
              placeholder="当前项的变量名"
              @change="updateNode"
            />
          </a-form-item>
        </template>

        <template v-if="selectedNode.data.config.loop_type === 'while'">
          <a-form-item label="循环条件">
            <a-textarea
              v-model:value="selectedNode.data.config.condition"
              :rows="2"
              placeholder="例如: {{counter}} < 10"
              @change="updateNode"
            />
          </a-form-item>
          <a-form-item label="最大迭代次数">
            <a-input-number
              v-model:value="selectedNode.data.config.max_iterations"
              :min="1"
              :max="1000"
              @change="updateNode"
            />
          </a-form-item>
        </template>
      </template>

      <!-- 代码节点配置 -->
      <template v-if="selectedNode.data.type === 'code'">
        <a-form-item label="Python代码">
          <a-textarea
            v-model:value="selectedNode.data.config.code"
            :rows="10"
            placeholder="# 可以使用 context 访问上下文变量&#10;result = context.get('var1', 0) + 1&#10;# 设置 result 作为输出"
            style="font-family: 'Courier New', monospace;"
            @change="updateNode"
          />
        </a-form-item>
        <a-form-item label="输出变量名">
          <a-input 
            v-model:value="selectedNode.data.config.output_key" 
            placeholder="保存结果的变量名"
            @change="updateNode"
          />
        </a-form-item>
      </template>

      <!-- 结束节点配置 -->
      <template v-if="selectedNode.data.type === 'end'">
        <a-form-item label="输出变量">
          <a-input
            v-model:value="selectedNode.data.config.output_key"
            placeholder="要作为最终输出的变量名"
            @change="updateNode"
          />
        </a-form-item>
      </template>

      <a-divider />
      
      <a-button danger block @click="deleteNode">
        <template #icon><DeleteOutlined /></template>
        删除节点
      </a-button>
    </a-form>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { message } from 'ant-design-vue'
import { PlusOutlined, DeleteOutlined } from '@ant-design/icons-vue'
import { useWorkflowStore } from '../stores/workflow'
import { toolApi } from '../api'

const workflowStore = useWorkflowStore()
const tools = ref([])

const selectedNode = computed(() => workflowStore.selectedNode)

onMounted(async () => {
  try {
    const response = await toolApi.getTools()
    tools.value = response.data
  } catch (error) {
    console.error('加载工具失败:', error)
  }
})

// 初始化配置
watch(selectedNode, (node) => {
  if (!node) return
  
  if (!node.data.config) {
    node.data.config = {}
  }
  
  // 初始化工具节点配置
  if (node.data.type === 'tool' && !node.data.config.inputs) {
    node.data.config.inputs = {}
  }
  
  // 初始化循环节点配置
  if (node.data.type === 'loop' && !node.data.config.loop_type) {
    node.data.config.loop_type = 'for'
    node.data.config.items_key = 'items'
    node.data.config.item_var = 'item'
  }
}, { immediate: true })

const updateNode = () => {
  // 触发更新
  workflowStore.updateNode(selectedNode.value.id, selectedNode.value)
}

const addInput = () => {
  const key = prompt('请输入参数名:')
  if (key && key.trim()) {
    if (!selectedNode.value.data.config.inputs) {
      selectedNode.value.data.config.inputs = {}
    }
    selectedNode.value.data.config.inputs[key.trim()] = ''
    updateNode()
  }
}

const deleteNode = () => {
  if (selectedNode.value.data.type === 'start') {
    message.warning('不能删除开始节点')
    return
  }
  workflowStore.removeNode(selectedNode.value.id)
  workflowStore.selectedNode = null
  message.success('节点已删除')
}
</script>
