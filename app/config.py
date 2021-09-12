from pydantic import BaseSettings


class MyBaseSettings(BaseSettings):
    def __hash__(self):
        return hash((type(self),) + tuple(self.__dict__.values()))


class Settings(MyBaseSettings):
    app_name: str = "v8i-service"
    app_host: str = "http://127.0.0.1:8000"
    v8i_folder: str = "tests/files"
