// Перевірка на обраність слоту
document.getElementById('bookingForm').addEventListener('submit', function (event) {
        const peopleCountInput = document.getElementById('id_people_count');
        const peopleCount = parseInt(peopleCountInput.value);
        const checkboxes = document.getElementsByName('slots');
        let hasSelectedSlots = false;
        checkboxes.forEach(checkbox => {
            if (checkbox.checked) {
                hasSelectedSlots = true;
            }
        });
        if (!hasSelectedSlots || peopleCount < 1) {
            event.preventDefault();
        }
    });
// Блокування слотів, якщо вільного сеансу немає
    function updateSlotAvailability() {
        const form = document.querySelector('form');
        const peopleCountInput = form.querySelector('#id_people_count');
        const slotsFormCheck = form.querySelectorAll('.form-check');
        const peopleCount = parseInt(peopleCountInput.value);
        let max_av_slot = 0;
        let hasUnavailableSlot = false;

        slotsFormCheck.forEach(formCheck => {
            const labels = formCheck.querySelectorAll('label');
            const label = labels[0];
            const avSlotLabel = labels[2];
            const avSlot = avSlotLabel.innerText.trim().split(' ')[0]; // Отримуємо кількість місць
            const checkbox = formCheck.querySelector('input[type="checkbox"]');

            if (avSlot > max_av_slot){
                max_av_slot = avSlot;
            }

            if (avSlot > 0 && peopleCount <= avSlot) {
                label.removeAttribute('disabled');
                checkbox.style.border = '1px solid #4FB4FE';
                label.style.opacity = '1';
                label.style.pointerEvents = 'auto';
                avSlotLabel.style.color = "#4FB4FE"
            }
            else {
                label.setAttribute('disabled', true);
                checkbox.style.border = '1px solid #9F9F9F'; // Встановлюємо фон зі змінної --form-background, коли неактивний
                label.style.opacity = '0.5';
                label.style.pointerEvents = 'none';
                avSlotLabel.style.color = "#9F9F9F";
                if (checkbox.checked) {
                    hasUnavailableSlot = true; // Перевіряємо, чи обраний слот має недостатньо місць
                }
            }
        });
        const bookingButton = document.getElementById('bookingButton');
        if (hasUnavailableSlot || peopleCount < 1) {
            bookingButton.setAttribute('disabled', true);
            bookingButton.style.opacity = '0.5';
            bookingButton.style.pointerEvents = 'none';
            bookingButton.style.background = "#9F9F9F";
        } else {
            bookingButton.removeAttribute('disabled');
            bookingButton.style.opacity = '1';
            bookingButton.style.pointerEvents = 'auto';
            bookingButton.style.background = "#4FB4FE";
        }
        if (max_av_slot < peopleCount){
            bookingButton.setAttribute('disabled', true);
            bookingButton.style.opacity = '0.5';
            bookingButton.style.pointerEvents = 'none';
            bookingButton.style.background = "#9F9F9F";
        }
    }
    const peopleCountInput = document.querySelector('#id_people_count');
    const minusButton = document.querySelector('.number-input div[onclick*="stepDown"]');
    const plusButton = document.querySelector('.number-input div[onclick*="stepUp"]');

    peopleCountInput.addEventListener('input', updateSlotAvailability);
    plusButton.addEventListener('click', updateSlotAvailability);
    minusButton.addEventListener('click', updateSlotAvailability);

    updateSlotAvailability();


// Можливість обрати лише два сумісних слоти
    function isCompatible(checkbox1, checkbox2) {
        const compatiblePairs = [
            ['id_slots_0', 'id_slots_1'],
            ['id_slots_1', 'id_slots_2'],
            ['id_slots_2', 'id_slots_3'],
            ['id_slots_3', 'id_slots_4'],
            ['id_slots_4', 'id_slots_5'],
            ['id_slots_5', 'id_slots_6'],
            ['id_slots_6', 'id_slots_7'],
            ['id_slots_7', 'id_slots_8'],
            ['id_slots_8', 'id_slots_9']
        ];
        return compatiblePairs.some(pair => {
            return (
                (checkbox1.id === pair[0] && checkbox2.id === pair[1]) ||
                (checkbox1.id === pair[1] && checkbox2.id === pair[0])
            );
        });
    }
    function limitCheckboxSelection(checkbox) {
        const maxAllowedChecked = 2;

        const checkboxes = document.getElementsByName('slots');
        let checkedCount = 0;

        for (let i = 0; i < checkboxes.length; i++) {
            if (checkboxes[i].checked) {
                checkedCount++;
            }
        }
        if (checkedCount > maxAllowedChecked) {
            for (let i = 0; i < checkboxes.length; i++) {
                if (checkboxes[i].checked && checkboxes[i] !== checkbox) {
                    checkboxes[i].checked = false;
                }
            }
        }
        for (let i = 0; i < checkboxes.length; i++) {
            if (checkboxes[i] !== checkbox && !isCompatible(checkbox, checkboxes[i])) {
                checkboxes[i].checked = false;
            }
        }
        updateSlotAvailability();
    }
    const checkboxes = document.getElementsByName('slots');
    checkboxes.forEach(checkbox => {
        checkbox.addEventListener('click', function () {
            limitCheckboxSelection(this);
        });
    });
// Підрахунок грошей
    function calculateTotalCost() {
        const slotCost = 200;
        const peopleCountInput1 = document.querySelector('#id_people_count');
        const peopleCount1 = parseInt(peopleCountInput1.value);

        const checkboxes1 = document.getElementsByName('slots');
        let selectedSlots = 0;
        checkboxes1.forEach(checkbox => {
            if (checkbox.checked) {
                selectedSlots++;
            }
        });

        let totalCost = 0;
        if (peopleCount1 > 0 && selectedSlots > 0) {
            totalCost = slotCost * selectedSlots * peopleCount1;
        }

        const totalCostElement = document.getElementById('total_cost');
        totalCostElement.textContent = totalCost.toFixed(2) + ' грн';
    }
    const peopleCountInput1 = document.querySelector('#id_people_count');
    peopleCountInput1.addEventListener('input', calculateTotalCost);
    const checkboxes1 = document.getElementsByName('slots');
    checkboxes1.forEach(checkbox => {
        checkbox.addEventListener('click', function () {
            limitCheckboxSelection(this);
            calculateTotalCost();
        });
    });

    const btnMinus = document.querySelector('.number-input div[onclick*="stepDown"]');
    btnMinus.addEventListener('click', function () {
        const peopleCountInput = document.querySelector('#id_people_count');
        const peopleCount = parseInt(peopleCountInput.value);
        peopleCountInput.value = peopleCount;
        calculateTotalCost();
    });

    const btnPlus = document.querySelector('.number-input div[onclick*="stepUp"]');
    btnPlus.addEventListener('click', function () {
        const peopleCountInput = document.querySelector('#id_people_count');
        const peopleCount = parseInt(peopleCountInput.value);
        peopleCountInput.value = peopleCount;
        calculateTotalCost();
    });
