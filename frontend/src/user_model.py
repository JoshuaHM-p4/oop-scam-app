class UserModel:
    def __init__(self, user_id: int = 0, username: str = '', email: str = '', access_token: str = ''):
        self.__user_id = user_id
        self.__username = username
        self.__email = email
        self.__access_token = access_token

    # Getters
    @property
    def user_id(self) -> int:
        return self.__user_id

    @user_id.setter
    def user_id(self, user_id: int) -> None:
        self.__user_id = user_id

    @property
    def username(self) -> str:
        return self.__username

    @username.setter
    def username(self, username: str) -> None:
        self.__username = username

    @property
    def email(self) -> str:
        return self.__email

    @email.setter
    def email(self, email: str) -> None:
        self.__email = email

    @property
    def access_token(self) -> str:
        return self.__access_token

    @access_token.setter
    def access_token(self, access_token: str) -> None:
        self.__access_token = access_token

    # From JSON
    @classmethod
    def from_json(cls, data: dict):
        return cls(
            user_id=data['user_id'],
            username=data['username'],
            email=data['email'],
            access_token=data['access_token']
        )