from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flasgger import Swagger

app = Flask(__name__)

# Configuração do SQLite
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///escola.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Inicialização do Swagger
swagger = Swagger(app)

# Modelo de Aluno
class Aluno(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    idade = db.Column(db.Integer, nullable=False)
    nota_primeiro_semestre = db.Column(db.Float, nullable=False)
    nota_segundo_semestre = db.Column(db.Float, nullable=False)
    nome_professor = db.Column(db.String(100), nullable=False)
    numero_sala = db.Column(db.String(20), nullable=False)

# Cria o banco de dados
with app.app_context():
    db.create_all()

# Rotas do CRUD

@app.route('/')
def index():
    return "Bem-vindo à API de Alunos!"

@app.route('/alunos', methods=['POST'])
def criar_aluno():
    """
    Criar um novo aluno
    ---
    tags:
      - Alunos
    parameters:
      - name: aluno
        in: body
        required: true
        schema:
          type: object
          properties:
            nome:
              type: string
              example: João da Silva
            idade:
              type: integer
              example: 20
            nota_primeiro_semestre:
              type: number
              format: float
              example: 8.5
            nota_segundo_semestre:
              type: number
              format: float
              example: 7.0
            nome_professor:
              type: string
              example: Prof. Ana
            numero_sala:
              type: string
              example: Sala 101
    responses:
      201:
        description: Aluno criado com sucesso
      400:
        description: Dados inválidos
    """
    dados = request.get_json()
    novo_aluno = Aluno(
        nome=dados['nome'],
        idade=dados['idade'],
        nota_primeiro_semestre=dados['nota_primeiro_semestre'],
        nota_segundo_semestre=dados['nota_segundo_semestre'],
        nome_professor=dados['nome_professor'],
        numero_sala=dados['numero_sala']
    )
    db.session.add(novo_aluno)
    db.session.commit()
    return jsonify({'mensagem': 'Aluno criado com sucesso!'}), 201

@app.route('/alunos', methods=['GET'])
def obter_alunos():
    """
    Obter todos os alunos
    ---
    tags:
      - Alunos
    responses:
      200:
        description: Lista de alunos
        schema:
          type: array
          items:
            type: object
            properties:
              id:
                type: integer
              nome:
                type: string
              idade:
                type: integer
              nota_primeiro_semestre:
                type: number
                format: float
              nota_segundo_semestre:
                type: number
                format: float
              nome_professor:
                type: string
              numero_sala:
                type: string
    """
    alunos = Aluno.query.all()
    return jsonify([{
        'id': aluno.id,
        'nome': aluno.nome,
        'idade': aluno.idade,
        'nota_primeiro_semestre': aluno.nota_primeiro_semestre,
        'nota_segundo_semestre': aluno.nota_segundo_semestre,
        'nome_professor': aluno.nome_professor,
        'numero_sala': aluno.numero_sala
    } for aluno in alunos])

@app.route('/alunos/<int:id>', methods=['GET'])
def obter_aluno(id):
    """
    Obter um aluno específico
    ---
    tags:
      - Alunos
    parameters:
      - name: id
        in: path
        type: integer
        required: true
    responses:
      200:
        description: Aluno encontrado
        schema:
          type: object
          properties:
            id:
              type: integer
            nome:
              type: string
            idade:
              type: integer
            nota_primeiro_semestre:
              type: number
              format: float
            nota_segundo_semestre:
              type: number
              format: float
            nome_professor:
              type: string
            numero_sala:
              type: string
      404:
        description: Aluno não encontrado
    """
    aluno = Aluno.query.get_or_404(id)
    return jsonify({
        'id': aluno.id,
        'nome': aluno.nome,
        'idade': aluno.idade,
        'nota_primeiro_semestre': aluno.nota_primeiro_semestre,
        'nota_segundo_semestre': aluno.nota_segundo_semestre,
        'nome_professor': aluno.nome_professor,
        'numero_sala': aluno.numero_sala
    })

@app.route('/alunos/<int:id>', methods=['PUT'])
def atualizar_aluno(id):
    """
    Atualizar um aluno
    ---
    tags:
      - Alunos
    parameters:
      - name: id
        in: path
        type: integer
        required: true
      - name: aluno
        in: body
        required: true
        schema:
          type: object
          properties:
            nome:
              type: string
            idade:
              type: integer
            nota_primeiro_semestre:
              type: number
              format: float
            nota_segundo_semestre:
              type: number
              format: float
            nome_professor:
              type: string
            numero_sala:
              type: string
    responses:
      200:
        description: Aluno atualizado com sucesso
      400:
        description: Dados inválidos
      404:
        description: Aluno não encontrado
    """
    aluno = Aluno.query.get_or_404(id)
    dados = request.get_json()
    aluno.nome = dados['nome']
    aluno.idade = dados['idade']
    aluno.nota_primeiro_semestre = dados['nota_primeiro_semestre']
    aluno.nota_segundo_semestre = dados['nota_segundo_semestre']
    aluno.nome_professor = dados['nome_professor']
    aluno.numero_sala = dados['numero_sala']
    db.session.commit()
    return jsonify({'mensagem': 'Aluno atualizado com sucesso!'})

@app.route('/alunos/<int:id>', methods=['DELETE'])
def deletar_aluno(id):
    """
    Deletar um aluno
    ---
    tags:
      - Alunos
    parameters:
      - name: id
        in: path
        type: integer
        required: true
    responses:
      200:
        description: Aluno deletado com sucesso
      404:
        description: Aluno não encontrado
    """
    aluno = Aluno.query.get_or_404(id)
    db.session.delete(aluno)
    db.session.commit()
    return jsonify({'mensagem': 'Aluno deletado com sucesso!'})

if __name__ == '__main__':
    app.run(debug=True)
