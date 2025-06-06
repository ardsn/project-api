# 📝 Changelog

Todas as mudanças notáveis neste projeto serão documentadas neste arquivo.

O formato é baseado em [Keep a Changelog](https://keepachangelog.com/pt-BR/1.0.0/),
e este projeto adere ao [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Não Lançado]

### 🚀 Adicionado
- Documentação completa do projeto no README.md
- Guia de contribuição (CONTRIBUTING.md)
- Configuração de test coverage com coverage.py
- Makefile para comandos automatizados

### 🔄 Alterado
- Melhorias na estrutura de testes
- Padronização de formatação de código

### 🐛 Corrigido
- Correção no teste `test_create_appointment` com formato de datetime

## [1.0.0] - 2024-12-XX

### 🚀 Adicionado
- **Sistema completo de agendamentos** com API REST
- **Modelos principais**:
  - `City`: Cidades disponíveis (read-only)
  - `Business`: Empresas/negócios
  - `Customer`: Clientes
  - `Service`: Serviços oferecidos
  - `Professional`: Profissionais
  - `AvailableDay`: Disponibilidade de horários
  - `Appointment`: Agendamentos
- **API REST completa** com operações CRUD
- **Autenticação** via Session e Token Authentication
- **Validações robustas**:
  - CPF com algoritmo oficial brasileiro
  - Telefones no formato brasileiro
  - E-mails com normalização automática
  - Datas e horários (timezone Brasil/São Paulo)
  - Preços e durações
- **Serializers personalizados** com normalização automática de dados
- **ViewSets** para todos os recursos
- **Paginação automática** para listas
- **Constraints de banco** para garantir integridade
- **Testes abrangentes**:
  - Testes de integração para views/API
  - Testes de modelos
  - Cobertura de testes com coverage.py
- **Configurações de desenvolvimento** com SQLite
- **Suporte a PostgreSQL** para produção
- **Estrutura de logs** configurada
- **Timezone** configurado para Brasil (America/Sao_Paulo)

### 🔧 Técnico
- **Django 5.1.0** como framework principal
- **Django REST Framework 3.16.0** para API
- **Python 3.11+** como requisito mínimo
- **Coverage.py** para análise de cobertura de testes
- **HTTPX** para testes de API
- **Django-environ** para configurações de ambiente
- **Psycopg** para conexão PostgreSQL

### 📊 Funcionalidades
- **Gestão de Negócios**: Criação e gerenciamento de empresas
- **Cadastro de Clientes**: Sistema completo de clientes por negócio
- **Catálogo de Serviços**: Serviços com preço e duração
- **Equipe de Profissionais**: Cadastro de profissionais com especialidades
- **Controle de Disponibilidade**: Dias disponíveis e bloqueios de horários
- **Sistema de Agendamentos**: Agendamentos com validações de horário
- **Múltiplas Fontes**: Agendamentos via WhatsApp, Website, etc.
- **Status de Agendamentos**: Agendado, Cancelado, Concluído
- **Validação de Duplicatas**: Evita agendamentos duplicados
- **Horários de Funcionamento**: JSON configurável por negócio/profissional

### 🔒 Segurança
- **Autenticação obrigatória** para todas as operações (exceto cidades)
- **Validação de dados** antes de persistir no banco
- **Constraints de unicidade** no banco de dados
- **Sanitização automática** de dados de entrada
- **Proteção CSRF** habilitada

### 📱 API
- **Endpoints RESTful** seguindo convenções
- **Serialização JSON** padronizada
- **Códigos de status HTTP** apropriados
- **Mensagens de erro** descritivas
- **Filtros de busca** disponíveis
- **Ordenação** configurável
- **Paginação** automática

---

## 📌 Legenda

- 🚀 **Adicionado**: para novas funcionalidades
- 🔄 **Alterado**: para mudanças em funcionalidades existentes
- ⚠️ **Depreciado**: para funcionalidades que serão removidas em breve
- 🗑️ **Removido**: para funcionalidades removidas
- 🐛 **Corrigido**: para correções de bugs
- 🔒 **Segurança**: para correções de vulnerabilidades

---

## 🔗 Links

- [Repository](https://github.com/seu-usuario/project-backend)
- [Issues](https://github.com/seu-usuario/project-backend/issues)
- [Pull Requests](https://github.com/seu-usuario/project-backend/pulls) 