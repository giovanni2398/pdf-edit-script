#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re
import glob
from datetime import datetime
import fitz  # PyMuPDF
from unidecode import unidecode

# Constantes
YEAR = 2025
DATE_FORMAT = '%d/%m/%Y'
PATIENT_MARKER = "Paciente:"
DATE_MARKER = "Brasília,"
OUTPUT_DATE_FORMAT = "-%m-%d"  # Formato da data no nome do arquivo

def normalize_name(name):
    """
    Normaliza o nome do paciente.
    
    Args:
        name (str): Nome original do paciente
        
    Returns:
        str: Nome normalizado (maiúsculas, sem acentos, sem caracteres especiais)
    """
    # Converte para maiúsculas
    name = name.upper()
    # Remove acentos e caracteres especiais
    name = unidecode(name)
    # Remove caracteres que não são letras, números ou espaços
    name = re.sub(r'[^A-Z0-9 ]', '', name)
    return name

def validate_date(date_str):
    """
    Valida se a data está no formato DD/MM/2025
    
    Args:
        date_str (str): String contendo a data a ser validada
        
    Returns:
        bool: True se a data for válida, False caso contrário
    """
    try:
        date_obj = datetime.strptime(date_str, DATE_FORMAT)
        if date_obj.year != YEAR:
            return False
        return True
    except ValueError:
        return False

def create_folder(folder_name):
    """
    Cria uma pasta com o nome especificado ou usa uma existente.
    
    Args:
        folder_name (str): Nome da pasta a ser criada ou usada
        
    Returns:
        str: Caminho da pasta
    """
    # Verifica se a pasta já existe
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
        print(f"Pasta criada: {folder_name}/")
    else:
        print(f"Pasta já existe: {folder_name}/")
    
    return folder_name

def edit_pdf(input_pdf, output_pdf, patient_name, date_str):
    """
    Edita o PDF modificando o conteúdo textual para substituir o nome do paciente e a data.
    
    Args:
        input_pdf (str): Caminho do arquivo PDF original
        output_pdf (str): Caminho onde o PDF editado será salvo
        patient_name (str): Nome do paciente (normalizado)
        date_str (str): Data no formato DD/MM/YYYY
        
    Returns:
        bool: True se a edição foi bem-sucedida
    """
    print(f"Processando: {os.path.basename(input_pdf)}")
    
    # Abre o documento
    doc = fitz.open(input_pdf)
    
    # Obtém a primeira página
    page = doc[0]
    
    # Cria uma cópia da página para modificação
    new_doc = fitz.open()
    new_page = new_doc.new_page(width=page.rect.width, height=page.rect.height)
    
    # Copia todo o conteúdo da página original
    new_page.show_pdf_page(new_page.rect, doc, 0)
    
    found_patient = False
    found_date = False
    
    # Tenta encontrar e substituir "Paciente:" e "Brasília,"
    try:
        # 1. Busca e substitui o nome do paciente
        patient_areas = page.search_for(PATIENT_MARKER)
        if patient_areas:
            rect = patient_areas[0]  # [x0, y0, x1, y1]
            
            # Estendendo o retângulo para a direita para cobrir o nome existente
            extended_rect = fitz.Rect(rect.x1, rect.y0, rect.x1 + 400, rect.y1)
            
            # Insere um retângulo branco para cobrir o texto antigo
            new_page.draw_rect(extended_rect, color=fitz.utils.getColor("white"), fill=fitz.utils.getColor("white"))
            
            # Insere o novo texto
            text_point = fitz.Point(rect.x1 + 5, rect.y0 + (rect.y1 - rect.y0) * 0.8)
            new_page.insert_text(text_point, patient_name, fontname="helv", fontsize=12)
            
            found_patient = True
            
        # 2. Busca e substitui a data
        date_areas = page.search_for(DATE_MARKER)
        if date_areas:
            rect = date_areas[0]
            
            # Estendendo o retângulo para a direita para cobrir a data existente
            extended_rect = fitz.Rect(rect.x1, rect.y0, rect.x1 + 100, rect.y1)
            
            # Insere um retângulo branco para cobrir o texto antigo
            new_page.draw_rect(extended_rect, color=fitz.utils.getColor("white"), fill=fitz.utils.getColor("white"))
            
            # Insere o novo texto
            text_point = fitz.Point(rect.x1 + 5, rect.y0 + (rect.y1 - rect.y0) * 0.8)
            new_page.insert_text(text_point, date_str, fontname="helv", fontsize=12)
            
            found_date = True
            
    except Exception as e:
        print(f"Erro ao tentar a substituição direta: {str(e)}")
    
    # Salva o documento modificado
    new_doc.save(output_pdf)
    new_doc.close()
    doc.close()
    
    # Reporta o resultado
    if found_patient and found_date:
        print(f"✓ Arquivo editado com sucesso: {os.path.basename(output_pdf)}")
    elif found_patient:
        print(f"⚠ Apenas o campo do paciente foi editado: {os.path.basename(output_pdf)}")
    elif found_date:
        print(f"⚠ Apenas o campo da data foi editado: {os.path.basename(output_pdf)}")
    else:
        print(f"⚠ Nenhum campo foi editado: {os.path.basename(output_pdf)}")
        
    return True

def process_all_pdf_models(patient_name, date_str, folder_name):
    """
    Processa todos os modelos de PDF disponíveis para um paciente.
    
    Args:
        patient_name (str): Nome normalizado do paciente
        date_str (str): Data no formato DD/MM/YYYY
        folder_name (str): Nome da pasta onde salvar os arquivos editados
        
    Returns:
        bool: True se pelo menos um modelo foi processado com sucesso
    """
    # Criar/usar a pasta especificada
    folder_path = create_folder(folder_name)
    
    # Obter todos os arquivos modelo (arquivos PDF que não contém o nome do paciente)
    pdf_models = [f for f in glob.glob("*.pdf") if not re.search(r'_[A-Z0-9 ]+_', f)]
    
    if not pdf_models:
        print("Nenhum modelo de PDF encontrado na pasta atual.")
        return False
    
    print(f"\nProcessando {len(pdf_models)} modelo(s) de PDF para o paciente {patient_name}:")
    
    success_count = 0
    
    # Processa cada modelo
    for model_pdf in pdf_models:
        base_name = os.path.splitext(model_pdf)[0]
        output_pdf = os.path.join(folder_path, f"{base_name}_{date_str.replace('/', '-')}.pdf")
        
        try:
            # Editar o PDF
            print(f"\nEditando o modelo: {model_pdf}")
            if edit_pdf(model_pdf, output_pdf, patient_name, date_str):
                success_count += 1
        except Exception as e:
            print(f"❌ Erro ao processar {model_pdf}: {str(e)}")
    
    print(f"\nResumo: {success_count} de {len(pdf_models)} arquivos processados com sucesso.")
    print(f"Os arquivos editados estão na pasta: {folder_path}/")
    
    return success_count > 0

def get_patient_name():
    """
    Solicita e normaliza o nome do paciente através da interface de linha de comando.
    
    Returns:
        str: Nome normalizado do paciente
    """
    while True:
        patient_name = input("\nDigite o nome do paciente: ")
        if patient_name.strip():
            # Normaliza o nome (maiúsculas, sem caracteres especiais)
            formatted_name = normalize_name(patient_name)
            print(f"Nome formatado: {formatted_name}")
            confirmation = input("O nome está correto? (s/n): ").lower()
            if confirmation in ['s', 'sim', 'y', 'yes']:
                return formatted_name
        else:
            print("❌ O nome não pode estar vazio.")

def get_date():
    """
    Solicita e valida a data através da interface de linha de comando.
    
    Returns:
        str: Data validada no formato DD/MM/YYYY
    """
    while True:
        date_str = input(f"\nDigite a data do pedido (DD/MM/{YEAR}): ")
        if validate_date(date_str):
            return date_str
        else:
            print(f"❌ Data inválida. Use o formato DD/MM/{YEAR}.")

def get_folder_name(patient_name):
    """
    Solicita o nome da pasta onde os arquivos serão salvos.
    Oferece o nome do paciente como padrão, mas permite personalizar.
    
    Args:
        patient_name (str): Nome normalizado do paciente para sugerir como padrão
        
    Returns:
        str: Nome normalizado da pasta escolhida
    """
    print(f"\nPasta padrão sugerida: {patient_name}")
    use_default = input("Usar esta pasta? (s/n): ").lower()
    
    if use_default in ['s', 'sim', 'y', 'yes']:
        return patient_name
    
    while True:
        folder_name = input("Digite o nome da pasta para salvar os arquivos: ")
        if folder_name.strip():
            # Normaliza o nome da pasta
            normalized_folder = normalize_name(folder_name)
            print(f"Nome da pasta: {normalized_folder}/")
            confirmation = input("O nome da pasta está correto? (s/n): ").lower()
            if confirmation in ['s', 'sim', 'y', 'yes']:
                return normalized_folder
        else:
            print("❌ O nome da pasta não pode estar vazio.")

def main():
    """Função principal que coordena o fluxo do programa."""
    print("=" * 70)
    print(f"{'EDITOR DE PEDIDOS MÉDICOS - AUTOMAÇÃO DE DOCUMENTOS':^70}")
    print("=" * 70)
    
    try:
        # 1. Obter informações do paciente
        patient_name = get_patient_name()
        date_str = get_date()
        
        # 2. Solicitar nome da pasta onde salvar os arquivos
        folder_name = get_folder_name(patient_name)
        
        # 3. Processar todos os PDFs
        process_all_pdf_models(patient_name, date_str, folder_name)
        
    except KeyboardInterrupt:
        print("\n\n⚠ Operação cancelada pelo usuário.")
    except Exception as e:
        print(f"\nOcorreu um erro durante o processamento: {str(e)}")
        print("Dica: Verifique se todas as dependências estão instaladas:")
        print("      pip install PyMuPDF unidecode")

if __name__ == "__main__":
    main() 