# PDF-edit-script

## Descrição

Este script permite realizar edições em um arquivo modelo de pedido médico em formato PDF. O script modifica especificamente o nome do paciente e a data do pedido no documento, utilizando o arquivo modelo "PEDIDO COM ASS.pdf".

## Funcionalidades

- Edição do nome do paciente (convertendo para caixa alta e removendo caracteres especiais)
- Edição da data do pedido no formato DD/MM/2025
- Preservação do restante do conteúdo do documento PDF original

## Como Funciona

O script usa uma abordagem robusta para editar o PDF:

1. **Localização inteligente de texto**: Identifica a posição exata dos campos "Paciente:" e "Brasília," no documento
2. **Edição precisa**: Substitui apenas o texto após esses marcadores, mantendo o formato e a aparência originais
3. **Preservação do conteúdo**: Todo o restante do documento permanece inalterado

## Requisitos

- Python 3.6 ou superior
- Bibliotecas necessárias:
  - PyMuPDF (fitz)
  - unidecode

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

1. Certifique-se de que o arquivo modelo "PEDIDO COM ASS.pdf" esteja na mesma pasta do script
2. Execute o script:

```
python pdf_editor.py
```

3. Siga as instruções no terminal:

   - Insira o nome do paciente (o script irá formatá-lo para maiúsculas e remover caracteres especiais)
   - Insira a data no formato DD/MM/2025

4. O arquivo PDF editado será salvo na mesma pasta com o nome "PEDIDO COM ASS*[NOME_PACIENTE]*[DATA].pdf"

## Resolução de Problemas

Se o script não encontrar os campos para edição, um diagnóstico será exibido no terminal mostrando o texto extraído do PDF.

## Licença

Este projeto está licenciado sob a licença MIT - veja o arquivo LICENSE para mais detalhes.
