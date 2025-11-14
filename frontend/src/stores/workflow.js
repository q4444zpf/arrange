import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useWorkflowStore = defineStore('workflow', () => {
  const nodes = ref([])
  const edges = ref([])
  const selectedNode = ref(null)
  const workflowInfo = ref({
    name: '未命名工作流',
    description: '',
    variables: {}
  })

  const addNode = (node) => {
    nodes.value.push(node)
  }

  const updateNode = (nodeId, updates) => {
    const index = nodes.value.findIndex(n => n.id === nodeId)
    if (index !== -1) {
      nodes.value[index] = { ...nodes.value[index], ...updates }
    }
  }

  const removeNode = (nodeId) => {
    nodes.value = nodes.value.filter(n => n.id !== nodeId)
    edges.value = edges.value.filter(e => e.source !== nodeId && e.target !== nodeId)
  }

  const addEdge = (edge) => {
    edges.value.push(edge)
  }

  const setWorkflow = (workflow) => {
    nodes.value = workflow.nodes || []
    edges.value = workflow.edges || []
    workflowInfo.value = {
      name: workflow.name,
      description: workflow.description,
      variables: workflow.variables || {}
    }
  }

  const clearWorkflow = () => {
    nodes.value = []
    edges.value = []
    selectedNode.value = null
    workflowInfo.value = {
      name: '未命名工作流',
      description: '',
      variables: {}
    }
  }

  return {
    nodes,
    edges,
    selectedNode,
    workflowInfo,
    addNode,
    updateNode,
    removeNode,
    addEdge,
    setWorkflow,
    clearWorkflow
  }
})
