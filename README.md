# 🏥 Sistema de Agendamentos - API REST

[![Python](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Django](https://img.shields.io/badge/django-5.1.0-green.svg)](https://www.djangoproject.com/)
[![DRF](https://img.shields.io/badge/djangorestframework-3.16.0-red.svg)](https://www.django-rest-framework.org/)
[![Coverage](https://img.shields.io/badge/coverage-90%25-brightgreen.svg)](#test-coverage)
[![License](https://img.shields.io/badge/license-Privada-red.svg)](LICENSE)

> **Sistema completo de gerenciamento de agendamentos para clínicas, consultórios e prestadores de serviços.**

Um sistema robusto desenvolvido em Django REST Framework para gerenciar agendamentos entre clientes e profissionais, com funcionalidades completas de CRUD, validações personalizadas, e autenticação.

## 📋 Índice

- [🏥 Sistema de Agendamentos - API REST](#-sistema-de-agendamentos---api-rest)
  - [📋 Índice](#-índice)
  - [🚀 Características](#-características)
  - [🏗️ Arquitetura](#️-arquitetura)
  - [📊 Modelo de Dados](#-modelo-de-dados)
  - [🛠️ Tecnologias](#️-tecnologias)
  - [⚙️ Instalação](#️-instalação)
    - [Pré-requisitos](#pré-requisitos)
    - [Configuração do Ambiente](#configuração-do-ambiente)
    - [Instalação das Dependências](#instalação-das-dependências)
    - [Configuração do Banco de Dados](#configuração-do-banco-de-dados)
    - [Executar o Servidor](#executar-o-servidor)
  - [🔧 Configuração](#-configuração)
    - [Variáveis de Ambiente](#variáveis-de-ambiente)
    - [Configurações do Django](#configurações-do-django)
  - [📚 API Endpoints](#-api-endpoints)
    - [Autenticação](#autenticação)
    - [Endpoints Disponíveis](#endpoints-disponíveis)
    - [Exemplos de Uso](#exemplos-de-uso)
  - [🧪 Testes](#-testes)
    - [Executar Testes](#executar-testes)
    - [Test Coverage](#test-coverage)
    - [Estrutura de Testes](#estrutura-de-testes)
  - [📁 Estrutura do Projeto](#-estrutura-do-projeto)
  - [🔍 Validações](#-validações)
    - [Validações Personalizadas](#validações-personalizadas)
    - [Padronização de Dados](#padronização-de-dados)
  - [🌐 Deploy](#-deploy)
    - [Usando Docker](#usando-docker)
    - [Deploy em Produção](#deploy-em-produção)
  - [🤝 Contribuição](#-contribuição)
  - [📄 Licença](#-licença)
  - [📞 Contato](#-contato)

## 🚀 Características

- ✅ **API REST completa** com operações CRUD para todos os recursos
- 🔐 **Autenticação e autorização** integradas
- 📝 **Validações robustas** com mensagens de erro claras
- 🏛️ **Arquitetura limpa** seguindo boas práticas do Django
- 📊 **Modelagem relacional** otimizada para agendamentos
- 🧪 **Cobertura de testes** extensiva (90%+)
- 📱 **API RESTful** com serialização padronizada
- 🔄 **Normalização automática** de dados de entrada
- 📋 **Paginação** automática para listas grandes
- 🕒 **Gestão de horários** com timezone Brasil/São Paulo

## 🏗️ Arquitetura

O sistema segue uma arquitetura em camadas baseada no padrão MVC do Django:

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   API Views     │    │   Serializers   │    │     Models      │
│   (ViewSets)    │◄──►│  (Validation)   │◄──►│  (Database)     │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         ▲                       ▲                       ▲
         │                       │                       │
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   URL Router    │    │   Validators    │    │   Migrations    │
│  (Endpoints)    │    │   (Business)    │    │   (Schema)      │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## 📊 Modelo de Dados

O sistema é estruturado em torno de 6 entidades principais:

```mermaid
erDiagram
    City ||--o{ Business : "localizada_em"
    Business ||--o{ Professional : "trabalha_em"
    Business ||--o{ Customer : "cliente_de"
    Business ||--o{ Service : "oferece"
    Business ||--o{ AvailableDay : "dias_disponiveis"
    Professional ||--o{ AvailableDay : "disponibilidade"
    
    Business ||--o{ Appointment : "agendamentos"
    Customer ||--o{ Appointment : "possui"
    Service ||--o{ Appointment : "utiliza"
    Professional ||--o{ Appointment : "atende"

    City {
        string name
        string state
    }
    
    Business {
        string name
        string category
        string address
        string public_phone
        string restricted_phone
        string email
        json schedule
        boolean closed_on_holidays
    }
    
    Professional {
        string name
        string cpf
        string speciality
        string email
        string phone
        json schedule
    }
    
    Customer {
        string name
        date birth_date
        string registration_source
        string cpf
        string email
        string phone
    }
    
    Service {
        string name
        text description
        decimal price
        duration duration
    }
    
    AvailableDay {
        date date
        time blocked_start_time
        time blocked_end_time
    }
    
    Appointment {
        datetime datetime
        string status
        string source
    }
```

## 🛠️ Tecnologias

| Tecnologia | Versão | Propósito |
|------------|--------|-----------|
| **Python** | 3.11+ | Linguagem principal |
| **Django** | 5.1.0 | Framework web |
| **Django REST Framework** | 3.16.0 | API REST |
| **PostgreSQL** | - | Banco de dados principal |
| **SQLite** | - | Banco para desenvolvimento/testes |
| **Coverage.py** | 7.8.2 | Cobertura de testes |
| **HTTPX** | 0.28.1 | Cliente HTTP para testes |

## ⚙️ Instalação

### Pré-requisitos

- **Python 3.11+** instalado
- **Git** para clonar o repositório
- **PostgreSQL** (opcional, para produção)

### Configuração do Ambiente

```bash
# Clonar o repositório
git clone https://github.com/seu-usuario/project-backend.git
cd project-backend

# Criar ambiente virtual
python -m venv venv

# Ativar ambiente virtual
# Linux/Mac
source venv/bin/activate
# Windows
venv\Scripts\activate
```

### Instalação das Dependências

```bash
# Instalar dependências
pip install -r requirements.txt
```

### Configuração do Banco de Dados

```bash
# Aplicar migrações
python manage.py migrate

# Carregar dados iniciais das cidades
python manage.py loaddata cities.json

# Criar superusuário (opcional)
python manage.py createsuperuser
```

### Executar o Servidor

```bash
# Servidor de desenvolvimento
python manage.py runserver

# API estará disponível em: http://localhost:8000/
```

## 🔧 Configuração

### Variáveis de Ambiente

Crie um arquivo `.env` na raiz do projeto:

```env
# Configurações básicas
DEBUG=True
SECRET_KEY=your-secret-key-here

# Banco de dados (PostgreSQL)
DATABASE_URL=postgresql://user:password@localhost:5432/dbname

# Configurações de timezone
TIME_ZONE=America/Sao_Paulo
USE_TZ=True

# Configurações de CORS (se necessário)
ALLOWED_HOSTS=localhost,127.0.0.1
```

### Configurações do Django

```python
# project/settings.py principais configurações

# Paginação padrão da API
REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20,
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.TokenAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
}
```

## 📚 API Endpoints

### Autenticação

Todas as rotas (exceto cidades) requerem autenticação. Use Token Authentication ou Session Authentication.

```bash
# Obter token (se usando Token Auth)
POST /api-auth/login/
```

### Endpoints Disponíveis

| Endpoint | Métodos | Descrição |
|----------|---------|-----------|
| `/cities/` | GET | Lista cidades disponíveis (read-only) |
| `/businesses/` | GET, POST, PUT, PATCH, DELETE | Gerenciar empresas |
| `/customers/` | GET, POST, PUT, PATCH, DELETE | Gerenciar clientes |
| `/services/` | GET, POST, PUT, PATCH, DELETE | Gerenciar serviços |
| `/professionals/` | GET, POST, PUT, PATCH, DELETE | Gerenciar profissionais |
| `/available_days/` | GET, POST, PUT, PATCH, DELETE | Gerenciar disponibilidade |
| `/appointments/` | GET, POST, PUT, PATCH, DELETE | Gerenciar agendamentos |

### Exemplos de Uso

#### 1. Listar Cidades

```bash
GET /cities/
```

```json
{
    "count": 2,
    "results": [
        {
            "id": 1,
            "name": "Ariquemes",
            "state": "RO"
        },
        {
            "id": 2,
            "name": "Porto Velho",
            "state": "RO"
        }
    ]
}
```

#### 2. Criar um Negócio

```bash
POST /businesses/
Content-Type: application/json
```

```json
{
    "name": "Clínica Saúde Total",
    "category": "C1",
    "city": 1,
    "address": "Rua das Flores, 123",
    "public_phone": "(69) 3536-1234",
    "restricted_phone": "(69) 99999-9999",
    "email": "contato@saudetotal.com",
    "schedule": {
        "0": {
            "start": "08:00",
            "end": "17:00",
            "breaks": []
        },
        "1": {
            "start": "08:00",
            "end": "17:00",
            "breaks": ["12:00-13:00"]
        }
    },
    "closed_on_holidays": true
}
```

#### 3. Criar um Agendamento

```bash
POST /appointments/
Content-Type: application/json
```

```json
{
    "business": 1,
    "customer": 1,
    "service": 1,
    "professional": 1,
    "datetime": "2024-06-15T14:30:00",
    "source": "WEBSITE",
    "status": "SCHEDULED"
}
```

#### 4. Filtrar Agendamentos

```bash
# Por data
GET /appointments/?datetime__date=2024-06-15

# Por profissional
GET /appointments/?professional=1

# Por status
GET /appointments/?status=SCHEDULED
```

## 🧪 Testes

### Executar Testes

```bash
# Todos os testes
python manage.py test

# Testes específicos
python manage.py test app.tests.integration
python manage.py test app.tests.models

# Com verbose
python manage.py test --verbosity=2
```

### Test Coverage

```bash
# Executar com coverage
coverage run --source='.' manage.py test
coverage report --show-missing
coverage html

# Ou usar Makefile
make coverage
make coverage-html
```

### Estrutura de Testes

```
app/tests/
├── integration/
│   ├── models/           # Testes dos modelos
│   │   ├── test_model_appointment.py
│   │   ├── test_model_business.py
│   │   └── ...
│   └── views/            # Testes das views/API
│       ├── test_view_appointment.py
│       ├── test_view_business.py
│       └── ...
└── unit/                 # Testes unitários
    ├── test_validators.py
    ├── test_serializers.py
    └── test_utils.py
```

## 📁 Estrutura do Projeto

```
project-backend/
├── 📁 app/                     # Aplicação principal
│   ├── 📁 migrations/          # Migrações do banco
│   │   ├── 📁 integration/    # Testes de integração
│   │   └── 📁 unit/           # Testes unitários
│   ├── 📄 models.py           # Modelos de dados
│   ├── 📄 serializers.py      # Serializers da API
│   ├── 📄 views.py            # ViewSets da API
│   ├── 📄 validators.py       # Validações customizadas
│   └── 📄 utils.py            # Utilitários
├── 📁 project/                # Configurações do Django
│   ├── 📄 settings.py         # Configurações principais
│   ├── 📄 urls.py             # Roteamento de URLs
│   └── 📄 wsgi.py            # WSGI para deploy
├── 📁 logs/                   # Logs da aplicação
├── 📄 manage.py               # Comando principal Django
├── 📄 requirements.txt        # Dependências Python
├── 📄 Makefile               # Comandos automatizados
├── 📄 .coveragerc            # Configuração coverage
├── 📄 run_tests.sh           # Script de testes
└── 📄 README.md              # Esta documentação
```

## 🔍 Validações

### Validações Personalizadas

O sistema implementa validações robustas para:

- **CPF**: Validação com algoritmo oficial
- **Telefones**: Formato brasileiro com DDD
- **E-mails**: Validação e normalização
- **Datas**: Não permite agendamentos no passado
- **Horários**: Validação de horários de funcionamento
- **Preços**: Valores positivos e formato decimal

### Padronização de Dados

Dados são automaticamente padronizados antes da validação:

```python
# Entrada do usuário → Dados padronizados
"(11) 99999-9999"     → "11999999999"
"joao.silva@EMAIL.COM" → "joao.silva@email.com"
"joão da silva"        → "João Da Silva"
"111.222.333-44"       → "11122233344"
```

## 🌐 Deploy

### Usando Docker

```dockerfile
# Dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
```

```bash
# Build e execução
docker build -t appointment-api .
docker run -p 8000:8000 appointment-api
```

### Deploy em Produção

1. **Configure as variáveis de ambiente**
2. **Use PostgreSQL** ao invés de SQLite
3. **Configure ALLOWED_HOSTS**
4. **Desative DEBUG**
5. **Configure arquivos estáticos**
6. **Use HTTPS** em produção

```python
# settings/production.py
DEBUG = False
ALLOWED_HOSTS = ['seu-dominio.com']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('DB_NAME'),
        'USER': os.environ.get('DB_USER'),
        'PASSWORD': os.environ.get('DB_PASSWORD'),
        'HOST': os.environ.get('DB_HOST'),
        'PORT': os.environ.get('DB_PORT'),
    }
}
```

## 🤝 Contribuição

1. **Fork** o projeto
2. Crie uma **branch** para sua feature (`git checkout -b feature/nova-funcionalidade`)
3. **Commit** suas mudanças (`git commit -m 'Adiciona nova funcionalidade'`)
4. **Push** para a branch (`git push origin feature/nova-funcionalidade`)
5. Abra um **Pull Request**

### Diretrizes para Contribuição

- ✅ Escreva testes para novas funcionalidades
- ✅ Mantenha a cobertura de testes acima de 85%
- ✅ Siga as convenções de código Python (PEP 8)
- ✅ Documente mudanças na API
- ✅ Use commits semânticos

## 📄 Licença

Este projeto está licenciado sob a Licença MIT - veja o arquivo [LICENSE](LICENSE) para detalhes.

## 📞 Contato

- **Desenvolvedor**: [Seu Nome](mailto:seu-email@exemplo.com)
- **Projeto**: [GitHub](https://github.com/seu-usuario/project-backend)
- **Issues**: [GitHub Issues](https://github.com/seu-usuario/project-backend/issues)

---

⭐ Se este projeto foi útil para você, considere dar uma estrela no GitHub! 