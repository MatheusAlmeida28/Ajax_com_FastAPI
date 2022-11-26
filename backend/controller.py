from fastapi import FastAPI
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Pessoa, Tokens
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from hashlib import sha256


def conectaBanco():
    engine = create_engine("sqlite:///sqlite.db")
    Session = sessionmaker(bind=engine)
    session = Session()
    return session

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/cadastro")
def cadastro(user: str, email: str, senha: str):
    if len(senha) < 6:
        return {'erro': 'Senha muito pequena' }

    senha = sha256(senha.encode()).hexdigest()
    session = conectaBanco()
    usuario_user = session.query(Pessoa).filter_by(usuario=user).all()

    if len(usuario_user) > 0:
        return 'Usuario já cadastrado'

    usuario_email = session.query(Pessoa).filter_by(email=email).all()

    if len(usuario_email) > 0:
        return 'Usuario já cadastrado com esse email'


    try:
        novo_usuario = Pessoa(
            usuario = user,
            email = email,
            senha = senha
        )

        session.add(novo_usuario)
        session.commit()
        return 'Usuário cadastrado com sucesso!'
    except Exception as e:
        return {'erro': e}

if __name__ == "__main__":
    uvicorn.run('controller:app', port=5000, reload=True, access_log=False)
    
