class Settings:
    """A class with settings that allow the user to 
    alter the behavior of the program 
    """
    def __init__(self) -> None:
        self.PORT: int  = 8080
        self.HOST: str  = "localhost"
        self.DB_FILENAME: str = "./data/database.xml"
