<template>
  <a-layout style="height: 100vh;">
    <!-- 顶部工具栏 -->
    <a-layout-header style="background: #001529; display: flex; align-items: center; justify-content: space-between; padding: 0 24px;">
      <a-space>
        <a-button type="text" style="color: white;" @click="router.push('/')">
          <template #icon><ArrowLeftOutlined /></template>
          返回
        </a-button>
        <a-divider type="vertical" style="background: rgba(255,255,255,0.3);" />
        <a-input
          v-model:value="workflowStore.workflowInfo.name"
          style="width: 200px;"
          placeholder="工作流名称"
        />
      </a-space>
      <a-space>
        <a-button @click="saveWorkflow" :loading="saving">保存</a-button>
        <a-button type="primary" @click="showExecuteModal">执行</a-button>
      </a-space>
    </a-layout-header>

    <a-layout>
      <!-- 左侧节点面板 -->
      <a-layout-sider width="250" style="background: white; border-right: 1px solid #f0f0f0;">
        <div style="padding: 16px;">
          <h3 style="margin-bottom: 16px;">节点类型</h3>
          <a-collapse :bordered="false" default-active-key="['1', '2']">
            <a-collapse-panel key="1" header="基础节点">
              <div
                v-for="node in baseNodes"
                :key="node.type"
                class="node-item"
                draggable="true"
                @dragstart="onDragStart($event, node)"
              >
                <component :is="node.icon" style="margin-right: 8px;" />
                {{ node.label }}
              </div>
            </a-collapse-panel>
            
            <a-collapse-panel key="2" header="工具节点">
              <a-spin :spinning="loadingTools">
                <div
                  v-for="tool in tools"
                  :key="tool.id"
                  class="node-item"
                  draggable="true"
                  @dragstart="onDragStart($event, { type: 'tool', label: tool.name, tool_id: tool.id })"
                >
                  <ApiOutlined style="margin-right: 8px;" />
                  {{ tool.name }}
                </div>
              </a-spin>
            </a-collapse-panel>
          </a-collapse>
        </div>
      </a-layout-sider>

      <!-- 中间画布 -->
      <a-layout-content style="position: relative; background: #f5f5f5;">
        <VueFlow
          v-model:nodes="workflowStore.nodes"
          v-model:edges="workflowStore.edges"
          @node-click="onNodeClick"
          @drop="onDrop"
          @dragover="onDragOver"
          :default-zoom="1"
          :min-zoom="0.2"
          :max-zoom="4"
        >
          <Background pattern-color="#aaa" :gap="16" />
          <Controls />
          <MiniMap />
          
          <template #node-custom="props">
            <CustomNode :data="props.data" :id="props.id" />
          </template>
        </VueFlow>
      </a-layout-content>

      <!-- 右侧属性面板 -->
      <a-layout-sider width="350" style="background: white; border-left: 1px solid #f0f0f0;">
        <div style="padding: 16px;">
          <h3 style="margin-bottom: 16px;">节点属性</h3>
          <NodeProperties v-if="workflowStore.selectedNode" />
          <a-empty v-else description="请选择一个节点" />
        </div>
      </a-layout-sider>
    </a-layout>
  </a-layout>

  <!-- 执行对话框 -->
  <a-modal
    v-model:open="executeModalVisible"
    title="执行工作流"
    @ok="handleExecute"
    :confirm-loading="executing"
  >
    <a-form layout="vertical">
      <a-form-item label="输入数据（JSON格式）">
        <a-textarea
          v-model:value="executeInputData"
          :rows="8"
          placeholder='{"key": "value"}'
        />
      </a-form-item>
    </a-form>
  </a-modal>
</template>

<script setup>
import { ref, onMounted, nextTick } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { message } from 'ant-design-vue'
import { VueFlow, useVueFlow } from '@vueflow/core'
import { Background } from '@vueflow/background'
import { Controls } from '@vueflow/controls'
import { MiniMap } from '@vueflow/minimap'
import { 
  ArrowLeftOutlined, 
  PlayCircleOutlined, 
  StopOutlined,
  BranchesOutlined,
  ReloadOutlined,
  CodeOutlined,
  ApiOutlined
} from '@ant-design/icons-vue'
import { useWorkflowStore } from '../stores/workflow'
import { workflowApi, toolApi, executionApi } from '../api'
import CustomNode from '../components/CustomNode.vue'
import NodeProperties from '../components/NodeProperties.vue'

import '@vueflow/core/dist/style.css'
import '@vueflow/core/dist/theme-default.css'
import '@vueflow/controls/dist/style.css'
import '@vueflow/minimap/dist/style.css'

const route = useRoute()
const router = useRouter()
const workflowStore = useWorkflowStore()
const { project } = useVueFlow()

const saving = ref(false)
const loadingTools = ref(false)
const tools = ref([])
const executeModalVisible = ref(false)
const executing = ref(false)
const executeInputData = ref('{}')
const workflowId = ref(null)

const baseNodes = [
  { type: 'start', label: '开始', icon: PlayCircleOutlined },
  { type: 'end', label: '结束', icon: StopOutlined },
  { type: 'condition', label: '条件分支', icon: BranchesOutlined },
  { type: 'loop', label: '循环', icon: ReloadOutlined },
  { type: 'code', label: '代码', icon: CodeOutlined }
]

let nodeIdCounter = 1

onMounted(async () => {
  await loadTools()
  
  // 如果有ID，加载工作流
  if (route.params.id) {
    workflowId.value = parseInt(route.params.id)
    await loadWorkflow(workflowId.value)
  } else {
    // 新建工作流，添加开始节点
    addNode({ type: 'start', label: '开始' }, { x: 250, y: 50 })
  }
})

const loadTools = async () => {
  loadingTools.value = true
  try {
    const response = await toolApi.getTools()
    tools.value = response.data
  } catch (error) {
    message.error('加载工具列表失败')
  } finally {
    loadingTools.value = false
  }
}

const loadWorkflow = async (id) => {
  try {
    const response = await workflowApi.getWorkflow(id)
    workflowStore.setWorkflow(response.data)
  } catch (error) {
    message.error('加载工作流失败')
  }
}

const onDragStart = (event, nodeData) => {
  event.dataTransfer.setData('application/vueflow', JSON.stringify(nodeData))
  event.dataTransfer.effectAllowed = 'move'
}

const onDragOver = (event) => {
  event.preventDefault()
  event.dataTransfer.dropEffect = 'move'
}

const onDrop = (event) => {
  const data = JSON.parse(event.dataTransfer.getData('application/vueflow'))
  const position = project({ x: event.clientX, y: event.clientY })
  addNode(data, position)
}

const addNode = (nodeData, position) => {
  const id = `node_${nodeIdCounter++}`
  const newNode = {
    id,
    type: 'custom',
    position,
    data: {
      type: nodeData.type,
      label: nodeData.label,
      tool_id: nodeData.tool_id || null,
      config: {}
    }
  }
  workflowStore.addNode(newNode)
}

const onNodeClick = (event) => {
  workflowStore.selectedNode = event.node
}

const saveWorkflow = async () => {
  saving.value = true
  try {
    const data = {
      name: workflowStore.workflowInfo.name,
      description: workflowStore.workflowInfo.description,
      nodes: workflowStore.nodes,
      edges: workflowStore.edges,
      variables: workflowStore.workflowInfo.variables
    }

    if (workflowId.value) {
      await workflowApi.updateWorkflow(workflowId.value, data)
      message.success('保存成功')
    } else {
      const response = await workflowApi.createWorkflow(data)
      workflowId.value = response.data.id
      message.success('创建成功')
      router.replace(`/workflow/${workflowId.value}`)
    }
  } catch (error) {
    message.error('保存失败: ' + (error.response?.data?.detail || error.message))
  } finally {
    saving.value = false
  }
}

const showExecuteModal = () => {
  if (!workflowId.value) {
    message.warning('请先保存工作流')
    return
  }
  executeInputData.value = '{}'
  executeModalVisible.value = true
}

const handleExecute = async () => {
  executing.value = true
  try {
    const inputData = JSON.parse(executeInputData.value)
    const response = await executionApi.executeWorkflow({
      workflow_id: workflowId.value,
      input_data: inputData
    })
    message.success('执行完成')
    executeModalVisible.value = false
    
    // 可以显示执行结果
    console.log('执行结果:', response.data)
  } catch (error) {
    message.error('执行失败: ' + (error.response?.data?.detail || error.message))
  } finally {
    executing.value = false
  }
}
</script>

<style scoped>
.node-item {
  padding: 8px 12px;
  margin: 8px 0;
  background: #f5f5f5;
  border-radius: 4px;
  cursor: move;
  display: flex;
  align-items: center;
  transition: all 0.3s;
}

.node-item:hover {
  background: #e6f7ff;
  border-color: #1890ff;
}
</style>
