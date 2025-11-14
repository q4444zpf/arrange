<template>
  <a-layout style="height: 100vh;">
    <a-layout-header style="background: #001529; display: flex; align-items: center; justify-content: space-between;">
      <a-space>
        <a-button type="text" style="color: white;" @click="router.push('/')">
          <template #icon><ArrowLeftOutlined /></template>
          返回
        </a-button>
        <a-divider type="vertical" style="background: rgba(255,255,255,0.3);" />
        <span style="color: white; font-size: 18px; font-weight: bold;">工具管理</span>
      </a-space>
      <a-button type="primary" @click="showCreateModal">创建工具</a-button>
    </a-layout-header>
    
    <a-layout-content style="padding: 24px; background: #f0f2f5;">
      <a-card :bordered="false">
        <a-table 
          :columns="columns" 
          :data-source="tools" 
          :loading="loading"
          row-key="id"
        >
          <template #bodyCell="{ column, record }">
            <template v-if="column.key === 'action'">
              <a-space>
                <a-button type="link" @click="editTool(record)">编辑</a-button>
                <a-popconfirm
                  title="确定要删除这个工具吗？"
                  @confirm="deleteTool(record.id)"
                >
                  <a-button type="link" danger>删除</a-button>
                </a-popconfirm>
              </a-space>
            </template>
          </template>
        </a-table>
      </a-card>
    </a-layout-content>

    <!-- 创建/编辑工具对话框 -->
    <a-modal
      v-model:open="modalVisible"
      :title="editingTool ? '编辑工具' : '创建工具'"
      @ok="handleSubmit"
      :confirm-loading="submitting"
      width="800px"
    >
      <a-form :model="formData" layout="vertical">
        <a-form-item label="工具名称" required>
          <a-input v-model:value="formData.name" placeholder="请输入工具名称" />
        </a-form-item>
        
        <a-form-item label="工具描述">
          <a-textarea v-model:value="formData.description" :rows="2" placeholder="请输入工具描述" />
        </a-form-item>
        
        <a-form-item label="分类">
          <a-select v-model:value="formData.category" placeholder="选择分类">
            <a-select-option value="API">API调用</a-select-option>
            <a-select-option value="数据处理">数据处理</a-select-option>
            <a-select-option value="文本处理">文本处理</a-select-option>
            <a-select-option value="其他">其他</a-select-option>
          </a-select>
        </a-form-item>
        
        <a-form-item label="输入参数配置（JSON）">
          <a-textarea 
            v-model:value="configStr" 
            :rows="4" 
            placeholder='[{"name": "param1", "type": "string", "required": true}]'
          />
        </a-form-item>
        
        <a-form-item label="Python代码" required>
          <a-textarea 
            v-model:value="formData.code" 
            :rows="12" 
            placeholder="def execute(inputs, context):&#10;    # 编写你的代码&#10;    result = inputs['param1']&#10;    return result"
            style="font-family: 'Courier New', monospace;"
          />
        </a-form-item>
      </a-form>
    </a-modal>
  </a-layout>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { message } from 'ant-design-vue'
import { ArrowLeftOutlined } from '@ant-design/icons-vue'
import { toolApi } from '../api'

const router = useRouter()

const columns = [
  { title: 'ID', dataIndex: 'id', key: 'id', width: 80 },
  { title: '名称', dataIndex: 'name', key: 'name' },
  { title: '描述', dataIndex: 'description', key: 'description' },
  { title: '分类', dataIndex: 'category', key: 'category' },
  { title: '操作', key: 'action', width: 150 }
]

const tools = ref([])
const loading = ref(false)
const modalVisible = ref(false)
const submitting = ref(false)
const editingTool = ref(null)
const configStr = ref('[]')

const formData = ref({
  name: '',
  description: '',
  category: 'API',
  code: `def execute(inputs, context):
    """
    工具执行函数
    :param inputs: 输入参数字典
    :param context: 上下文变量
    :return: 执行结果
    """
    # 在这里编写你的代码
    result = inputs.get('param1', '')
    return result`
})

onMounted(() => {
  loadTools()
})

const loadTools = async () => {
  loading.value = true
  try {
    const response = await toolApi.getTools()
    tools.value = response.data
  } catch (error) {
    message.error('加载工具列表失败')
  } finally {
    loading.value = false
  }
}

const showCreateModal = () => {
  editingTool.value = null
  formData.value = {
    name: '',
    description: '',
    category: 'API',
    code: `def execute(inputs, context):
    """
    工具执行函数
    :param inputs: 输入参数字典
    :param context: 上下文变量
    :return: 执行结果
    """
    # 在这里编写你的代码
    result = inputs.get('param1', '')
    return result`
  }
  configStr.value = '[]'
  modalVisible.value = true
}

const editTool = (tool) => {
  editingTool.value = tool
  formData.value = {
    name: tool.name,
    description: tool.description,
    category: tool.category,
    code: tool.code
  }
  configStr.value = JSON.stringify(tool.config, null, 2)
  modalVisible.value = true
}

const handleSubmit = async () => {
  submitting.value = true
  try {
    const config = JSON.parse(configStr.value)
    const data = {
      ...formData.value,
      config
    }
    
    if (editingTool.value) {
      // TODO: 实现更新接口
      message.info('编辑功能开发中')
    } else {
      await toolApi.createTool(data)
      message.success('创建成功')
      modalVisible.value = false
      loadTools()
    }
  } catch (error) {
    if (error instanceof SyntaxError) {
      message.error('配置JSON格式错误')
    } else {
      message.error('操作失败: ' + (error.response?.data?.detail || error.message))
    }
  } finally {
    submitting.value = false
  }
}

const deleteTool = async (id) => {
  try {
    await toolApi.deleteTool(id)
    message.success('删除成功')
    loadTools()
  } catch (error) {
    message.error('删除失败')
  }
}
</script>
