from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

DOTENV_PATH = Path(__file__).resolve().parents[1]/".env"

class Settings(BaseSettings):
    db_name: str #env 파일의 DB_NAME항목과 매핑되도록 같은 이름으로 설정
    db_user: str
    db_pwd: str
    db_host: str
    model_config = SettingsConfigDict(env_file=DOTENV_PATH, env_file_encoding="utf-8")
    
    @property
    def database_url(self) ->str:
        return(
            f"mysql+aiomysql://{self.db_user}:{self.db_pwd}"
            f"@{self.db_host}:3306/{self.db_name}"
        )
settings = Settings() # 이때 .env 파일을 읽어서 설정값을 르드한다.
#SettingsConfigDict 에서 case_sensitive=True 로 설정하면 키 이름의 대/소문자가
#정확히 일치해야한ㄷ. 예0. db_name과 DB_NAME 을 다른 키로 취급된 

        