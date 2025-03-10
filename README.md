# Iniciando o Projeto

## Ambiente de Desenvolvimento

1. Crie um ambiente virtual Python:
```bash
python -m venv .venv
```

2. Ative o ambiente virtual:
```bash
# Linux/MacOS
source .venv/bin/activate

# Windows
.venv\Scripts\activate
```

3. Instale as dependências:
```bash
pip install -r requirements.txt
```

4. Execute a aplicação:
```bash
python -m src.main
```

## Configuração do Banco de Dados

1. Inicie o container Docker:
```bash
docker compose up -d
```

2. Configure o banco de dados:
```bash
python -m src.database
```

3. Importe os dados iniciais:
- Execute o notebook `other/convert_data.ipynb` para adicionar os dados dos Hot Wheels

## Notas
- Certifique-se de ter o Docker instalado para a configuração do banco PostgreSQL
- O ambiente virtual (.venv) deve estar ativo para todos os comandos Python