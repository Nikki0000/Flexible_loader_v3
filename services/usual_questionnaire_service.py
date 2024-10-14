from click import option
from flask import session

from models import QuestionnaireHeader, TaskType
from sqlalchemy.orm import sessionmaker
from datetime import datetime

from models.question import Question
from models.question_configuration import QuestionConfiguration
from models.questiona_answer import QuestionAnswer
from models.questionnaire import Questionnaire
from models.questionnaire_to_task_type import QuestionnaireToTaskType
from models.questionnaire_to_task_type_specialization import QuestionnaireToTaskTypeSpecialization
from models.specialization import Specialization


class UsualQuestionnaireService:

    def __init__(self, sesion_factory: sessionmaker):
        self.session = sesion_factory()

    # Получаем данные из таблицы QuestionnaireHeader
    def get_all_headers(self):
        return self.session.query(QuestionnaireHeader).all()

    # Получаем данных из таблицы TaskType
    def get_all_task_types(self):
        return self.session.query(TaskType).all()

    # Получаем данные из таблицы Specialization (отсортированные по названию)
    def get_all_specialization(self):
        return self.session.query(Specialization).order_by(Specialization.Name).all()



    # Создание анкеты и добавление связки с TaskType
    def create_questionnaire(self, questionnaire_name, task_type_ids, specialization_ids):
        try:
            new_questionnaire = Questionnaire(
                Name=questionnaire_name,
                CreatedOn=datetime.now(),
                ModifiedOn=datetime.now()
            )
            self.session.add(new_questionnaire)
            self.session.flush() # Сразу получаем Id созданной анкеты
            print(f"Новая анкета {new_questionnaire} была добавлена")

            # Добавляем запись в QuestionnaireToTaskType
            order = 0
            for task_type_id in task_type_ids:
                new_link = QuestionnaireToTaskType(
                    QuestionnaireId=new_questionnaire.Id,
                    TaskTypeId=int(task_type_id),
                    Order=order,
                    CreatedOn=datetime.now(),
                    ModifiedOn=datetime.now()
                )
                self.session.add(new_link)
                self.session.flush()

                for specialization_id in specialization_ids:
                    new_specialization_link = QuestionnaireToTaskTypeSpecialization(
                        QuestionnaireId = new_questionnaire.Id,
                        SpecializationId = specialization_id,
                        QuestionnaireToTaskTypeId = new_link.Id,
                        CreatedOn = datetime.now(),
                        ModifiedOn = datetime.now()
                    )
                    self.session.add(new_specialization_link)

                order += 1

            print(f"Получены идендификаторы TaskType: {task_type_ids}")
            print(f"Получены идентификаторы Specialization: {specialization_ids}")

            #self.session.commit()

            return new_questionnaire.Id


        except Exception as e:
            print(f"Ошибка при создании анкеты: {e}")
            self.session.rollback()
            raise e






    # Если был выбран заголовок "другой" (other), создаем новый заголовок
    # def process_submission(self, selected_task_type, selected_header, new_header_name):
    #
    #     try:
    #         # Логика обработки выбранных типов задач
    #         if selected_task_type:
    #             print("Выбраны типы задач:", selected_task_type)
    #
    #         print(f"Получено значение selected_header: {selected_header}")
    #         print(f"Получено значение new_header_name: {new_header_name}")
    #
    #         # Логика обработки заголовка
    #         if selected_header == 'other':
    #             if new_header_name:
    #                 # Создаем новый заголовок, если выбрана опция "Другое" и введен новый заголовок
    #                 selected_header_id = self.create_new_header(new_header_name)
    #                 print(f"Создан новый заголовок с ID: {selected_header_id}")
    #             else:
    #                 raise ValueError("Выбрано 'Другое', но новый заголовок не введен")
    #         elif selected_header.isdigit():
    #             # Если выбран существующий заголовок, преобразуем его в int
    #             selected_header_id = int(selected_header)
    #             print(f"Использован существующий заголовок с ID: {selected_header_id}")
    #         else:
    #             # Если заголовок не выбран и новый не введен, вызываем исключение
    #             raise ValueError("Не выбран существующий заголовок и не введен новый заголовок")
    #
    #         # Коммитим изменения после обработки
    #         self.session.commit()
    #     except Exception as e:
    #         print(f"Ошибка при обработке данных: {e}")
    #         self.session.rollback()
    #         raise e
        # finally:
        #     # Закрываем сессию после всех операций
        #     self.session.close()




    # Проверяем существует ли заголовок с таким именем
    def create_new_header(self, header_text: str):
        try:
            existing_header = self.session.query(QuestionnaireHeader).filter_by(Name=header_text).first()

            if existing_header:
                print(f"Заголовок '{header_text}' уже существует.")
                return existing_header.Id
            else:
                new_header = QuestionnaireHeader(
                    Name=header_text,
                    CreatedOn=datetime.now(),
                    ModifiedOn=datetime.now(),
                    Visible=True,
                    Position=1
                )
                self.session.add(new_header)
                self.session.flush()
                print(f"Заголовок '{header_text}' был добавлен")
                return new_header.Id
        except Exception as e:
            print(f"Ошибка при добавлении нового заголовка: {e}")
            self.session.rollback()
            raise e




    # Логика определения позиции header
    def _get_next_position(self):
        max_position = self.session.query(QuestionnaireHeader.Position).order_by(QuestionnaireHeader.Position.desc().first)
        return (max_position[0] + 1) if max_position else 1


    # Создание вопроса и его конфигурации
    def create_question(self, questionnaire_id, question_text, question_type, header_id, row_number, answer_options=None):
        try:
            new_question = Question(
                Name=question_text,
                Type=question_type,
                QuestionnaireId=questionnaire_id,
                Order=row_number,
                CreatedOn=datetime.now(),
                ModifiedOn=datetime.now()
            )
            self.session.add(new_question)
            self.session.flush()


            new_question_configuration = QuestionConfiguration(
                QuestionId=new_question.Id,
                QuestionnaireHeaderId=header_id,
                RowNumber=row_number,
                CreatedOn=datetime.now(),
                ModifiedOn=datetime.now()
            )

            self.session.add(new_question_configuration)


            if question_type == "4" and answer_options:
                answer_options = [option.strip() for option in answer_options if option.strip()]
                if answer_options:
                    order = 0
                    for option in answer_options:
                        new_answer = QuestionAnswer(
                            QuestionId=new_question.Id,
                            Order=order,
                            Name=option,
                            CreatedOn=datetime.now(),
                            ModifiedOn=datetime.now()
                        )
                        self.session.add(new_answer)
                        order += 1


            self.session.commit()
            print(f"Вопрос '{question_text}' был добавлен")
        except Exception as e:
            print(f"Ошибка при создании вопроса: {e}")
            self.session.rollback()
            raise e


    # def create_questionnaire_to_task_type(self, questionnaire_id, selected_task_types):
    #     questionnaire_to_task_type = QuestionnaireToTaskType(
    #         QuestionnaireId = questionnaire_id,
    #         TaskTypeId = selected_task_types,
    #         CreatedOn = datetime.now(),
    #         ModifiedOn = datetime.now(),
    #         Order = 0
    #     )
    #     self.session.add(questionnaire_to_task_type)
    #     self.session.commit()




    def close_session(self):
        self.session.close()
