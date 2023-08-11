const carousel = document.querySelector(".carousel");
const firstCard = carousel.querySelector(".card");
const cardWidth = firstCard.offsetWidth;
const cardMarginRight = parseInt(window.getComputedStyle(firstCard).marginRight);

let isDragging = false;
let startX, startScrollLeft;

const calculateCardPerView = () => {
    return Math.round(carousel.offsetWidth / (cardWidth + cardMarginRight));
};

const addCloneCards = () => {
    const cardPerView = calculateCardPerView();
    const allCards = [...carousel.querySelectorAll(".card")];
    allCards.slice(-cardPerView).forEach((card) => {
        carousel.insertAdjacentHTML("afterbegin", card.outerHTML);
    });
    allCards.slice(0, cardPerView).forEach((card) => {
        carousel.insertAdjacentHTML("beforeend", card.outerHTML);
    });
};

const dragStart = (e) => {
    isDragging = true;
    carousel.classList.add("dragging");
    startX = e.pageX - carousel.offsetLeft;
    startScrollLeft = carousel.scrollLeft;
};

const dragging = (e) => {
    if (!isDragging) return;
    const x = e.pageX - carousel.offsetLeft;
    const walk = (x - startX) * 2;
    carousel.scrollLeft = startScrollLeft - walk;
};

const dragStop = () => {
    isDragging = false;
    carousel.classList.remove("dragging");
};

const infiniteScroll = () => {
    if (carousel.scrollLeft <= 0) {
        carousel.scrollLeft = carousel.scrollWidth - carousel.offsetWidth;
    } else if (carousel.scrollLeft >= carousel.scrollWidth - carousel.offsetWidth) {
        carousel.scrollLeft = 0;
    }
};

carousel.addEventListener("mousedown", dragStart);
document.addEventListener("mousemove", dragging);
document.addEventListener("mouseup", dragStop);
carousel.addEventListener("scroll", infiniteScroll);

window.addEventListener("resize", () => {
    const cardPerView = calculateCardPerView();
    if (cardPerView !== Math.round(carousel.offsetWidth / (cardWidth + cardMarginRight))) {
        carousel.innerHTML = ""; // Clear carousel
        addCloneCards();
        carousel.scrollLeft = carousel.offsetWidth;
    }
});

addCloneCards();
carousel.scrollLeft = carousel.offsetWidth;
