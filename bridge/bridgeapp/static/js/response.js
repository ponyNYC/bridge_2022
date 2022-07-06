document.addEventListener("DOMContentLoaded", (e) => {
  // Pop the model in thread.html if the ResponseForm
  // <textarea> (response.body) is preloaded with data
  const respForm = document.getElementById('response-form');
  const respText = respForm.body.value;
  const showModalBtn = document.getElementById('response-form-btn');

  if (respText) {
    showModalBtn.click();
    const modalHeader = document.querySelector('.modal-header');
    const modalFooter = document.querySelector('.modal-footer');
    const closeBtn = document.querySelector('.btn-close');
    const cancelBtn = document.getElementById('btn-cancel');
    const link = document.createElement('a');
    link.className = "btn btn-close";
    link.href = respForm.action.slice(0,-1) + '0'
    const subBtn = document.createElement('a');
    subBtn.className = "btn btn-secondary";
    subBtn.textContent = "Cancel";
    subBtn.href = respForm.action.slice(0,-1) + '0'
    modalHeader.removeChild(closeBtn);
    modalHeader.append(link);
    modalFooter.removeChild(cancelBtn);
    modalFooter.insertBefore(subBtn, modalFooter.firstChild)
    // console.log(modalHeader, modalFooter, closeBtn, cancelBtn);
  }
});
