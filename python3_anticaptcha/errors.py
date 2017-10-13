class AntiCaptchaError(Exception):
    """Базовый класс для всех исключений в этом модуле."""
    def __init__(self, description):
        if description=='ERROR_WRONG_USER_KEY':
            print(WrongUserKeyError.__doc__)



class WrongUserKeyError(AntiCaptchaError):
    """Исключение порождается при неправильном RuCaptcha KEY.
    Вы указали значение параметра key в неверном формате, ключ должен содержать 32 символа.
    Прекратите отправку запросов и проверьте ваш ключ API.

    ERROR_WRONG_USER_KEY - исключение из таблицы.
    """

'''
1	ERROR_KEY_DOES_NOT_EXIST	Авторизационный ключ не существует в системе или имеет неверный формат (длина не равняется 32 байтам)
2	ERROR_NO_SLOT_AVAILABLE	Нет свободных работников в данный момент, попробуйте позже либо повысьте свою максимальную ставку здесь
3	ERROR_ZERO_CAPTCHA_FILESIZE	Размер капчи которую вы загружаете менее 100 байт
4	ERROR_TOO_BIG_CAPTCHA_FILESIZE	Размер капчи которую вы загружаете более 500,000 байт
10	ERROR_ZERO_BALANCE	Баланс учетной записи ниже нуля или равен нулю
11	ERROR_IP_NOT_ALLOWED	Запрос с этого IP адреса с текущим ключом отклонен. Управление доступом по IP находится здесь
12	ERROR_CAPTCHA_UNSOLVABLE	5 разных работников не смогли разгадать капчу, задание остановлено
13	ERROR_BAD_DUPLICATES	Не хватило заданного количества дублей капчи для функции 100% распознавания.
14	ERROR_NO_SUCH_METHOD	Запрос в API выполнен на несуществующий метод
15	ERROR_IMAGE_TYPE_NOT_SUPPORTED	Формат капчи не распознан по EXIF заголовку либо не поддерживается. Допустимые форматы: JPG, GIF, PNG
16	ERROR_NO_SUCH_CAPCHA_ID	Капча с таким ID не была найдена в системе. Убедитесь что вы запрашиваете состояние капчи в течение 300 секунд после загрузки.
20	ERROR_EMPTY_COMMENT	Отсутствует комментарий в параметрах рекапчи версии API 1
21	ERROR_IP_BLOCKED	Доступ к API с этого IP запрещен из-за большого количества ошибок. Узнать причину можно здесь.
22	ERROR_TASK_ABSENT	Отсутствует задача в методе createTask.
23	ERROR_TASK_NOT_SUPPORTED	Тип задачи не поддерживается или указан не верно.
24	ERROR_INCORRECT_SESSION_DATA	Неполные или некорректные данные об эмулируемом пользователе. Все требуемые поля не должны быть пустыми.
25	ERROR_PROXY_CONNECT_REFUSED	Не удалось подключиться к прокси-серверу - отказ в подключении
26	ERROR_PROXY_CONNECT_TIMEOUT	Таймаут подключения к прокси-серверу
27	ERROR_PROXY_READ_TIMEOUT	Таймаут операции чтения прокси-сервера.
28	ERROR_PROXY_BANNED	Прокси забанен на целевом сервисе капчи
29	ERROR_PROXY_TRANSPARENT	Ошибка проверки прокси. Прокси должен быть не прозрачным, скрывать адрес конечного пользователя. 
В противном случае Google будет фильтровать запросы с IP нашего сервера. 
30	ERROR_RECAPTCHA_TIMEOUT	Таймаут загрузки скрипта рекапчи, проблема либо в медленном прокси, либо в медленном сервере Google
31	ERROR_RECAPTCHA_INVALID_SITEKEY	Ошибка получаемая от сервера рекапчи. Неверный/невалидный sitekey.
32	ERROR_RECAPTCHA_INVALID_DOMAIN	Ошибка получаемая от сервера рекапчи. Домен не соответствует sitekey.
33	ERROR_RECAPTCHA_OLD_BROWSER	Для задачи используется User-Agent неподдерживаемого рекапчей браузера.
34	ERROR_RECAPTCHA_STOKEN_EXPIRED	Параметр stoken устарел. Модифицируйте свое приложение, оно должно использовать stoken как можно быстрее.
35	ERROR_PROXY_HAS_NO_IMAGE_SUPPORT	Прокси не поддерживает передачу изображений с серверов Google
36	ERROR_PROXY_INCOMPATIBLE_HTTP_VERSION	Прокси не поддерживает длинные (длиной 2000 байт) GET запросы и не поддерживает SSL подключения
37	ERROR_FACTORY_SERVER_API_CONNECTION_FAILED	Не смогли подключиться к API сервера фабрики в течени 5 секунд.
38	ERROR_FACTORY_SERVER_BAD_JSON	
Неправильный JSON ответ фабрики, что-то сломалось.
39	ERROR_FACTORY_SERVER_ERRORID_MISSING	API фабрики не вернул обязательное поле errorId
40	ERROR_FACTORY_SERVER_ERRORID_NOT_ZERO	Ожидали errorId = 0 в ответе API фабрики, получили другое значение.
41	ERROR_FACTORY_MISSING_PROPERTY	Значения некоторых требуемых полей в запросе к фабрике отсутствуют. Клиент должен прислать все требуемы поля.
42	ERROR_FACTORY_PROPERTY_INCORRECT_FORMAT	
Тип значения не соответствует ожидаемому в структуре задачи фабрики. Клиент должен прислать значение с требуемым типом.
43	ERROR_FACTORY_ACCESS_DENIED	Доступ к управлению фабрикой принадлежит другой учетной записи. Проверьте свой ключ доступа.
44	ERROR_FACTORY_SERVER_OPERATION_FAILED	Общий код ошибки сервера фабрики.
45	ERROR_FACTORY_PLATFORM_OPERATION_FAILED	Общий код ошибки платформы.
46	ERROR_FACTORY_PROTOCOL_BROKEN	Ошибка в протоколе во время выполнения задачи фабрики.
47	ERROR_FACTORY_TASK_NOT_FOUND	Задача не найдена или недоступна для этой операции.
48	ERROR_FACTORY_IS_SANDBOXED	Фабрика находится в режиме песочницы, создание задач доступно только для владельца фабрики. Переведите фабрику в боевой режим, чтобы сделать ее доступной для всех клиентов.
'''