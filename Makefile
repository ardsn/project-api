.PHONY: test coverage coverage-html coverage-report

# Executar apenas testes
test:
	python manage.py test

# Executar testes com coverage
coverage:
	coverage run --source='.' manage.py test
	coverage report

# Gerar relatório HTML
coverage-html:
	coverage run --source='.' manage.py test
	coverage html
	@echo "📄 Relatório HTML: htmlcov/index.html"

# Relatório detalhado
coverage-report:
	coverage run --source='.' manage.py test
	coverage report --show-missing
	coverage html

# Limpar arquivos de coverage
coverage-clean:
	coverage erase
	rm -rf htmlcov/
	rm -f .coverage

# Executar testes específicos com coverage
test-unit:
	coverage run --source='.' manage.py test app.tests.unit
	coverage report --show-missing 

test-integration:
	coverage run --source='.' manage.py test app.tests.integration
	coverage report --show-missing 