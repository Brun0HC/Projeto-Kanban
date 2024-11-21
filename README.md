# Projeto Kanban

#### Este é um projeto Kanban para a disciplina de Projetos. Siga as instruções abaixo para configurar e executar o projeto.

## Pré-requisitos:
- Python 3.8 ou superior instalado
- pip para gerenciar pacotes Python
- virtualenv para criar ambientes virtuais

### Passos para Configuração e Execução:

### 1. Clone o repositório, crie um ambiente virtual, ative-o e instale as dependências:
   ```bash 
   git clone https://github.com/Brun0HC/Projeto-Kanban.git
   cd Projeto-Kanban
   python -m venv venv
   source venv/bin/activate  # No Windows, use: venv\Scripts\activate
   pip install -r requirements.txt
   ``` 

### 2. Entre na pasta do aplicativo, aplique as migrações e crie um superusuário:
   ```bash
   cd app
   python manage.py makemigrations
   python manage.py migrate
   python manage.py createsuperuser  # Use admin/admin para facilitar o login inicial
   ```
### 3 . Configure a variável de e-mail no arquivo `.env`:
   - Dentro da pasta `/app`, crie o arquivo `.env`.
   - Adicione a variável: EMAIL_USER=<seu_email>

### 4. Inicie o servidor:
   ```bash
   python manage.py runserver
   ```

### 5. Acesse o Django Admin:
   - Abra o navegador em: http://localhost:8000/admin
   - Faça login com o superusuário criado no passo anterior.

### 6. No Django Admin, adicione um membro:
   - Navegue até a seção "Membros".
   - Adicione um novo membro com um endereço de e-mail criado no passo 3.
