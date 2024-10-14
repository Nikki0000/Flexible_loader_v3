from flask import Flask, render_template, request, redirect, url_for, session
from models import get_engine, get_session
from services.usual_questionnaire_service import UsualQuestionnaireService
from sqlalchemy.orm import sessionmaker

app = Flask(__name__)

# Подключение к базе данных
db_connection = 'Подключение к БД'
engine = get_engine(db_connection)
SessionFactory = sessionmaker(bind=engine)


@app.route('/')
def index():
    # Передаем фабрику сессий в сервис
    questionnaire_service = UsualQuestionnaireService(SessionFactory)

    # Получаем необходимые данные для отображения
    headers = questionnaire_service.get_all_headers()
    task_types = questionnaire_service.get_all_task_types()
    specializations = questionnaire_service.get_all_specialization()

    questionnaire_service.close_session()

    return render_template('index.html', task_types=task_types, headers=headers, specializations=specializations)


@app.route('/submit', methods=['POST'])
def submit():




    # Получаем название анкеты
    questionnaire_name = request.form.get('questionnaireName')
    # Получаем список выбранных типов задач
    selected_task_types = request.form.getlist('taskTypes[]')
    # Получаем список выбранных специализаций
    selected_specialization = request.form.getlist('specialization[]')

    print(f"Название анкеты: {questionnaire_name}")
    print(f"Выбранные типы задач: {selected_task_types}")
    print(f"Выбранные специализации: {selected_specialization}")

    # Получаем выбранный заголовок
    # selected_headers = request.form.getlist('questions[0][header]')
    # Получаем текст для нового заголовка, если выбран пункт 'other'
    # new_header_name = request.form.get('questions[0][customHeader]').strip() if request.form.get('questions[0][customHeader]') else None

    # if selected_headers:
    #     selected_headers = [header.strip() for header in selected_headers]


    questions_data = []

    question_indices = set()
    for key in request.form.keys():
        if key.startswith('questions['):
            index = key.split('[')[1].split(']')[0]
            question_indices.add(index)

    question_indices = sorted(question_indices, key=int)

    for idx in question_indices:
        question_text = request.form.get(f'questions[{idx}][text]')
        question_header = request.form.get(f'questions[{idx}][header]')
        question_custom_header = request.form.get(f'questions[{idx}][customHeader]')
        question_type = request.form.get(f'questions[{idx}][answerType]')
        answer_options = request.form.getlist(f'questions[{idx}][options][]')

        questions_data.append({
            'text': question_text,
            'header': question_header,
            'custom_header': question_custom_header.strip() if question_custom_header else None,
            'answer_type': question_type,
            'answer_options': answer_options,
            'index': int(idx)
        })








    # Получаем текст вопроса и тип вопроса
    # question_text = request.form.get('questions[0][text]')
    # question_type = request.form.get('questions[0][answerType]')

    # Получаем возможные варианты ответа если это выбор
    # answer_option = request.form.get('answerOptions', '').split(',')


    questionnaire_service = UsualQuestionnaireService(SessionFactory)

    # Создаем анкету и связываем ее с выбранными типами задач
    questionnaire_id = questionnaire_service.create_questionnaire(questionnaire_name, selected_task_types, selected_specialization)

    try:
        for question in questions_data:

            selected_header = question['header']
            new_header_name = question['custom_header']

            # Проверка на "Другое"
            if selected_header == 'other' and not new_header_name:
                return "Ошибка: выбрано 'Другое', но новый заголовок не введен", 400


            if selected_header == 'other':
                selected_header_id = questionnaire_service.create_new_header(new_header_name)
            else:
                selected_header_id = int(selected_header)

            # # После обработки заголовка создаем вопрос
            # selected_header_id = questionnaire_service.create_new_header(
            #     new_header_name) if header == 'other' else int(header)



            # Используем метод process_submission для обработки каждого заголовка
            # questionnaire_service.process_submission(selected_task_types, header, new_header_name)



            # Создаем вопрос с учетом заголовка
            questionnaire_service.create_question(
                questionnaire_id=questionnaire_id,
                question_text=question['text'],
                question_type=question['answer_type'],
                header_id=selected_header_id,
                row_number=question['index'] + 1,
                answer_options=question['answer_options']
            )

        questionnaire_service.session.commit()


    except Exception as e:

        print(f"Ошибка при обработке вопросов: {e}")

        questionnaire_service.session.rollback()

        return "Произошла ошибка при сохранении анкеты.", 500



    questionnaire_service.close_session()

    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)





