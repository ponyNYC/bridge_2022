document.addEventListener("DOMContentLoaded", (e) => {
  // Pop the model in thread.html if the ResponseForm
  // <textarea> (response.body) is preloaded with data
  const respForm = document.getElementById('response-form');
  const respText = respForm.body.value;
  const showModelBtn = document.getElementById('response-form-btn');

  if (respText) {
    showModelBtn.click();
    const modelHeader = document.querySelectorAll('.modal-header')[0];
    const modelFooter = document.querySelectorAll('.modal-footer')[0];
    const closeBtn = document.querySelectorAll('.btn-close')[0];
    const cancelBtn = document.getElementById('btn-cancel');
    const link = document.createElement('a');
    link.className = "btn btn-close";
    link.href = respForm.action.slice(0,-1) + '0'
    const subBtn = document.createElement('a');
    subBtn.className = "btn btn-secondary";
    subBtn.textContent = "Cancel";
    subBtn.href = respForm.action.slice(0,-1) + '0'
    modelHeader.removeChild(closeBtn);
    modelHeader.append(link);
    modelFooter.removeChild(cancelBtn);
    modelFooter.insertBefore(subBtn, modelFooter.firstChild)

    // console.log(modelHeader, modelFooter, closeBtn, cancelBtn);
  }
});
