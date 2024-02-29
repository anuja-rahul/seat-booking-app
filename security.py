
import hashlib
from python_datalogger import DataLogger


class SecurityHandler:
    def __init__(self, password: str):
        self.__password = password

    @DataLogger.logger
    def get_hashed_password(self) -> str:
        return hashlib.sha256(self.__password.encode()).hexdigest()

    @DataLogger.logger
    def check_password_hashes(self, password_hash: str = None) -> bool:
        if self.get_hashed_password() == password_hash:
            return True
        else:
            return False
