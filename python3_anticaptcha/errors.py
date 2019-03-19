class AntiCaptchaApiException(Exception):
    pass


class DownloadError(AntiCaptchaApiException):
    def __init__(self):
        AntiCaptchaApiException.__init__(self, """\nОшибка при скачивании файла""")


class ReadError(AntiCaptchaApiException):
    def __init__(self, error):
        AntiCaptchaApiException.__init__(
            self,
            """\nПораждается, при проблеме во время чтения сохранённого файла.
													\n\t{0}""".format(
                error
            ),
        )


class ParamError(AntiCaptchaApiException):
    def __init__(self, additional_info=None):
        AntiCaptchaApiException.__init__(
            self,
            """\nПораждается, при передаче неверного параметра.""" + additional_info
            if additional_info
            else "\n",
        )


class IdGetError(AntiCaptchaApiException):
    def __init__(self, server_answer):
        AntiCaptchaApiException.__init__(
            self,
            """\n Пораждается при ошибке получения ID капчи от сервиса. Ответ сервера:\n
											   {0}""".format(
                server_answer
            ),
        )
