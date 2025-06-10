# 🤝 Guia de Contribuição

Obrigado por considerar contribuir para o Sistema de Agendamentos! Este documento fornece diretrizes para contribuir de forma efetiva.

## 📋 Índice

- [🤝 Guia de Contribuição](#-guia-de-contribuição)
  - [📋 Índice](#-índice)
  - [🚀 Como Começar](#-como-começar)
  - [🐛 Reportando Bugs](#-reportando-bugs)
  - [✨ Sugerindo Melhorias](#-sugerindo-melhorias)
  - [💻 Contribuindo com Código](#-contribuindo-com-código)
    - [Processo de Pull Request](#processo-de-pull-request)
    - [Padrões de Código](#padrões-de-código)
    - [Testes](#testes)
    - [Commits](#commits)
  - [📝 Contribuindo com Documentação](#-contribuindo-com-documentação)
  - [🏷️ Versionamento](#️-versionamento)
  - [📞 Precisa de Ajuda?](#-precisa-de-ajuda)

## 🚀 Como Começar

1. **Fork** o repositório no GitHub
2. **Clone** seu fork localmente:
   ```bash
   git clone https://github.com/SEU_USERNAME/project-api.git
   cd project-api
   ```
3. **Configure** o ambiente de desenvolvimento:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   # ou venv\Scripts\activate  # Windows
   pip install -r requirements.txt
   ```
4. **Execute** os testes para garantir que tudo está funcionando:
   ```bash
   python manage.py test
   ```

## 🐛 Reportando Bugs

Antes de reportar um bug, verifique se ele já não foi reportado nas [Issues](https://github.com/ardsn/project-api/issues).

### Como reportar um bug:

1. **Use** o template de issue para bugs
2. **Descreva** o comportamento esperado vs atual
3. **Forneça** passos para reproduzir o problema
4. **Inclua** informações do ambiente:
   - Versão do Python
   - Versão do Django
   - Sistema operacional
   - Versão do navegador (se aplicável)

### Exemplo de bug report:

```markdown
**Descrição do Bug**
O endpoint /appointments/ retorna 500 quando data está no formato incorreto.

**Passos para Reproduzir**
1. POST /appointments/ com datetime: "2024-13-01"
2. Observar erro 500

**Comportamento Esperado**
Deveria retornar 400 Bad Request com mensagem de erro clara.

**Ambiente**
- Python: 3.11.0
- Django: 5.1.0
- SO: Ubuntu 22.04
```

## ✨ Sugerindo Melhorias

Sugestões de melhorias são sempre bem-vindas! Para sugerir uma melhoria:

1. **Verifique** se a sugestão já existe nas issues
2. **Abra** uma nova issue com o template de feature request
3. **Descreva** detalhadamente a melhoria proposta
4. **Explique** por que seria útil para o projeto

## 💻 Contribuindo com Código

### Processo de Pull Request

1. **Crie** uma branch para sua feature:
   ```bash
   git checkout -b feature/nova-funcionalidade
   ```

2. **Faça** suas alterações seguindo os padrões do projeto

3. **Adicione** testes para suas alterações:
   ```bash
   # Executar testes
   python manage.py test
   
   # Verificar coverage
   coverage run --source='.' manage.py test
   coverage report
   ```

4. **Commit** suas alterações:
   ```bash
   git commit -m "feat: adiciona validação de CPF mais robusta"
   ```

5. **Push** para seu fork:
   ```bash
   git push origin feature/nova-funcionalidade
   ```

6. **Abra** um Pull Request no GitHub

### Padrões de Código

#### Python/Django
- Siga [PEP 8](https://pep8.org/)
- Use type hints quando possível
- Documente funções complexas
- Mantenha linhas com máximo 88 caracteres

#### Estrutura de arquivos
```python
# models.py
class MinhaModel(models.Model):
    """
    Documentação da model
    """
    campo = models.CharField(max_length=50)
    
    class Meta:
        constraints = [...]
    
    def __str__(self):
        return self.campo
    
    def save(self, **kwargs):
        self.full_clean()
        super().save(**kwargs)

# serializers.py
class MinhaSerializer(serializers.ModelSerializer):
    """
    Serializer para MinhaModel
    """
    class Meta:
        model = MinhaModel
        fields = '__all__'
    
    def to_internal_value(self, data):
        # Padronização de dados
        return super().to_internal_value(data)
```

### Testes

#### Estrutura de Testes
```python
# tests/integration/test_minha_funcionalidade.py
class TestMinhaFuncionalidade(APITestCase):
    
    @classmethod
    def setUpTestData(cls):
        """Setup de dados para todos os testes"""
        cls.user = User.objects.create_user(...)
    
    def setUp(self):
        """Setup antes de cada teste"""
        self.client.force_authenticate(user=self.user)
    
    def test_deve_criar_objeto_com_sucesso(self):
        """Testa criação bem-sucedida"""
        data = {...}
        response = self.client.post('/endpoint/', data)
        
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Model.objects.count(), 1)
    
    def test_deve_falhar_com_dados_invalidos(self):
        """Testa falha com dados inválidos"""
        data = {...}
        response = self.client.post('/endpoint/', data)
        
        self.assertEqual(response.status_code, 400)
```

#### Cobertura de Testes
- **Mínimo**: 85% de cobertura
- **Ideal**: 90%+ de cobertura
- Teste casos de sucesso e falha
- Teste validações e edge cases

### Commits

Use [Conventional Commits](https://conventionalcommits.org/):

```bash
# Tipos de commit
feat: nova funcionalidade
fix: correção de bug
docs: documentação
style: formatação de código
refactor: refatoração sem mudança de funcionalidade
test: adicionar/modificar testes
chore: tarefas de manutenção

# Exemplos
git commit -m "feat: adiciona endpoint para cancelar agendamento"
git commit -m "fix: corrige validação de CPF"
git commit -m "docs: atualiza README com novos endpoints"
git commit -m "test: adiciona testes para validação de telefone"
```

## 📝 Contribuindo com Documentação

Melhorias na documentação são muito valiosas:

### Tipos de documentação:
- **README**: Informações gerais e setup
- **API Docs**: Documentação dos endpoints
- **Code Comments**: Comentários no código
- **Docstrings**: Documentação de funções/classes

### Padrões para documentação:
```python
def minha_funcao(parametro: str) -> dict:
    """
    Breve descrição da função.
    
    Args:
        parametro: Descrição do parâmetro
    
    Returns:
        dict: Descrição do retorno
    
    Raises:
        ValueError: Quando parâmetro é inválido
    
    Example:
        >>> minha_funcao("teste")
        {"resultado": "sucesso"}
    """
    pass
```

## 🏷️ Versionamento

O projeto segue [Semantic Versioning](https://semver.org/):

- **MAJOR**: Mudanças incompatíveis na API
- **MINOR**: Novas funcionalidades compatíveis
- **PATCH**: Correções de bugs compatíveis

Exemplo: `1.2.3`

## 📞 Precisa de Ajuda?

- 💬 **Issues**: Para discussões técnicas
- 📧 **Email**: Para questões privadas
- 💡 **Discussions**: Para ideias e sugestões gerais

### Recursos úteis:
- [Django Documentation](https://docs.djangoproject.com/)
- [Django REST Framework Guide](https://www.django-rest-framework.org/)
- [Python PEP 8 Style Guide](https://pep8.org/)
- [Git Flow](https://nvie.com/posts/a-successful-git-branching-model/)

---

**Obrigado por contribuir! 🚀**

Toda contribuição, por menor que seja, é valiosa para o projeto. 