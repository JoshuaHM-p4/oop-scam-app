class NotebookModel: 
    """ 
    Contains the data model for a notebook. 
    """

    def __init__(self, id, owner_id, title): 
        """ 
        
        """
        self.id = id
        self.owner_id = owner_id
        self.title = title 
        self.notes = []
    
    def get_pages(self) -> int: 
        """
        Returns the number of pages in the notebook.
        """
        return len(self.notes)  
    
    def change_title(self, new_title: str): 
        """
        Changes the title of the notebook.
        """
        self.title = new_title

class NoteModel:
    """
    Contains the data model for a note.
    """

    def __init__(self, id, notebook_id, title, content):
        """
        Initializes a new instance of the NoteModel class.

        Args:
            title (str): The title of the note.
            content (str): The content of the note.
        """
        self.id = id
        self.notebook_id = notebook_id
        self.title = title
        self.content = content

        