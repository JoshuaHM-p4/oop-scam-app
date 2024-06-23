class TemplateModel:
    """
    Represents a template model.

    Attributes:
        name (str): The name of the template.
        title (str): The title of the template.
        date (str): The date of the template.
        subject (str): The subject of the template.
    """

    def __init__(self, name: str, title: str, date, subject: str):
        self.name = name
        self.title = title
        self.date = date
        self.subject = subject

class HomeworkModel(TemplateModel):
    """
    Represents a homework template model.

    Attributes:
        name (str): The name of the homework.
        title (str): The title of the homework.
        date (str): The date of the homework.
        subject (str): The subject of the homework.
        questions (list[str]): The list of questions for the homework.
    """

    def __init__(self, name: str, title: str, date: str, subject: str, questions: list[str]):
        super().__init__(name, title, date, subject)
        self.questions = questions

class LetterModel(TemplateModel):
    """
    Represents a letter template model.

    Attributes:
        name (str): The name of the letter.
        title (str): The title of the letter.
        date (str): The date of the letter.
        subject (str): The subject of the letter.
        recipient (str): The recipient of the letter.
    """

    def __init__(self, name: str, title: str, date: str, subject: str, recipient: str):
        super().__init__(name, title, date, subject)
        self.recipient = recipient

class EssayModel(TemplateModel):
    """
    Represents an essay template model.

    Attributes:
        name (str): The name of the essay.
        title (str): The title of the essay.
        date (str): The date of the essay.
        subject (str): The subject of the essay.
        topic (str): The topic of the essay.
    """

    def __init__(self, name: str, title: str, date: str, subject: str, topic: str):
        super().__init__(name, title, date, subject)
        self.topic = topic

class MathModel(TemplateModel):
    """
    Represents a math template model.

    Attributes:
        name (str): The name of the math model.
        title (str): The title of the math model.
        date (str): The date of the math model.
        subject (str): The subject of the math model.
        problems (list[str]): A list of problems in the math model.
    """

    def __init__(self, name: str, title: str, date: str, subject: str, problems: list[str]):
        super().__init__(name, title, date, subject)
        self.problems = problems
