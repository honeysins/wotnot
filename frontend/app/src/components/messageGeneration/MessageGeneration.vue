<template>
  <div class="message-generation-container">
    <div class="header">
      <h2 class="text-2xl font-bold text-gray-800 mb-4">
        <i class="fas fa-magic mr-2"></i>
        AI Message Generator
      </h2>
      <p class="text-gray-600 mb-6">
        Generate professional messages using AI. Enter your prompt and get a customized message that you can edit and use.
      </p>
    </div>

    <div class="generation-form">
      <div class="form-group">
        <label for="prompt" class="block text-sm font-medium text-gray-700 mb-2">
          Message Prompt *
        </label>
        <textarea
          v-model="prompt"
          id="prompt"
          rows="4"
          placeholder="e.g., I am trying to send a Diwali wish to my customers, can you please build a message"
          class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
          required
        ></textarea>
        <p class="text-xs text-gray-500 mt-1">
          Describe what kind of message you want to generate
        </p>
      </div>

      <div class="form-actions">
        <button
          @click="generateMessage"
          :disabled="isLoading || !prompt"
          class="bg-blue-600 text-white px-6 py-2 rounded-md hover:bg-blue-700 disabled:bg-gray-400 disabled:cursor-not-allowed flex items-center"
        >
          <i v-if="isLoading" class="fas fa-spinner fa-spin mr-2"></i>
          <i v-else class="fas fa-magic mr-2"></i>
          {{ isLoading ? 'Generating...' : 'Generate Message' }}
        </button>
      </div>
    </div>

    <!-- Generated Message Section -->
    <div v-if="generatedMessage" class="generated-message-section">
      <div class="section-header">
        <h3 class="text-lg font-semibold text-gray-800 mb-2">
          <i class="fas fa-robot mr-2"></i>
          Generated Message
        </h3>
        <div class="action-buttons">
          <button
            @click="copyMessage"
            class="text-blue-600 hover:text-blue-800 text-sm font-medium"
          >
            <i class="fas fa-copy mr-1"></i>
            Copy
          </button>
          <button
            @click="regenerateMessage"
            :disabled="isLoading"
            class="text-green-600 hover:text-green-800 text-sm font-medium ml-4"
          >
            <i class="fas fa-redo mr-1"></i>
            Regenerate
          </button>
        </div>
      </div>

      <div class="message-preview">
        <textarea
          v-model="editableMessage"
          rows="6"
          class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
          placeholder="Generated message will appear here..."
        ></textarea>
      </div>

      <div class="message-actions">
        <button
          @click="useMessage"
          class="bg-green-600 text-white px-4 py-2 rounded-md hover:bg-green-700"
        >
          <i class="fas fa-check mr-2"></i>
          Use This Message
        </button>
        <button
          @click="clearMessage"
          class="bg-gray-600 text-white px-4 py-2 rounded-md hover:bg-gray-700 ml-2"
        >
          <i class="fas fa-times mr-2"></i>
          Clear
        </button>
      </div>
    </div>

    <!-- Error Message -->
    <div v-if="errorMessage" class="error-message">
      <div class="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded-md">
        <div class="flex items-center">
          <i class="fas fa-exclamation-triangle mr-2"></i>
          <span>{{ errorMessage }}</span>
        </div>
      </div>
    </div>

    <!-- Success Message -->
    <div v-if="successMessage" class="success-message">
      <div class="bg-green-100 border border-green-400 text-green-700 px-4 py-3 rounded-md">
        <div class="flex items-center">
          <i class="fas fa-check-circle mr-2"></i>
          <span>{{ successMessage }}</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'MessageGeneration',
  data() {
    return {
      prompt: '',
      generatedMessage: '',
      editableMessage: '',
      isLoading: false,
      errorMessage: '',
      successMessage: ''
    }
  },
  methods: {
    async generateMessage() {
      if (!this.prompt) {
        this.errorMessage = 'Please provide a prompt'
        return
      }

      this.isLoading = true
      this.errorMessage = ''
      this.successMessage = ''

      try {
        const response = await axios.post(
          `${process.env.VUE_APP_API_URL}/generate-message`,
          {
            prompt: this.prompt
          },
          {
            headers: {
              'Authorization': `Bearer ${localStorage.getItem('token')}`,
              'Content-Type': 'application/json'
            }
          }
        )

        if (response.data.success) {
          this.generatedMessage = response.data.generated_message
          this.editableMessage = response.data.generated_message
          this.successMessage = 'Message generated successfully!'
        } else {
          this.errorMessage = response.data.error || 'Failed to generate message'
        }
      } catch (error) {
        console.error('Error generating message:', error)
        if (error.response && error.response.data && error.response.data.detail) {
          this.errorMessage = error.response.data.detail
        } else {
          this.errorMessage = 'Failed to generate message. Please try again.'
        }
      } finally {
        this.isLoading = false
      }
    },

    async regenerateMessage() {
      await this.generateMessage()
    },

    copyMessage() {
      if (this.editableMessage) {
        navigator.clipboard.writeText(this.editableMessage).then(() => {
          this.successMessage = 'Message copied to clipboard!'
          setTimeout(() => {
            this.successMessage = ''
          }, 3000)
        }).catch(() => {
          this.errorMessage = 'Failed to copy message'
        })
      }
    },

    useMessage() {
      if (this.editableMessage) {
        // Emit event to parent component or handle message usage
        this.$emit('message-generated', this.editableMessage)
        this.successMessage = 'Message is ready to use!'
        setTimeout(() => {
          this.successMessage = ''
        }, 3000)
      }
    },

    clearMessage() {
      this.generatedMessage = ''
      this.editableMessage = ''
      this.errorMessage = ''
      this.successMessage = ''
    }
  }
}
</script>

<style scoped>
.message-generation-container {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
}

.header {
  text-align: center;
  margin-bottom: 30px;
}

.generation-form {
  background: #f8f9fa;
  padding: 25px;
  border-radius: 10px;
  margin-bottom: 30px;
}

.form-group {
  margin-bottom: 20px;
}

.form-actions {
  text-align: center;
}

.generated-message-section {
  background: #ffffff;
  border: 1px solid #e5e7eb;
  border-radius: 10px;
  padding: 25px;
  margin-bottom: 20px;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 15px;
}

.action-buttons {
  display: flex;
  gap: 15px;
}

.message-preview {
  margin-bottom: 20px;
}

.message-actions {
  text-align: center;
}

.error-message,
.success-message {
  margin-top: 20px;
}

@media (max-width: 768px) {
  .message-generation-container {
    padding: 15px;
  }
  
  .section-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 10px;
  }
  
  .action-buttons {
    width: 100%;
    justify-content: flex-start;
  }
}
</style>
