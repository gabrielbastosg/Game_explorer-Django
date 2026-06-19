# 🎮 Games Explorer

Aplicação web em **Django** que consome a **[API RAWG](https://rawg.io/)** para explorar videogames: listar, buscar, ver detalhes, favoritar e organizar uma **estante pessoal** por status de jogo (Quero jogar / Jogando / Zerei).

Interface em **pt-BR**, tema escuro com acentos roxo/azul.

---

## ✨ Funcionalidades

- 🔎 **Listagem e busca** de jogos em tempo real via API RAWG
- 🕹️ **Página de detalhe** com imagem, nota, data de lançamento, gêneros e descrição
- 👤 **Cadastro e login** de usuários (autenticação nativa do Django)
- ❤️ **Favoritos** por usuário
- 📚 **Minha Estante** — marque cada jogo como **Quero jogar**, **Jogando** ou **Zerei** e veja-os agrupados por status
- 🎨 Tema escuro responsivo, com CSS organizado por página

---

## 🛠️ Tecnologias

- **Python** + **Django 5.2**
- **SQLite** (banco padrão de desenvolvimento)
- **requests** — chamadas HTTP à API RAWG
- **python-decouple** — variáveis de ambiente (`.env`)
- HTML + CSS (sem framework front-end)

---

## 🚀 Como rodar localmente

### 1. Clone o repositório

```bash
git clone https://github.com/gabrielbastosg/games-explorer-django.git
cd games-explorer-django
```

### 2. Crie e ative um ambiente virtual

```bash
python -m venv .venv
.venv\Scripts\activate        # Windows
# source .venv/bin/activate   # Linux/macOS
```

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

### 4. Configure a chave da API

Crie um arquivo `.env` na raiz (use o `.env.example` como modelo) com a sua chave da RAWG:

```
RAWG_API_KEY=sua_chave_aqui
```

> A chave gratuita pode ser obtida em [rawg.io/apidocs](https://rawg.io/apidocs).

### 5. Aplique as migrações e rode o servidor

```bash
python manage.py migrate
python manage.py runserver
```

Acesse **http://127.0.0.1:8000/** 🎉

---

## 📂 Estrutura

```
games_explorer/
├── config/          # configurações do projeto Django
├── games/           # app principal (views, models, urls, templates, static)
│   ├── models.py    # FavoriteGame e GameStatus
│   ├── views.py     # home, busca, detalhe, favoritos, estante
│   └── templates/
├── manage.py
└── requirements.txt
```

---

## 📌 Créditos

Dados de jogos fornecidos por **[RAWG](https://rawg.io/)**.

---

Projeto desenvolvido por **Gabriel Bastos** como estudo de Django + consumo de APIs. 🚀
