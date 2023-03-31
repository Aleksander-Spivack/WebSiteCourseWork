const modal = document.querySelector('dialog')
const modalTriggerShow = document.getElementById('triggerOpen')
const modalTriggerShowVer = document.getElementById('triggerOpenVer')
const modalClose = document.getElementById('triggerClose')

const scrollbarWidth = parseInt(window.innerWidth) - parseInt(document.documentElement.clientWidth);

let isModalOpen = false

modalTriggerShow.addEventListener('click', (e) => {
  modal.showModal()
  modalTriggerShow.style.left = "calc(50% - " + (175 - scrollbarWidth / 2) + "px)";
  isModalOpen = true
  e.stopPropagation()

})

modalTriggerShowVer.addEventListener('click', (e) => {
  modal.showModal()
  modalTriggerShowVer.style.left = "calc(50% - " + (175 - scrollbarWidth / 2) + "px)";
  isModalOpen = true
  e.stopPropagation()
})

modalClose.addEventListener('click', () => {
  modal.close()
  isModalOpen = false
})

