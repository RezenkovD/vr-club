document.addEventListener("DOMContentLoaded", function () {
        var body = document.querySelector("body")
        var headerA = document.querySelector(".header-container");
        var menuUL = document.querySelector(".navigation-container");
        var btnToggle = document.querySelector(".btn-toggle");
        var signContainer = document.querySelector(".sign-container");
        var btnToggle_ = document.getElementById("btn-toggle");
        var hiddenForHead = document.querySelector(".not-head");
        btnToggle.addEventListener("click", function () {
            if (menuUL.style.maxHeight) {
                menuUL.style.maxHeight = null;
                btnToggle_.innerHTML = '<svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 32 32" fill="none"><path fill-rule="evenodd" clip-rule="evenodd" d="M4.66683 6.66675C4.31321 6.66675 3.97407 6.80722 3.72402 7.05727C3.47397 7.30732 3.3335 7.64646 3.3335 8.00008C3.3335 8.3537 3.47397 8.69284 3.72402 8.94289C3.97407 9.19294 4.31321 9.33341 4.66683 9.33341L27.3335 9.33342C27.6871 9.33342 28.0263 9.19294 28.2763 8.94289C28.5264 8.69284 28.6668 8.3537 28.6668 8.00008C28.6668 7.64646 28.5264 7.30732 28.2763 7.05727C28.0263 6.80722 27.6871 6.66675 27.3335 6.66675L4.66683 6.66675ZM3.3335 16.0001C3.3335 15.6465 3.47397 15.3073 3.72402 15.0573C3.97407 14.8072 4.31321 14.6667 4.66683 14.6667L27.3335 14.6667C27.6871 14.6667 28.0263 14.8072 28.2763 15.0573C28.5264 15.3073 28.6668 15.6465 28.6668 16.0001C28.6668 16.3537 28.5264 16.6928 28.2763 16.9429C28.0263 17.1929 27.6871 17.3334 27.3335 17.3334L4.66683 17.3334C4.31321 17.3334 3.97407 17.1929 3.72402 16.9429C3.47397 16.6928 3.3335 16.3537 3.3335 16.0001ZM3.3335 24.0014C3.3335 23.6478 3.47397 23.3087 3.72402 23.0586C3.97407 22.8086 4.31321 22.6681 4.66683 22.6681L27.3335 22.6681C27.6871 22.6681 28.0263 22.8086 28.2763 23.0586C28.5264 23.3087 28.6668 23.6478 28.6668 24.0014C28.6668 24.355 28.5264 24.6942 28.2763 24.9442C28.0263 25.1943 27.6871 25.3347 27.3335 25.3347L4.66683 25.3347C4.31321 25.3347 3.97407 25.1943 3.72402 24.9442C3.47397 24.6942 3.3335 24.355 3.3335 24.0014Z" fill="#FCFCFC" /></svg>'
                headerA.style.position = ""
                var scrollPosition = window.scrollY;
                if (scrollPosition > 0) {
                    headerA.style.backgroundColor = "rgba(2, 2, 4, 0.70)";
                } else {
                    headerA.style.backgroundColor = "";
                }
                hiddenForHead.style.display = ""
                body.style.overflowY = "auto"
            } else {
                menuUL.style.maxHeight = "initial";
                btnToggle_.innerHTML = '<svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 32 32" fill="none"><path d="M25.3332 8.54675L23.4532 6.66675L15.9998 14.1201L8.5465 6.66675L6.6665 8.54675L14.1198 16.0001L6.6665 23.4534L8.5465 25.3334L15.9998 17.8801L23.4532 25.3334L25.3332 23.4534L17.8798 16.0001L25.3332 8.54675Z" fill="white"/></svg>'
                headerA.style.position = "fixed"
                headerA.style.background = ""
                hiddenForHead.style.display = "none"
                body.style.overflowY = "hidden"
            }

            if (signContainer.style.display === "flex") {
                signContainer.style.display = "none";
            } else {
                signContainer.style.display = "flex";
            }
        });
    });


// Почекати, поки сторінка завантажиться
window.addEventListener('load', function() {
    var header = document.querySelector('.header-container');
    var scrollPosition = window.scrollY;

    if (scrollPosition > 0) {
        header.style.backgroundColor = 'rgba(2, 2, 4, 0.70)';
        header.style.marginTop = '0';
        header.style.height = '64px';
    } else {
        header.style.backgroundColor = '';
        header.style.marginTop = '8px';
        header.style.height = '48px';
    }

    // Додати подію прокрутки після завантаження сторінки
    window.addEventListener('scroll', function() {
        var scrollPosition = window.scrollY;

        if (scrollPosition > 0) {
            header.style.backgroundColor = 'rgba(2, 2, 4, 0.70)';
            header.style.marginTop = '0';
            header.style.height = '64px';
        } else {
            header.style.backgroundColor = '';
            header.style.marginTop = '8px';
            header.style.height = '48px';
        }
    });
});
