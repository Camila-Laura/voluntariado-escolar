from flask import Flask, request, jsonify, render_template, redirect, url_for, flash, session
from flask_login import login_required, logout_user, login_user
from flask import abort
from flask_cors import CORS
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Voluntario, Administrador, Solicitante, Atendimento
from flask_login import LoginManager

app = Flask(__name__)
CORS(app)

app.secret_key = "camila_1098765rt2893"
engine = create_engine("sqlite:///database.db")
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
db_session = Session()

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

# função para identificar se o admin está logado no sistema
@login_manager.user_loader
def load_user(user_id):
    return db_session.query(Administrador).get(int(user_id))

@app.route("/")
def home():
    admin_existente = db_session.query(Administrador).first() is not None
    return render_template("index.html", admin_existente=admin_existente)

@app.route("/login", methods=["POST"])
def login():
    dados = request.get_json() #pegar dados enviados pelo frontend
    email = dados.get("email")
    senha = dados.get("senha")

    admin = db_session.query(Administrador).filter_by(email=email).first()

    if admin and admin.senha == senha:
        login_user(admin)
        return jsonify({"sucesso": True})
    else:
        return jsonify({"erro": "E-mail ou senha inválidos"}), 401

# rotas web
@app.route('/sair')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))
    
@app.route("/admin")
@login_required
def painel_admin():
    return render_template("painel_admin.html")

@app.route("/admin/cadastro-voluntario")
def tela_cadastro_voluntario():
    return render_template("formulario_voluntario.html")

@app.route("/admin/formulario-admin")
def formulario_admin():
    return render_template("formulario_admin.html")

@app.route("/admin/formulario-solicitante")
def formulario_solicitante():
    return render_template("formulario_solicitante.html")

@app.route("/dados-voluntario")
def tabela_voluntario():
    return render_template("tabela_voluntario.html")

@app.route("/admin/dados-solicitante")
def tabela_solicitante():
    return render_template("tabela_solicitante.html")

@app.route("/admin/atendimentos")
def tabela_atendimentos():
    return render_template("tabela_atendimento.html")

#Rotas do Administrador
@app.route("/cadastro-administrador", methods=["POST"])
def criar_admin():
    if db_session.query(Administrador).first():
        return jsonify({"message": "Já existe um administrador cadastrado!"}), 400
    data = request.get_json() 

    admin = Administrador(
        nome=data["nome"],
        cargo=data["cargo"],
        email=data["email"],
        senha=data["senha"]
    )
    db_session.add(admin)
    db_session.commit()
    return jsonify({"message": "Administrador criado com sucesso!"})

# Rotas do Solicitante
@app.route("/solicitante", methods=["POST"])
def criar_solicitante():
    data = request.get_json()
    
    solicitante = Solicitante(
        nome=data["nome"],
        dificuldade=data["dificuldade"],
        horario_disponivel=data["horario_disponivel"],
        email=data["email"]
    )
    db_session.add(solicitante )
    db_session.commit()
    return jsonify({"message": "Solicitante criado com sucesso!"})

@app.route("/admin/solicitante", methods=["GET"])
def listar_solicitante():
    solicitante = db_session.query(Solicitante).all()

    return jsonify([
        {
            "id": s.id,
            "nome": s.nome,
            "dificuldade": s.dificuldade,
            "horario_disponivel": s.horario_disponivel,
            "email": s.email
        }
        for s in solicitante
    ])
    
@app.route("/admin/solicitante/<int:id>", methods=["PUT"])
def atualizar_dados_solicitante(id):
    s = db_session.query(Solicitante).get(id)
    if not s:
        return jsonify({"erro": "Solicitante não encontrado"}), 404
    data = request.get_json()
    s.nome = data.get("nome", s.nome)
    s.email = data.get("email", s.email)
    db_session.commit()
    return jsonify({"message": "Solicitante atualizado!"})

@app.route("/admin/solicitante/<int:id>", methods=["DELETE"])
def deletar_dados_solicitante(id):
    s = Session()
    u = s.query(Solicitante).get(id)
    s.delete(u)
    s.commit()
    return jsonify({"message": "Solicitante deletado!"})


#rotas do voluntario
@app.route("/voluntarios", methods=["POST"])
def add_voluntario():
    data = request.get_json()

    novo = Voluntario(
        nome=data["nome"],
        disponibilidade=data["disponibilidade"],
        tipo_apoio=data["tipo_apoio"],
        email=data["email"]
    )
    db_session.add(novo)
    db_session.commit()
    return jsonify({"message": "Voluntário criado com sucesso!"})

@app.route("/voluntarios", methods=["GET"])
def listar_voluntarios():
    voluntarios = db_session.query(Voluntario).all()

    return jsonify([
        {
            "id": v.id,
            "nome": v.nome,
            "disponibilidade": v.disponibilidade,
            "tipo_apoio": v.tipo_apoio,
            "email": v.email
        }
        for v in voluntarios
    ])

@app.route("/voluntarios/<int:id>", methods=["GET"])
def buscar_voluntario(id):
    v = db_session.query(Voluntario).get(id)

    if not v:
        return jsonify({"erro": "Não encontrado"}), 404

    return jsonify({
        "id": v.id,
        "nome": v.nome,
        "disponibilidade": v.disponibilidade,
        "tipo_apoio": v.tipo_apoio,
        "email": v.email
    })

@app.route("/admin/voluntarios/<int:id>", methods=["PUT"])
def atualizar_dados_voluntario(id):
    u = db_session.query(Voluntario).get(id)

    if not u:
        return jsonify({"erro": "Voluntário não encontrado"}), 404
    data = request.get_json()

    u.nome = data.get("nome", u.nome)
    u.email = data.get("email", u.email)

    db_session.commit()
    return jsonify({"message": "Voluntario atualizado!"})

@app.route("/admin/voluntarios/<int:id>", methods=["DELETE"])
def deletar_dados_voluntario(id):
    u = db_session.query(Voluntario).get(id)
    if not u:
        return jsonify({"erro": "Voluntário não encontrado"}), 404
    db_session.delete(u)
    db_session.commit()
    return jsonify({"message": "Voluntario deletado!"})

@app.route("/api/atendimentos", methods=["GET"])
def listar_atendimentos():
    atendimentos = db_session.query(Atendimento).all()

    lista = []
    for a in atendimentos:
        lista.append({
            "id": a.id,
            "voluntario_id": a.voluntario_id,
            "voluntario_nome": a.voluntario.nome if a.voluntario else None,
            "solicitante_id": a.solicitante_id,
            "solicitante_nome": a.solicitante.nome if a.solicitante else None
        })
    return jsonify(lista)

# Rotas de atendimento
@app.route("/api/atendimentos", methods=["POST"])
def criar_atendimento():
    data = request.get_json()
    atendimento = Atendimento(
        voluntario_id=data["voluntario_id"],
        solicitante_id=data["solicitante_id"]
    )
    db_session.add(atendimento)
    db_session.commit()
    return jsonify({"message": "Atendimento criado com sucesso!"})

@app.route("/api/atendimentos/<int:id>", methods=["DELETE"])
def deletar_atendimento(id):
    a = db_session.query(Atendimento).get(id)
    if not a:
        return jsonify({"erro": "Atendimento não encontrado"}), 404
    db_session.delete(a)
    db_session.commit()
    return jsonify({"message": "Atendimento deletado!"})

if __name__ == "__main__":
    app.run(debug=True)