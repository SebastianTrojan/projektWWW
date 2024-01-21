
    document.addEventListener("DOMContentLoaded", function () {
        const profileAvatar = document.getElementById("profile-avatar");
        const profileDropdown = document.getElementById("profile-dropdown");

        profileAvatar.addEventListener("click", function (event) {
            event.stopPropagation();
            profileDropdown.classList.toggle("show");
        });

        window.addEventListener("click", function () {
            if (profileDropdown.classList.contains("show")) {
                profileDropdown.classList.remove("show");
            }
        });
    });
