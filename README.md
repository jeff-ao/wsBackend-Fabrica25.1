# Star Wars Translate API

## Sobre o Projeto

A **Star Wars Translate API** é uma API REST desenvolvida com **Django Rest Framework**, que permite traduzir textos escritos em inglês para diferentes línguas fictícias do universo Star Wars.

### Idiomas Disponíveis:

- **Cheunh**
- **Gungan**
- **Huttese**
- **Mandalorian**
- **Sith**
- **Yoda**

## Tecnologias Utilizadas

- **Linguagem**: Python 3.13
- **Framework**: Django 5.1.6 + Django REST Framework
- **Banco de Dados**: SQLite (padrão)
- **Autenticação**: Email e senha (hash de senha utilizando Django's `make_password`)
- **Containers**: Docker + Docker Compose
- **Tradução**: API externa `funtranslations.com`

## Como Executar o Projeto

### Requisitos

- **Docker** e **Docker compose** instalados

### Passos

1. Clone o repositório:

   ```sh
   https://github.com/jeff-ao/wsBackend-Fabrica25.1.git
   ```

   entre no diretório

2. Construa e inicie os containers Docker:

   ```sh
   docker-compose build -d
   docker ps
   ```

   Vai aparecer algo assim:

   ```sh
   CONTAINER ID   IMAGE               COMMAND                  CREATED              STATUS              PORTS                    NAMES
   xxxxxxxxxxxx   starwarstranslate   "python manage.py ru…"   About a minute ago   Up About a minute   0.0.0.0:8000->8000/tcp   NOME-DO-CONTAINER

   docker exec -it NOME-DO-CONATINER bash

   root@xxxxxxxxxxxx:/starWarsTranslate# python manage.py migrate
   ```

3. A API estará rodando em: `http://localhost:8000/api/`

4. Para testar as requisições, use ferramentas como **Postman** ou **cURL**.

## Endpoints da API

### 1. Usuários

#### Criar um novo usuário

- **Rota**: `POST /api/users/`
- **Validações**:
  - `name` (obrigatório, string, max 255 caracteres)
  - `email` (obrigatório, string, único, max 255 caracteres)
  - `password` (obrigatório, min 8 caracteres, deve conter 3 números, uma maiúscula e um caractere especial)
- **Exemplo de Request:**
  ```json
  {
    "name": "Luke Skywalker",
    "email": "luke@jedi.com",
    "password": "Jedi123!"
  }
  ```
- **Resposta de Sucesso (201)**:
  ```json
  {
    "name": "Luke Skywalker",
    "email": "luke@jedi.com",
    "createdAt": "2025-03-01T12:00:00Z",
    "updatedAt": "2025-03-01T12:00:00Z"
  }
  ```

#### Login do usuário

- **Rota**: `POST /api/users/login/`
- **Exemplo de Request:**
  ```json
  {
    "email": "luke@jedi.com",
    "password": "Jedi123!"
  }
  ```
- **Resposta de Sucesso (200):**
  ```json
  {
    "message": "Login bem-sucedido",
    "user_id": 1
  }
  ```

### 2. Traduções

#### Criar uma nova tradução

- **Rota**: `POST /api/translates/`
- **Validações**:
  - `language` (obrigatório, uma das opções: `yoda`, `sith`, `mandalorian`, `huttese`, `gungan`, `cheunh`)
  - `text` (obrigatório, string, max 1000 caracteres)
  - `user_id` (obrigatório, int, deve existir no banco de dados)
- **Exemplo de Request:**
  ```json
  {
    "language": "yoda",
    "text": "I am a Jedi like my father before me",
    "user_id": 1
  }
  ```
- **Resposta de Sucesso (201):**
  ```json
  {
    "id": 1,
    "language": "yoda",
    "text": "I am a Jedi like my father before me",
    "translatedText": "A Jedi like my father before me, I am",
    "user_id": 1,
    "createdAt": "2025-03-01T12:05:00Z",
    "updatedAt": "2025-03-01T12:05:00Z"
  }
  ```

#### Buscar todas as traduções

- **Rota**: `GET /api/translates/`

#### Buscar uma tradução por ID

- **Rota**: `GET /api/translates/{id}/`

#### Atualizar uma tradução

- **Rota**: `PUT /api/translates/{id}/`

#### Deletar uma tradução

- **Rota**: `DELETE /api/translates/{id}/?user_id={user_id}`

## Decisão de Uso de ID Incremental

Nesta API, os identificadores (âncora primária) das entidades **Users** e **Translates** são IDs incrementais (inteiros sequenciais) ao invés de UUIDs.

Essa escolha foi feita por questão de **eficiência**, pois consultas em bancos relacionais são mais rápidas quando usam IDs inteiros ao invés de UUIDs, melhorando o desempenho das queries.

## Contato

Caso tenha dúvidas ou sugestões, entre em contato com o desenvolvedor pelo email: **jeffsonluiz11@gmail.com**.

---

Isso é tudo, jovem Padawan! Que a força esteja com você. ✨
