# PDF-edit-script

## Descrição

Este script automatiza a edição de arquivos modelo de pedidos médicos em formato PDF. O script localiza e modifica especificamente o nome do paciente e a data do pedido em múltiplos modelos de PDF, criando uma pasta individual para cada paciente.

## Funcionalidades

- Edição do nome do paciente (convertendo para caixa alta e removendo caracteres especiais)
- Edição da data do pedido no formato DD/MM/2025
- Escolha personalizada da pasta para salvar os arquivos
- Processamento em lote de múltiplos modelos de PDF
- Preservação do formato e aparência original dos documentos

## Como Funciona

O script implementa um fluxo de trabalho completo:

1. **Captura de dados**: Solicita o nome do paciente e a data do pedido
2. **Escolha da pasta**: Permite selecionar ou criar uma pasta para os documentos editados
3. **Localização de modelos**: Identifica todos os PDFs modelo disponíveis no diretório
4. **Edição inteligente**: Substitui precisamente o nome do paciente e a data em cada modelo
5. **Organização**: Salva os arquivos editados na pasta escolhida

## Recursos Técnicos

- Localização precisa de texto usando o PyMuPDF
- Tratamento de erros robusto
- Interface de usuário com feedback detalhado
- Manipulação eficiente de múltiplos arquivos
- Código modular e bem documentado

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

1. Coloque todos os seus modelos de PDF na pasta do projeto
2. Execute o script:

```
python pdf_editor.py
```

3. Siga as instruções no terminal:

   - Digite o nome do paciente (será formatado automaticamente)
   - Digite a data no formato DD/MM/2025
   - Escolha a pasta para salvar os arquivos (por padrão, usa o nome do paciente)

4. O script criará:
   - A pasta especificada (se não existir)
   - Cópias editadas de todos os PDFs modelo nessa pasta

## Personalização

O script está configurado para localizar estes marcadores nos PDFs:

- "Paciente:" - Após este texto será inserido o nome do paciente
- "Brasília," - Após este texto será inserida a data

Se seus modelos usam marcadores diferentes, você pode modificar as constantes no início do script.

## Resolução de Problemas

Se o script não encontrar os campos para edição, um diagnóstico será exibido no terminal mostrando o texto extraído do PDF.

## Licença

Este projeto está licenciado sob a licença MIT - veja o arquivo LICENSE para mais detalhes.
