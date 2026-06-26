# 🎮 Games Explorer

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat&logo=python&logoColor=white)
![Django](https://img.shields.io/badge/Django-5-092E20?style=flat&logo=django&logoColor=white)
![API](https://img.shields.io/badge/API-RAWG-EF233C?style=flat)
![Status](https://img.shields.io/badge/status-em%20desenvolvimento-yellow?style=flat)

Aplicação web para descobrir e organizar jogos, construída com **Django** e a **[API RAWG](https://rawg.io/)**.

> Mais do que um catálogo: o Games Explorer tem uma **estante pessoal** onde você acompanha o que quer jogar, está jogando e já zerou — com dashboard, notas e reviews próprios.

---

## ✨ Funcionalidades

### 🔍 Exploração
- Busca de jogos com **contador de resultados**
- **Filtros combinados**: plataforma (PC · PlayStation · Xbox · Nintendo), gênero e ordenação (mais avaliados · mais recentes · A-Z)
- Paginação que preserva todos os filtros ativos
- Página de detalhe com **galeria de screenshots** interativa, plataformas disponíveis e informações completas

### 📚 Estante pessoal
- Organize seus jogos em três listas: **Quero jogar**, **Jogando** e **Zerei**
- **Dashboard** com contadores por status e barra de progresso geral
- Para jogos zerados: adicione uma **nota (1–5)** e uma **review pessoal**

### ❤️ Favoritos & Conta
- Salve favoritos separados da estante, com página dedicada
- Cadastro e login — cada usuário tem sua própria estante e favoritos

---

## 🗺️ Fluxo principal

```
Início
  └─ Buscar / Filtrar jogos
       └─ Ver detalhe do jogo
            ├─ Favoritar ❤️
            └─ Adicionar à estante 📚
                 └─ Minha Estante
                      ├─ Dashboard (contadores + progresso)
                      ├─ Mudar status (Quero jogar → Jogando → Zerei)
                      └─ Avaliar e escrever review (jogos zerados)
```

---

## 🛠️ Tecnologias

| Camada | Tecnologia |
|--------|-----------|
| Backend | Python 3 · Django 5 |
| API externa | [RAWG Video Games Database](https://rawg.io/apidocs) |
| Frontend | HTML · CSS · JavaScript vanilla |
| Banco de dados | SQLite |
| Configuração | python-decouple (`.env`) |

---

## 🚀 Como rodar localmente

**Pré-requisitos:** Python 3.10+ e pip

```bash
# 1. Clone o repositório
git clone https://github.com/gabrielbastosg/Game_explorer-Django.git
cd Game_explorer-Django

# 2. Crie e ative a virtual environment
python -m venv .venv
.venv\Scripts\activate        # Windows
# source .venv/bin/activate   # Linux/macOS

# 3. Instale as dependências
pip install -r requirements.txt
```

Crie um arquivo `.env` na raiz do projeto:

```env
SECRET_KEY=sua_chave_secreta_django
RAWG_API_KEY=sua_chave_rawg
```

> Chave gratuita da RAWG disponível em [rawg.io/apidocs](https://rawg.io/apidocs).

```bash
# 4. Rode as migrations e inicie o servidor
python manage.py migrate
python manage.py runserver
```

Acesse **http://127.0.0.1:8000** 🎉

---

## 📁 Estrutura

```
games_explorer/
├── config/              # Configurações do projeto (settings, urls)
├── games/
│   ├── templates/       # HTML de cada página
│   ├── static/          # CSS e JS por página
│   ├── models.py        # FavoriteGame · GameStatus
│   ├── views.py         # Lógica e integração com a API RAWG
│   └── urls.py
└── manage.py
```

---

## 🧠 Aprendizados

- Consumo de API externa com `requests` e tratamento de erros (HTTP 404, falhas de rede)
- Autenticação e autorização nativas do Django
- Modelagem relacional com `ForeignKey` para dados isolados por usuário
- Filtros dinâmicos combinados com preservação de estado na paginação
- Manipulação do DOM com JavaScript puro (galeria de screenshots)
- CSS com variáveis, gradientes e animações sem frameworks externos

---

Dados de jogos fornecidos por **[RAWG](https://rawg.io/)** · Desenvolvido por **[Gabriel Bastos](https://github.com/gabrielbastosg)**
