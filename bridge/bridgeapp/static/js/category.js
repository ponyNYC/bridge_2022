document.addEventListener("DOMContentLoaded", (e) => {
  // Pop the model in thread.html if the ResponseForm
  // <textarea> (response.body) is preloaded with data
  (function () {
    const submitButton = document.getElementById("submit-btn");
    const checkbox1 = document.getElementById("id_category_ids_0");
    const checkbox2 = document.getElementById("id_category_ids_1");
    const checkbox3 = document.getElementById("id_category_ids_2");
    const checkboxChecks = [checkbox1.checked, checkbox2.checked, checkbox3.checked]

    submitButton.addEventListener('mouseover', (e) => {
      if (!checkboxChecks.some(el => el)) {
        alert("You must check at least one of the checkboxes to submit your question!")
      }
    });
  })();
});
