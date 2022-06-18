document.addEventListener("DOMContentLoaded", (e) => {
  // Pop the model in thread.html if the ResponseForm
  // <textarea> (response.body) is preloaded with data
  (function () {
    const respForm = document.getElementById('response-form');
    const respText = respForm.body.value;
    const showModelBtn = document.getElementById('response-form-btn');

    if (respText) showModelBtn.click();
  })();
});
