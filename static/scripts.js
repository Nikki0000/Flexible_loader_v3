document.addEventListener('DOMContentLoaded', function () {
    const questionsContainer = document.getElementById('questionsContainer');
    let questionCount = 1;  // Счетчик вопросов

    document.getElementById('addQuestionButton').addEventListener('click', function () {
        const newQuestionBlock = document.createElement('div');
        newQuestionBlock.classList.add('question-block');
        newQuestionBlock.innerHTML = `
            <label for="questionText${questionCount}">Текст вопроса:</label>
            <input type="text" id="questionText${questionCount}" name="questions[${questionCount}][text]" required>

            <label for="headerSelect${questionCount}">Выберите заголовок:</label>
            <select id="headerSelect${questionCount}" name="questions[${questionCount}][header]" class="headerSelect" required>
                <option value="" disabled selected>Выберите заголовок</option>
                ${document.getElementById('headerSelect0').innerHTML} <!-- Копирование опций -->
            </select>

            <input type="text" id="headerText${questionCount}" name="questions[${questionCount}][customHeader]" class="headerText" placeholder="Введите заголовок" style="display: none;">

            <label for="answerType${questionCount}">Тип ответа:</label>
            <select id="answerType${questionCount}" name="questions[${questionCount}][answerType]" class="answerTypeSelect" required>
                <option value="" disabled selected>Выберите тип ответа</option>
                <option value="3">Числовой ответ</option>
                <option value="4">Выбор варианта ответа</option>
                <option value="5">Текстовый ответ</option>
            </select>

            <div class="answer-options-block" id="answerOptions${questionCount}" style="display: none;">
                <label>Варианты ответа:</label>
                <div class="answer-options-container" id="answerOptionsContainer${questionCount}">
                    <div class="answer-option">
                        <input type="text" name="questions[${questionCount}][options][]" placeholder="Введите вариант ответа" required>
                    </div>
                </div>
                <button type="button" class="add-option-button">Добавить вариант</button>
            </div>

            <button type="button" class="remove-question">Удалить вопрос</button>
        `;
        questionsContainer.appendChild(newQuestionBlock);
        questionCount++;
    });

    questionsContainer.addEventListener('change', function (event) {
        if (event.target.classList.contains('headerSelect')) {
            const headerSelect = event.target;
            const headerText = headerSelect.parentElement.querySelector('.headerText');

            if (headerSelect.value === 'other') {
                headerText.style.display = 'block';  // Показать поле для ввода собственного заголовка
                headerText.required = true;  // Сделать его обязательным
            } else {
                headerText.style.display = 'none';   // Скрыть поле для ввода собственного заголовка
                headerText.required = false;
            }
        }

        if (event.target.classList.contains('answerTypeSelect')) {
            const answerTypeSelect = event.target;
            const answerOptionsBlock = answerTypeSelect.parentElement.querySelector('.answer-options-block');

            if (answerTypeSelect.value === '4') {
                answerOptionsBlock.style.display = 'block';  // Показать блок для вариантов ответа
                const optionInputs = answerOptionsBlock.querySelectorAll('input[type="text"]');
                optionInputs.forEach(input => input.required = true);  // Сделать обязательными
            } else {
                answerOptionsBlock.style.display = 'none';   // Скрыть блок для вариантов ответа
                const optionInputs = answerOptionsBlock.querySelectorAll('input[type="text"]');
                optionInputs.forEach(input => input.required = false);  // Сделать необязательными
            }
        }
    });

    questionsContainer.addEventListener('click', function (event) {
        if (event.target.classList.contains('add-option-button')) {
            const optionsContainer = event.target.parentElement.querySelector('.answer-options-container');
            const newOption = document.createElement('div');
            newOption.classList.add('answer-option');
            newOption.innerHTML = `<input type="text" name="${optionsContainer.querySelector('input').name}" placeholder="Введите вариант ответа" required>`;
            optionsContainer.appendChild(newOption);
        }
    });

    questionsContainer.addEventListener('click', function (event) {
        if (event.target.classList.contains('remove-question')) {
            event.target.parentElement.remove();
        }
    });

    const taskTypesBlock = document.getElementById('taskTypesBlock');
    const toggleButton = document.getElementById('toggleTaskTypes');
    const taskTypesContainer = document.getElementById('taskTypesContainer');
    const selectedCount = document.getElementById('selectedCount');

    toggleButton.addEventListener('click', function () {
        taskTypesBlock.style.display = taskTypesBlock.style.display === 'none' ? 'block' : 'none';
    });

    taskTypesContainer.addEventListener('change', function () {
        const selectedOptions = taskTypesContainer.querySelectorAll('input[type="checkbox"]:checked');
        selectedCount.textContent = `Выбрано ${selectedOptions.length} типов задач`;
    });


    let specializationCount = 1;
    const specializationContainer = document.getElementById('specializationContainer');
    const addSpecializationButton = document.getElementById('addSpecializationButton');

    addSpecializationButton.addEventListener('click', function () {
        const newSpecializationBlock = document.createElement('div');
        newSpecializationBlock.classList.add('specialization-block');
        newSpecializationBlock.innerHTML = `
            <label for="specializationSelect${specializationCount}">Выберите специализацию ${specializationCount + 1}:</label>
            <select id="specializationSelect${specializationCount}" name="specialization[]" required>
                <option value="" disabled selected>Выберите специализацию</option>
                ${document.getElementById('specializationSelect0').innerHTML} <!-- Копирование списка специализаций -->
            </select>
        `;
        specializationContainer.appendChild(newSpecializationBlock);
        specializationCount++;
    });



});
