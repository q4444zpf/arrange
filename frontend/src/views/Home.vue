<template>
  <a-layout style="height: 100vh;">
    <a-layout-header style="background: #001529; display: flex; align-items: center; justify-content: space-between;">
      <div style="color: white; font-size: 20px; font-weight: bold;">🔧 API编排引擎</div>
      <a-space>
        <a-button type="primary" @click="router.push('/tools')">工具管理</a-button>
        <a-button type="primary" @click="createWorkflow">创建工作流</a-button>
      </a-space>
    </a-layout-header>
    
    <a-layout-content style="padding: 24px; background: #f0f2f5;">
      <a-card title="工作流列表" :bordered="false">
        <a-table 
          :columns="columns" 
          :data-source="workflows" 
          :loading="loading"
          row-key="id"
        >
          <template #bodyCell="{ column, record }">
            <template v-if="column.key === 'created_at'">
              {{ formatDate(record.created_at) }}
            </template>
            <template v-else-if="column.key === 'action'">
              <a-space>
                <a-button type="link" @click="editWorkflow(record.id)">编辑</a-button>
                <a-button type="link" @click="executeWorkflow(record)">执行</a-button>
                <a-popconfirm
                  title="确定要删除这个工作流吗？"
                  @confirm="deleteWorkflow(record.id)"
                >
                  <a-button type="link" danger>删除</a-button>
                </a-popconfirm>
              </a-space>
            </template>
          </template>
        </a-table>
      </a-card>
    </a-layout-content>

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

    <!-- 执行结果对话框 -->
    <a-modal
      v-model:open="resultModalVisible"
      title="执行结果"
      :footer="null"
      width="800px"
    >
      <a-descriptions bordered :column="1">
        <a-descriptions-item label="状态">
          <a-tag :color="executionResult.status === 'completed' ? 'success' : 'error'">
            {{ executionResult.status }}
          </a-tag>
        </a-descriptions-item>
        <a-descriptions-item label="输出结果">
          <pre style="max-height: 300px; overflow: auto;">{{ JSON.stringify(executionResult.output_data, null, 2) }}</pre>
        </a-descriptions-item>
        <a-descriptions-item label="执行日志">
          <div style="max-height: 300px; overflow: auto;">
            <div v-for="(log, index) in executionResult.logs" :key="index">
              <a-tag :color="getLogColor(log.level)">{{ log.level }}</a-tag>
              {{ log.message }}
            </div>
          </div>
        </a-descriptions-item>
      </a-descriptions>
    </a-modal>
  </a-layout>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { message } from 'ant-design-vue'
import { workflowApi, executionApi } from '../api'

const router = useRouter()

const columns = [
  { title: 'ID', dataIndex: 'id', key: 'id', width: 80 },
  { title: '名称', dataIndex: 'name', key: 'name' },
  { title: '描述', dataIndex: 'description', key: 'description' },
  { title: '创建时间', dataIndex: 'created_at', key: 'created_at' },
  { title: '操作', key: 'action', width: 200 }
]

const workflows = ref([])
const loading = ref(false)
const executeModalVisible = ref(false)
const resultModalVisible = ref(false)
const executing = ref(false)
const executeInputData = ref('{}')
const currentWorkflow = ref(null)
const executionResult = ref({})

onMounted(() => {
  loadWorkflows()
})

const loadWorkflows = async () => {
  loading.value = true
  try {
    const response = await workflowApi.getWorkflows()
    workflows.value = response.data
  } catch (error) {
    message.error('加载工作流列表失败')
  } finally {
    loading.value = false
  }
}

const createWorkflow = () => {
  router.push('/workflow')
}

const editWorkflow = (id) => {
  router.push(`/workflow/${id}`)
}

const executeWorkflow = (workflow) => {
  currentWorkflow.value = workflow
  executeInputData.value = '{}'
  executeModalVisible.value = true
}

const handleExecute = async () => {
  executing.value = true
  try {
    const inputData = JSON.parse(executeInputData.value)
    const response = await executionApi.executeWorkflow({
      workflow_id: currentWorkflow.value.id,
      input_data: inputData
    })
    executionResult.value = response.data
    executeModalVisible.value = false
    resultModalVisible.value = true
    message.success('工作流执行完成')
  } catch (error) {
    message.error('执行失败: ' + (error.response?.data?.detail || error.message))
  } finally {
    executing.value = false
  }
}

const deleteWorkflow = async (id) => {
  try {
    await workflowApi.deleteWorkflow(id)
    message.success('删除成功')
    loadWorkflows()
  } catch (error) {
    message.error('删除失败')
  }
}

const formatDate = (dateStr) => {
  return new Date(dateStr).toLocaleString('zh-CN')
}

const getLogColor = (level) => {
  const colors = {
    info: 'blue',
    success: 'green',
    error: 'red',
    warning: 'orange'
  }
  return colors[level] || 'default'
}
</script>

<style scoped>
pre {
  background: #f5f5f5;
  padding: 12px;
  border-radius: 4px;
  margin: 0;
}
</style>
