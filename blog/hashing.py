from passlib.context import CryptContext

pwd_cxt= CryptContext(schemes=["bcrypt"], deprecated = "auto")

class Hash:
    def bcrypt(password:str):
        hpw= pwd_cxt.hash(password)
        return hpw
    def verify(hashed, plain):
        return pwd_cxt.verify(plain, hashed)