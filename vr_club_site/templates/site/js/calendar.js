// Calendar
document.addEventListener("DOMContentLoaded", function () {
    const monthDiv = document.getElementById("month");
    const daysDiv = document.getElementById("days");
    const prevMonthBtn = document.getElementById("prevMonthBtn");
    const nextMonthBtn = document.getElementById("nextMonthBtn");
    let currentYear, currentMonth;

    async function generateCalendar(year, month) {
        const now = new Date();
        const daysInMonth = new Date(year, month + 1, 0).getDate();
        const firstDayIndex = new Date(year, month, 0).getDay();
        const lastDayIndex = new Date(year, month, daysInMonth).getDay();
        const lastDayPrevMonth = new Date(year, month, 0).getDate();

        const months = [
            "Січень",
            "Лютий",
            "Березень",
            "Квітень",
            "Травень",
            "Червень",
            "Липень",
            "Серпень",
            "Вересень",
            "Жовтень",
            "Листопад",
            "Грудень",
        ];

        monthDiv.innerHTML = months[month] + " " + year;

        let days = "";

        for (let i = firstDayIndex; i > 0; i--) {
            days += `<div class="transparent-wrap"></div>`;
        }

        let today = now.getDate();
        let number;
        let day_;
        for (let i = 1; i <= daysInMonth; i++) {
            day_ = i
            number = i;
            if (number < 10) {
                number = "0" + number;
            }
            if (i === now.getDate() && month === now.getMonth() && year === now.getFullYear()) {
                today = i;
                days += `<div class="wrap" onclick="openPopup('${number}', '${month + 1}', '${year}')" data-day="${day_}" style="cursor: pointer;"><div class="blue-background"></div><div class="today" style="color: #001729;">${number}</div><div class="count_place" style="color: #001729;"></div></div>`;
            } else {
                if (i < today && month <= now.getMonth() && year <= now.getFullYear() || month < now.getMonth() && year <= now.getFullYear() || month > now.getMonth() && year < now.getFullYear() || i >= today && month === now.getMonth() && year < now.getFullYear()) {
                    days += `<div class="wrap"><div class="no-change"></div><div class="old-day">${number}</div></div>`;
                }
                else {
                    days += `<div class="wrap" onclick="openPopup('${number}', '${month + 1}', '${year}')" data-day="${day_}" style="cursor: pointer;"><div class="us-background"></div><div class="base-day">${number}</div><div class="count_place"></div></div>`;
                }
            }
        }
        await getAvailableSlotsMonth(year, month)

        for (let i = 1; i < 7 - lastDayIndex; i++) {
            days += `<div class="transparent-wrap"></div>`;
        }

        daysDiv.innerHTML = days;

        if (currentMonth == 0) {
            prevMonthBtn.innerHTML = months[11];
        }
        else {
            prevMonthBtn.innerHTML = months[currentMonth - 1];
        }

        if (currentMonth + 1 > 11) {
            nextMonthBtn.innerHTML = months[0];
        }
        else {
            nextMonthBtn.innerHTML = months[currentMonth + 1];
        }

        const prevMonth_ = document.getElementById("prevMonth");
        if (currentYear === now.getFullYear() && currentMonth === now.getMonth()) {
            prevMonth_.style.opacity = 0;
            prevMonth_.style.cursor = "default"
        } else {
            prevMonth_.style.opacity = 1;
            prevMonth_.style.cursor = "pointer"
        }

    }

    function updateCalendar() {
        generateCalendar(currentYear, currentMonth);
    }

    function prevMonth() {
        if (currentYear !== now.getFullYear() || currentMonth !== now.getMonth()) {
            currentMonth--;
            if (currentMonth < 0) {
                currentMonth = 11;
                currentYear--;
            }
            updateCalendar();
        }
    }

    const maxMonthsAhead = 2;

    function nextMonth() {
        const currentDate = new Date(currentYear, currentMonth);

        const maxAllowedDate = new Date();
        maxAllowedDate.setMonth(maxAllowedDate.getMonth() + maxMonthsAhead - 1);

        if (currentDate > maxAllowedDate) {
            return;
        }
        currentMonth++;
        if (currentMonth > 11) {
            currentMonth = 0;
            currentYear++;
        }
        updateCalendar();
    }

    // Встановлюємо початковий місяць на поточний місяць.
    const now = new Date();
    currentYear = now.getFullYear();
    currentMonth = now.getMonth();
    generateCalendar(currentYear, currentMonth);


    prevMonthBtn.addEventListener("click", prevMonth);
    nextMonthBtn.addEventListener("click", nextMonth);
});
var popupScrollPosition;
async function openPopup(day, month, year) {
    popupScrollPosition = window.scrollY;
    const dateDiv = document.querySelector('.booking-date');
    const monthsNames = [
        "січня",
        "лютого",
        "березня",
        "квітня",
        "травня",
        "червня",
        "липня",
        "серпня",
        "вересня",
        "жовтня",
        "листопада",
        "грудня",
    ];

    dateDiv.textContent = `${parseInt(day, 10)} ${monthsNames[parseInt(month) - 1]} ${year}`;

    await getAvailableSlots(`${year}-${parseInt(month, 10)}-${parseInt(day, 10)}`)
    const dateInput = document.getElementById('id_date');
    dateInput.value = `${day}-${month}-${year}`;

    const popup = document.getElementById('popup');
    const body = document.querySelector('body');
    popup.style.display = 'block';
    body.style.overflow = 'hidden';
    history.pushState(null, null, '');
}

function closePopup() {
    const popup = document.getElementById('popup');
    const body = document.querySelector('body');
    popup.style.display = 'none';
    body.style.overflow = 'auto';
    window.scrollTo(0, popupScrollPosition);
    history.pushState(null, null, '');
    const checkboxes = document.querySelectorAll('input[type="checkbox"]');
    checkboxes.forEach(checkbox => {
        checkbox.checked = false;
    });
    const inputElements = document.querySelectorAll('input[type="text"]');
    inputElements.forEach(input => {
        input.value = '';
    });
    const peopleCountInput = document.getElementById('id_people_count');
    peopleCountInput.value = 1;
    const totalCostSpan = document.getElementById('total_cost');
    totalCostSpan.textContent = '0.00 грн';
}

window.addEventListener('popstate', function(event) {
    var state = event.state;

    if (state && state.popupOpen) {
        openPopup(state.day, state.month, state.year);
    } else {
        closePopup();
    }
});

