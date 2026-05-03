import { ref } from 'vue'

export function useImageUpload() {
  const uploadedImage = ref(null)
  const editedImage = ref(null)

  function readFile(file) {
    if (!file || !file.type.startsWith('image/')) return
    const reader = new FileReader()
    reader.onload = (e) => {
      uploadedImage.value = e.target.result
      editedImage.value = null
    }
    reader.readAsDataURL(file)
  }

  function handleUpload(e) {
    readFile(e.target.files[0])
  }

  function handleDrop(e) {
    readFile(e.dataTransfer.files[0])
  }

  function clear() {
    uploadedImage.value = null
    editedImage.value = null
  }

  return { uploadedImage, editedImage, handleUpload, handleDrop, clear }
}
