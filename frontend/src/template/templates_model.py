from docx import Document
from docx.shared import Pt, Inches, RGBColor
from docx.enum.text import WD_TAB_ALIGNMENT

class TemplateModel:
    """
    Represents a template model.

    Attributes:
        name (str): The name of the template.
        title (str): The title of the template.
        date (str): The date of the template.
        subject (str): The subject of the template.
        professor (str): The professor of the template.
        section (str): The section of the template.
    """

    def __init__(self, name: str, title: str, date, subject: str, professor: str = None, section: str = None):
        self.name = name
        self.title = title
        self.date = date
        self.subject = subject
        self.professor = professor
        self.section = section

        self.COLOR = RGBColor(0, 0, 0)
        self.FONT = "Cambria"

    def __str__(self):
        return f"{self.name} - {self.title} - {self.date} - {self.subject} - {self.professor} - {self.section}"

    def create_header(self, filename: str):
        """
        Creates a header for the template.

        Args:
            filename (str): The name of the file to save the header to.

        Returns:
            None
        """
        doc = Document()

        # Add and Edit Section
        section = doc.sections[0]
        section.top_margin = Inches(0.8)
        section.bottom_margin = Inches(0.8)
        section.left_margin = Inches(1)
        section.right_margin = Inches(1)

        # Add Header
        header = section.header

        # Edit Styles
        doc.styles["Heading 1"].font.size = Pt(20)
        doc.styles["Heading 1"].font.name = self.FONT
        doc.styles["Heading 1"].font.bold = True
        doc.styles["Heading 1"].font.color.rgb = self.COLOR

        doc.styles["Heading 2"].font.size = Pt(13)
        doc.styles["Heading 2"].font.name = self.FONT
        doc.styles["Heading 2"].font.bold = True
        doc.styles["Heading 2"].font.color.rgb = self.COLOR

        doc.styles["Body Text"].font.size = Pt(13)
        doc.styles["Body Text"].font.name = self.FONT
        doc.styles["Body Text"].font.bold = False
        doc.styles["Body Text"].font.color.rgb = self.COLOR

        # Adding Header Content
        header_content = [
            self.subject,
            self.title,
            f"{self.name}\t\t{self.date}"
        ]

        # SUBJECT
        header.paragraphs[0].text = header_content[0].upper()
        header.paragraphs[0].style = doc.styles["Heading 1"]
        header.paragraphs[0].paragraph_format.space_before = Pt(5)
        header.paragraphs[0].paragraph_format.space_after = Pt(0)

        # Title
        paragraph = header.add_paragraph(header_content[1], style = doc.styles["Heading 2"])
        paragraph.paragraph_format.space_before = Pt(5)
        paragraph.paragraph_format.space_after = Pt(0)

        # Name and Date
        paragraph = header.add_paragraph(header_content[2], style = doc.styles["Body Text"])
        paragraph.paragraph_format.space_after = Pt(0)
        tab_stops = paragraph.paragraph_format.tab_stops
        tab_stops.add_tab_stop(Inches(1), alignment=WD_TAB_ALIGNMENT.LEFT)
        tab_stops.add_tab_stop(Inches(6), alignment=WD_TAB_ALIGNMENT.RIGHT)

        # Professor and Section
        if self.professor and self.section:
            header_content.append(f"{self.professor}\t\t{self.section}")
            paragraph = header.add_paragraph(header_content[3], style = doc.styles["Body Text"])
            paragraph.paragraph_format.space_after = Pt(0)
            tab_stops = paragraph.paragraph_format.tab_stops
            tab_stops.add_tab_stop(Inches(1), alignment=WD_TAB_ALIGNMENT.LEFT)
            tab_stops.add_tab_stop(Inches(6), alignment=WD_TAB_ALIGNMENT.RIGHT)

        # Add Line
        header.add_paragraph("_"*90, style = doc.styles["Body Text"])

        doc.save(filename)


class HomeworkModel(TemplateModel):
    """
    Represents a homework template model.

    Attributes:
        name (str): The name of the homework.
        title (str): The title of the homework.
        date (str): The date of the homework.
        subject (str): The subject of the homework.
        questions (list[str]): The list of questions for the homework.
        professor (str): The professor of the template.
        section (str): The section of the template.
    """

    def __init__(self, name: str, title: str, date: str, subject: str, questions: list[str], professor: str = None, section: str = None):
        super().__init__(name, title, date, subject, professor, section)
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
        professor (str): The professor of the template.
        section (str): The section of the template.
    """

    def __init__(self, name: str, title: str, date: str, subject: str, recipient: str, professor: str = None, section: str = None):
        super().__init__(name, title, date, subject, professor, section)
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
        professor (str): The professor of the template.
        section (str): The section of the template.
    """

    def __init__(self, name: str, title: str, date: str, subject: str, topic: str, professor: str = None, section: str = None):
        super().__init__(name, title, date, subject, professor, section)
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
        professor (str): The professor of the template.
        section (str): The section of the template.
    """

    def __init__(self, name: str, title: str, date: str, subject: str, problems: list[str], professor: str = None, section: str = None):
        super().__init__(name, title, date, subject)
        self.problems = problems


if __name__ == "__main__":
    TemplateModel("John Doe", "Math Homework", "July 06, 2024", "Mathematics", "Prof. Bill Joe", "Section 1").create_header("math_homework.docx")