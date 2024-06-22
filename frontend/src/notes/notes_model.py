class NoteModel:
    """
    Contains the data model for a note.
    """

    def __init__(self, id, title, content):
        """
        Initializes a new instance of the NoteModel class.

        Args:
            title (str): The title of the note.
            content (str): The content of the note.
        """
        self.id = id
        self.title = title
        self.content = content