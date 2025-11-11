# Cadastro-de-Funcionários
Sistema de gerenciamento de funcionários (CRUD), construído com Python (FastAPI) e Jinja2.

# 🚀 Sistema de Cadastro de Funcionários

Um sistema web completo para Gerenciamento de Funcionários (CRUD) com importação em massa via Excel. Construído com Python, FastAPI, SQLAlchemy e Jinja2.

<img width="1920" height="925" alt="Capturar 555" src="https://github.com/user-attachments/assets/babb50de-7df7-4de7-82bc-4aee8c8955be" />


---

## ✨ Funcionalidades

* **CRUD Completo:** Crie, visualize, edite e exclua registros de funcionários.
* **Listagem e Detalhes:** Visualize todos os funcionários em uma tabela paginada e clique para ver detalhes.
* **Importação em Massa:** Cadastre centenas de funcionários de uma vez enviando um arquivo `.xlsx`.
* **Interface Moderna:** Front-end limpo e responsivo construído com templates Jinja2, CSS moderno e JavaScript.
* **Banco de Dados Leve:** Utiliza SQLite, que não requer instalação de servidor (um único arquivo `test.db`).

---

## 🛠️ Tecnologias Utilizadas

* **Backend:** [Python 3](https://www.python.org/)
* **Framework Web:** [FastAPI](https://fastapi.tiangolo.com/)
* **Servidor ASGI:** [Uvicorn](https://www.uvicorn.org/)
* **Banco de Dados (ORM):** [SQLAlchemy](https://www.sqlalchemy.org/)
* **Banco de Dados (Driver):** [SQLite](https://www.sqlite.org/index.html)
* **Templates (Frontend):** [Jinja2](https://jinja.palletsprojects.com/en/3.1.x/)
* **Manipulação de Excel:** [openpyxl](https://openpyxl.readthedocs.io/en/stable/)
* **Formulários:** [python-multipart](https://pypi.org/project/python-multipart/)

---

## 🏁 Como Executar o Projeto

Siga os passos abaixo para rodar o projeto em sua máquina local.

### 1. Pré-requisitos

* [Python 3.10+](https://www.python.org/downloads/)
* [Git](https://git-scm.com/downloads) (opcional, para clonar)

### 2. Instalação

**1. Clone o repositório:**
```bash
git clone [https://github.com/claudiojrrodrigues04/Cadastro-de-Funcionarios.git](https://github.com/claudiojrrodrigues04/Cadastro-de-Funcionarios.git)
cd Cadastro-de-Funcionarios
```

**2. (Opcional) Crie um Ambiente Virtual (Virtual Environment):**
```bash
# Windows
python -m venv venv
.\venv\Scripts\activate
```

**3. Instale as dependências:**
O arquivo `requirements.txt` contém todas as bibliotecas que o projeto precisa.
```bash
pip install -r requirements.txt
```

**4. Execute o servidor:**
O `uvicorn` irá iniciar o servidor. O `--reload` faz com que o servidor reinicie automaticamente se você alterar um arquivo.
```bash
uvicorn main:app --reload --port 8000
```

**5. Acesse no navegador:**
Abra seu navegador e acesse:
[**http://127.0.0.1:8000**](http://127.0.0.1:8000)
