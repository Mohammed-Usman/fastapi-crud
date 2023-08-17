from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash(password: str):
    return pwd_context.hash(password)


def verify(password, hashed_passowrd):
    return pwd_context.verify(password, hashed_passowrd)

# pm.environment.set("JWT", pm.response.json().access_token);
