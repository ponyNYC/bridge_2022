document.addEventListener("DOMContentLoaded", (e) => {
    // Pop the model in thread.html if the ResponseForm
    // <textarea> (response.body) is preloaded with data
    const threadForm = document.getElementById("thread-form");
    const checkbox1 = document.getElementById("id_category_ids_0");
    const checkbox2 = document.getElementById("id_category_ids_1");
    const checkbox3 = document.getElementById("id_category_ids_2");
    const checkboxes = [checkbox1, checkbox2, checkbox3];

    threadForm.addEventListener("submit", (e) => {
        if (!checkboxes.some((el) => el.checked)) {
            e.preventDefault();
            alert(
                "You must check at least one of the checkboxes to submit your question!"
            );
        }
    });
});
