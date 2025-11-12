import axios from 'axios'

const api = axios.create({
  baseURL: '/api',
  timeout: 30000
})

// 工具相关API
export const toolApi = {
  getTools: () => api.get('/tools/'),
  getTool: (id) => api.get(`/tools/${id}`),
  createTool: (data) => api.post('/tools/', data),
  deleteTool: (id) => api.delete(`/tools/${id}`)
}

// 工作流相关API
export const workflowApi = {
  getWorkflows: () => api.get('/workflows/'),
  getWorkflow: (id) => api.get(`/workflows/${id}`),
  createWorkflow: (data) => api.post('/workflows/', data),
  updateWorkflow: (id, data) => api.put(`/workflows/${id}`, data),
  deleteWorkflow: (id) => api.delete(`/workflows/${id}`)
}

// 执行相关API
export const executionApi = {
  executeWorkflow: (data) => api.post('/execution/run', data),
  getExecutionLog: (id) => api.get(`/execution/logs/${id}`)
}

export default api
