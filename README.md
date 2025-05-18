# PDF-edit-script

## Descrição

Este script permite realizar edições em um arquivo modelo de pedido médico em formato PDF. O script modifica especificamente o nome do paciente e a data do pedido no documento.

## Funcionalidades

- Edição do nome do paciente (convertendo para caixa alta e removendo caracteres especiais)
- Edição da data do pedido no formato DD/MM/2025
- Preservação do restante do conteúdo do documento PDF original

## Requisitos

- Python 3.6 ou superior
- Bibliotecas necessárias (listadas no arquivo requirements.txt)

## Instalação

1. Clone este repositório:

```
git clone https://github.com/seu-usuario/PDF-edit-script.git
cd PDF-edit-script
```

2. Crie um ambiente virtual (recomendado):

```
python -m venv venv
```

3. Ative o ambiente virtual:

   - Windows:

   ```
   venv\Scripts\activate
   ```

   - Linux/Mac:

   ```
   source venv/bin/activate
   ```

4. Instale as dependências:

```
pip install -r requirements.txt
```

## Uso

1. Coloque o arquivo PDF modelo na pasta do projeto
2. Execute o script:

```
python pdf_editor.py
```

3. Siga as instruções no terminal:
   - Insira o nome do paciente (o script irá formatá-lo para maiúsculas e remover caracteres especiais)
   - Insira a data no formato DD/MM/2025
4. O arquivo PDF editado será salvo com um novo nome na mesma pasta

## Licença

Este projeto está licenciado sob a licença MIT - veja o arquivo LICENSE para mais detalhes.
