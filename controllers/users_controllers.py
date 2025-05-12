import bcrypt
from db.supabase import SessionLocal
from models.user_models import User


def get_password_hash(password):
    # hashpw() hashes une string et génère un stal hash alétoire
    return bcrypt.hashpw(
        password.encode("utf-8"),
        bcrypt.gensalt(),
        # on stocke le hash comme string
        ).decode("utf-8")


def verify_password(plain_password, hashed_password):
    # checkpw() compare le password en string en clair avec le password hashé en db
    return bcrypt.checkpw(
        plain_password.encode("utf-8"),
        # on convertit le hash stocké en bytes
        hashed_password.encode("utf-8")
        )


def get_user(username:str):
    with SessionLocal() as db:
        print("🟡 GET USER:", db.query(User).filter(User.name == username).first())
        return db.query(User).filter(User.name == username).first()


def authenticate_user(username: str, password:str):
    with SessionLocal() as db:
        user = get_user(username)  
        print(f"🟣 AUTHENTICATE USER: {user}")
        if not user:
            return False
        if not verify_password(password, user.password):
            return False
        return user 