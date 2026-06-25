"""
BANCO DE DADOS - SCHEMA DO SISTEMA DE GESTÃO DE ESCOLA
Cria todas as tabelas necessárias para o sistema funcionar
"""

import sqlite3
import hashlib
import secrets
from binascii import hexlify
from pathlib import Path
from datetime import datetime, date

DB_PATH = Path(__file__).resolve().parent / 'escola.db'

def hash_senha(senha):
    salt = secrets.token_hex(32)
    hash_obj = hashlib.pbkdf2_hmac(
        'sha256',
        senha.encode('utf-8'),
        salt.encode('utf-8'),
        100000
    )
    return f"{salt}${hexlify(hash_obj).decode()}"

def criar_banco_dados():
    """Cria o banco de dados e todas as tabelas"""
    
    conexao = sqlite3.connect(DB_PATH)
    cursor = conexao.cursor()
    
    # ========== TABELA DE SETORES ==========
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS setores (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL UNIQUE,
        descricao TEXT,
        data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    
    # ========== TABELA DE FUNCIONÁRIOS ==========
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS funcionarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        email TEXT NOT NULL UNIQUE,
        cpf TEXT NOT NULL UNIQUE,
        senha TEXT NOT NULL,
        cargo TEXT NOT NULL,
        setor_id INTEGER,
        salario REAL,
        data_admissao DATE,
        ativo INTEGER DEFAULT 1,
        data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (setor_id) REFERENCES setores(id)
    )
    ''')
    
    # ========== TABELA DE PROFESSORES ==========
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS professores (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        email TEXT NOT NULL UNIQUE,
        cpf TEXT NOT NULL UNIQUE,
        senha TEXT NOT NULL,
        matricula TEXT NOT NULL UNIQUE,
        formacao TEXT,
        especialidade TEXT,
        ativo INTEGER DEFAULT 1,
        data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    
    # ========== TABELA DE CURSOS ==========
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS cursos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        descricao TEXT,
        duracao_meses INTEGER,
        valor REAL,
        ativo INTEGER DEFAULT 1,
        data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    
    # ========== TABELA DE MÓDULOS ==========
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS modulos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        curso_id INTEGER NOT NULL,
        nome TEXT NOT NULL,
        descricao TEXT,
        carga_horaria INTEGER,
        ordem INTEGER,
        data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (curso_id) REFERENCES cursos(id)
    )
    ''')
    
    # ========== TABELA DE TURMAS ==========
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS turmas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        codigo TEXT NOT NULL UNIQUE,
        nome TEXT NOT NULL,
        curso_id INTEGER NOT NULL,
        professor_id INTEGER NOT NULL,
        semestre TEXT,
        data_inicio DATE,
        data_fim DATE,
        horario TEXT,
        sala TEXT,
        capacidade INTEGER,
        ativa INTEGER DEFAULT 1,
        data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (curso_id) REFERENCES cursos(id),
        FOREIGN KEY (professor_id) REFERENCES professores(id)
    )
    ''')
    
    # ========== TABELA DE ALUNOS ==========
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS alunos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        email TEXT NOT NULL UNIQUE,
        cpf TEXT NOT NULL UNIQUE,
        senha TEXT NOT NULL,
        matricula TEXT NOT NULL UNIQUE,
        data_nascimento DATE,
        telefone TEXT,
        endereco TEXT,
        cidade TEXT,
        estado TEXT,
        ativo INTEGER DEFAULT 1,
        data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    
    # ========== TABELA DE MATRÍCULAS ==========
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS matriculas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        aluno_id INTEGER NOT NULL,
        turma_id INTEGER NOT NULL,
        data_matricula DATE,
        status TEXT DEFAULT 'ativa',
        data_conclusao DATE,
        data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (aluno_id) REFERENCES alunos(id),
        FOREIGN KEY (turma_id) REFERENCES turmas(id),
        UNIQUE(aluno_id, turma_id)
    )
    ''')
    
    # ========== TABELA DE FREQUÊNCIA ==========
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS frequencias (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        matricula_id INTEGER NOT NULL,
        data_aula DATE,
        presente INTEGER,
        justificativa TEXT,
        data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (matricula_id) REFERENCES matriculas(id)
    )
    ''')
    
    # ========== TABELA DE NOTAS ==========
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS notas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        matricula_id INTEGER NOT NULL,
        modulo_id INTEGER NOT NULL,
        primeira_nota REAL,
        segunda_nota REAL,
        terceira_nota REAL,
        media_final REAL,
        data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (matricula_id) REFERENCES matriculas(id),
        FOREIGN KEY (modulo_id) REFERENCES modulos(id)
    )
    ''')
    
    # ========== TABELA DE OBSERVAÇÕES PEDAGÓGICAS ==========
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS observacoes_pedagogicas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        matricula_id INTEGER NOT NULL,
        professor_id INTEGER NOT NULL,
        texto TEXT,
        data_observacao DATE,
        data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (matricula_id) REFERENCES matriculas(id),
        FOREIGN KEY (professor_id) REFERENCES professores(id)
    )
    ''')
    
    # ========== TABELA DE MATERIAL DIDÁTICO ==========
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS materiais (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        modulo_id INTEGER NOT NULL,
        nome TEXT NOT NULL,
        descricao TEXT,
        tipo TEXT,
        arquivo TEXT,
        data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (modulo_id) REFERENCES modulos(id)
    )
    ''')
    
    # ========== TABELA DE FINANCEIRO ==========
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS financeiro (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        matricula_id INTEGER NOT NULL,
        valor_total REAL,
        valor_pago REAL DEFAULT 0,
        data_vencimento DATE,
        status TEXT DEFAULT 'pendente',
        parcelas INTEGER,
        descricao TEXT,
        data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (matricula_id) REFERENCES matriculas(id)
    )
    ''')
    
    # ========== TABELA DE PAGAMENTOS ==========
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS pagamentos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        financeiro_id INTEGER NOT NULL,
        valor REAL,
        data_pagamento DATE,
        metodo_pagamento TEXT,
        observacao TEXT,
        data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (financeiro_id) REFERENCES financeiro(id)
    )
    ''')
    
    # ========== TABELA DE CONTROLE COMERCIAL ==========
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS controle_comercial (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        turma_id INTEGER NOT NULL,
        total_vagas INTEGER,
        vagas_preenchidas INTEGER,
        vagas_disponiveis INTEGER,
        valor_aula REAL,
        descontos_aplicados TEXT,
        faturamento_previsto REAL,
        faturamento_realizado REAL,
        mes_ano TEXT,
        data_atualizacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (turma_id) REFERENCES turmas(id)
    )
    ''')
    
    # ========== TABELA DE USUÁRIOS (Para login) ==========
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS usuarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        email TEXT NOT NULL UNIQUE,
        senha TEXT NOT NULL,
        tipo_usuario TEXT NOT NULL,
        tabela_referencia TEXT,
        id_referencia INTEGER,
        ativo INTEGER DEFAULT 1,
        data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')

    # ========== TABELAS USADAS PELO APP v2 ==========
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS status_aluno (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        aluno_id INTEGER NOT NULL,
        status TEXT NOT NULL,
        motivo TEXT,
        data_atualizacao DATE,
        data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (aluno_id) REFERENCES alunos(id)
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS relatorios_aluno (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        aluno_id INTEGER NOT NULL,
        tipo TEXT,
        titulo TEXT,
        conteudo TEXT,
        criado_por INTEGER,
        data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (aluno_id) REFERENCES alunos(id)
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS anexos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        aluno_id INTEGER NOT NULL,
        tipo TEXT,
        titulo TEXT,
        arquivo TEXT,
        arquivo_nome TEXT,
        arquivo_tamanho INTEGER,
        arquivo_tipo TEXT,
        data_upload TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (aluno_id) REFERENCES alunos(id)
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS audit_log (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        usuario_id INTEGER,
        usuario_tipo TEXT,
        acao TEXT,
        tabela_afetada TEXT,
        id_registro INTEGER,
        valores_antigos TEXT,
        valores_novos TEXT,
        data_acao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS parcelas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        financeiro_id INTEGER NOT NULL,
        numero_parcela INTEGER,
        valor_parcela REAL,
        data_vencimento DATE,
        data_pagamento DATE,
        status TEXT DEFAULT 'pendente',
        metodo_pagamento TEXT,
        observacao TEXT,
        data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (financeiro_id) REFERENCES financeiro(id)
    )
    ''')

    # Dados minimos para o primeiro acesso e para o dashboard abrir sem erro.
    cursor.executemany('''
    INSERT OR IGNORE INTO setores (id, nome, descricao) VALUES (?, ?, ?)
    ''', [
        (1, 'Administrativo', 'Setor administrativo da escola'),
        (2, 'Pedagogico', 'Setor responsavel pelo ensino'),
        (3, 'Financeiro', 'Setor de financas'),
        (4, 'Comercial', 'Setor de vendas e matriculas'),
    ])

    cursor.execute('''
    INSERT OR IGNORE INTO funcionarios (id, nome, email, cpf, senha, cargo, setor_id, salario)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (1, 'Administrador', 'admin@escola.com', '00000000000',
          hash_senha('Mudar@123'), 'Administrador', 1, 0))

    cursor.execute('''
    INSERT OR IGNORE INTO usuarios (email, senha, tipo_usuario, tabela_referencia, id_referencia)
    VALUES (?, ?, ?, ?, ?)
    ''', ('admin@escola.com', hash_senha('Mudar@123'), 'admin', 'funcionarios', 1))

    cursor.execute('''
    INSERT OR IGNORE INTO professores (id, nome, email, cpf, senha, matricula, formacao, especialidade)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (1, 'Ana Silva', 'ana@escola.com', '12345678901',
          hash_senha('Prof@123'), 'PROF001', 'Licenciatura', 'Matematica'))

    cursor.execute('''
    INSERT OR IGNORE INTO usuarios (email, senha, tipo_usuario, tabela_referencia, id_referencia)
    VALUES (?, ?, ?, ?, ?)
    ''', ('ana@escola.com', hash_senha('Prof@123'), 'professor', 'professores', 1))

    cursor.execute('''
    INSERT OR IGNORE INTO cursos (id, nome, descricao, duracao_meses, valor)
    VALUES (?, ?, ?, ?, ?)
    ''', (1, 'Matematica Basica', 'Curso inicial de matematica', 2, 500))

    cursor.execute('''
    INSERT OR IGNORE INTO turmas (id, codigo, nome, curso_id, professor_id, semestre, data_inicio, data_fim, horario, sala, capacidade)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (1, 'TUR001', 'Turma A - Matematica', 1, 1, '2026.1',
          date.today(), date.today(), '19:00-21:00', 'Sala 101', 30))

    cursor.execute('''
    INSERT OR IGNORE INTO alunos (id, nome, email, cpf, senha, matricula, data_nascimento, telefone)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (1, 'Joao Silva', 'joao@escola.com', '11111111111',
          hash_senha('Aluno@123'), 'ALN001', '2000-01-01', '(11) 98765-4321'))

    cursor.execute('''
    INSERT OR IGNORE INTO usuarios (email, senha, tipo_usuario, tabela_referencia, id_referencia)
    VALUES (?, ?, ?, ?, ?)
    ''', ('joao@escola.com', hash_senha('Aluno@123'), 'aluno', 'alunos', 1))

    cursor.execute('''
    INSERT INTO status_aluno (aluno_id, status, data_atualizacao)
    SELECT ?, ?, ?
    WHERE NOT EXISTS (SELECT 1 FROM status_aluno WHERE aluno_id = ?)
    ''', (1, 'Frequente', date.today(), 1))
    
    conexao.commit()
    conexao.close()
    print("[OK] Banco de dados criado com sucesso!")

if __name__ == "__main__":
    criar_banco_dados()
