document.addEventListener("DOMContentLoaded", (e) => {
    // Pop the model in thread.html if the ResponseForm
    // <textarea> (response.body) is preloaded with data
    (function () {
        const navbar = document.querySelector(".navbar");
        let scrollpos = window.scrollY;

        function checkScroll() {
            scrollpos = window.scrollY;
            if (scrollpos > 100) {
                navbar.className =
                    "navbar navbar-expand-md navbar-dark bg-secondary fixed-top shadow-lg";
            } else {
                navbar.className =
                    "navbar navbar-expand-md navbar-dark fixed-top";
            }
        }

        window.addEventListener("scroll", checkScroll);
    })();
});
