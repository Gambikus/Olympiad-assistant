# Веретин Василий - "Olympiad assistant"
# Пользовательские сценарии

### Группа: 10 - МИ - 3
### Электронная почта: ver4vas@ya.ru
### VK: www.vk.com/gambikus


### [ Сценарий 1 - Регистрация пользователя ]

1. Пользователь вводит логин, с которым он будет заходить в систему
2. Пользователь вводит пароль, с которым он будет заходить в систему
3. Пользователь вводит адрес электронной почты, который будет использоваться в системе
4. Если выбранный логин уже существует в системе, то пользователю сообщается об этом и предлагается придумать новый логин
5. Если пароль содержит менее 6 символов, система сообщает, что пароль должен быть от 6 до 30 символов и пользователь должен придумать новый пароль
6. Если введённый адрес электронной почты не соответствует формату, то система выводит сообщение об ошибке и просит ввести адрес ещё раз
7. После успешной регистрации система приветствует пользователя и переходит в диалог выбора предпочитаемых олимпиад и ввод информации о себе.
8. Запускается Сценарий 2 - Выбор предпочитаемых олимпиад и ввод информации о себе.

### [ Сценарий 2 - Выбор предпочитаемых олимпиад и ввод информации о себе ]

1. Пользователь вводит свои ФИО.
2. Пользователь выбирает класс, за который будет писать олимпиады.
3. Пользователь вводит номер\название своей школы.
4. Пользователь вводит ближайший крупный населенный пункт.
5. Пользователь выбирает интересуемые ВУЗы.
6. Пользователь выбирает интересуемые уровни олимпиад: а) 1 уровень б) 2 уровень в) 3 уровень д) ВСОШ
7. Пользователь выбирает интересуемые предметы олимпиад(Математика, Информатика, Физика, Химия, Биология, География,  История, Обществознание, Право, Экономика, Русский язык, Литература, Лингвистика, Ин. языки, Астрономия, Экология, Робототехника, Технология, Искусство, ИЗО, Черчение, Психология, ОБЖ, Физкультура, Предпринимательство)
8. Запускается Сценарий 3 - Выбор олимпиад

### [ Сценарий 3 - Выбор олимпиад ]

1. Пользователь видит перед собой список олимпиад, которые удовлетворяют ранее введеным критериям.
2. Каждая олимпиада представляет из себя блок с названием олимпиады, уровнем, предметом и средней оценкой пользователей.
3. На каждом блоке присутствует кнопка "Отслеживать", которая позволит сформировать ленту новостей для пользователя.
4. Так же на каждом блоке присутствует кнопка "Подробнее", которая запускает Сценарий 4 - Профиль олимпиады.
5. Когда пользователь выберет все нужные олимпиады, он нажимает на кнопку "Перейти в ленту новостей" и запускается Сценарий 5 - Лента новостей.

### [ Сценарий 4 - Профиль олимпиады ]

1. Пользователь видит перед собой название и описание олимпиады.
2. Так же в профиле олимпиады есть информация о сроках проведения олимпиады, об уровне олимпиады, о этапах проведения.
3. Пользователь может перейти на сайт олимпиады, нажав на кнопку "Сайт олимпиады".
4. Так же пользователь может добавить олимпиаду в список отслеживаемых олимпиад, нажав на кнопку "Отслеживать".
5. Пользователь может посмотреть средние оценки других пользователей по разным критериям(Уровень сложности, уровень контроля и т.д.)
6. Так же пользователь может прочитать отзывы других пользователей касаемо этой олимпиады.
7. Нажав на кнопку "Оставить отзыв", пользователь перейдет к Сценарию 6 - написание отзыва об олимпиаде.

### [ Сценарий 5 - Лента новостей ]

1. Пользователь видит перед собой заголовки новостей о выбранных им олимпиадах.
2. Каждая новость содержит небольшой отрывок из новости и кнопкой "подробнее", нажатие на которую переносит на страницу новости.
3. На странице новости, помимо текста новости, присутсвует кнопка "В избранное", которая добавляет новость в избранное
4. Так же есть кнопка "Отписаться", которая позволяет пользователю не видеть больше новостей об этой олимпиаде.
5. Под текстом присутствует счетчик лайков, так же пользователь сам может оценить новость.
6. Далее находится ветки обусждения новости, где пользователь может прочитать чужие комментарии, ответить на них или написать свой.
7. Далее пользователь может открыть меню, откуда он может перейти свой профиль, отслеживаемые олимпиады или календарь олимпиад.

### [ Сценарий 6 - Написание отзыва об олимпиаде ]

1. Сначала пользователь оценивает отборочный этап олимпиады.
2. Если пользовотель не участвовал в отборочном этапе, то может перейти сразу к заключительному этапу.
3. Пользователь оценивает отборочный этап олимпиады от 1 до 10 по нескольким параматрам(Уровень сложности, уровень контроля и т.д.).
4. Затем, пользователь может заполняет текстовые поля "Плюсы", "Минусы" и "Отзыв".
5. Пользователь нажимает кнопку "Далее" и переходит к оценке заключительного этапа олимпиады.
6. Пользователь оценивает заключительный этап по подобию оценки отборочного.
7. В конце пользователь должен нажать кнопку "Опубликовать", чтобы опубликовать отзыв.

### [ Сценарий 7 - Календарь олимпиад ]

1. Пользователь видит перед собой календарь текущего года.
2. На календаре отмечены периоды, в которые проводятся отслеживаемя пользователем олимпиады.
3. Пользователь может выбрать олимпиады, которые не будут отображаться на календаре.
4. Пользователь может включить Push-уведомления для некоторых олимпиад.
5. Пользователь может перейти в профиль каждой олимпиады. 

