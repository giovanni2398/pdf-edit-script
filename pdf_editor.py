#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re
from datetime import datetime
import fitz  # PyMuPDF
from unidecode import unidecode

def normalize_name(name):
    """
    Normaliza o nome do paciente:
    - Converte para maiúsculas
    - Remove caracteres especiais/acentos
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
    """
    try:
        date_obj = datetime.strptime(date_str, '%d/%m/%Y')
        if date_obj.year != 2025:
            return False
        return True
    except ValueError:
        return False

def edit_pdf(input_pdf, output_pdf, patient_name, date_str):
    """
    Edita o PDF modificando o conteúdo textual
    """
    print(f"Processando o arquivo: {input_pdf}")
    
    # Abre o documento
    doc = fitz.open(input_pdf)
    
    # Obtém a primeira página
    page = doc[0]
    
    # Cria uma cópia da página para modificação
    new_doc = fitz.open()
    new_page = new_doc.new_page(width=page.rect.width, height=page.rect.height)
    
    # Copia todo o conteúdo da página original
    new_page.show_pdf_page(new_page.rect, doc, 0)
    
    # Localiza o texto do paciente existente e o substitui
    # Primeiro procuramos todos os blocos de texto
    text_blocks = page.get_text("dict")["blocks"]
    
    # Para diagnóstico, imprime todos os textos encontrados no documento
    print("\nTextos encontrados no PDF:")
    all_text = page.get_text()
    print(all_text)
    
    found_patient = False
    found_date = False
    
    # Tentativa 1: Usando a API de extração e substituição de texto
    try:
        # Busca por "Paciente:" seguido por qualquer texto
        patient_areas = page.search_for("Paciente:")
        if patient_areas:
            print(f"Encontrado 'Paciente:' na posição: {patient_areas[0]}")
            # A área encontrada contém as coordenadas do texto "Paciente:"
            # Vamos colocar o retângulo logo após isso
            rect = patient_areas[0]  # [x0, y0, x1, y1]
            
            # Estendendo o retângulo para a direita para cobrir o nome existente
            extended_rect = fitz.Rect(rect.x1, rect.y0, rect.x1 + 400, rect.y1)
            
            # Insere um retângulo branco para cobrir o texto antigo
            new_page.draw_rect(extended_rect, color=fitz.utils.getColor("white"), fill=fitz.utils.getColor("white"))
            
            # Insere o novo texto
            text_point = fitz.Point(rect.x1 + 5, rect.y0 + (rect.y1 - rect.y0) * 0.8)
            new_page.insert_text(text_point, patient_name, fontname="helv", fontsize=12)
            
            found_patient = True
            
        # Busca por "Brasília," seguido por qualquer texto
        date_areas = page.search_for("Brasília,")
        if date_areas:
            print(f"Encontrado 'Brasília,' na posição: {date_areas[0]}")
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
        print(f"Erro ao tentar a abordagem de substituição direta: {str(e)}")
    
    # Salva o documento modificado
    new_doc.save(output_pdf)
    new_doc.close()
    doc.close()
    
    if found_patient and found_date:
        print("Ambos os campos (paciente e data) foram encontrados e editados com sucesso!")
    elif found_patient:
        print("Apenas o campo do paciente foi encontrado e editado.")
    elif found_date:
        print("Apenas o campo da data foi encontrado e editado.")
    else:
        print("Nenhum dos campos foi encontrado. O arquivo foi salvo sem edições de texto.")
        
    return True

def main():
    # Nome fixo do arquivo modelo
    input_pdf = "PEDIDO COM ASS.pdf"
    
    if not os.path.exists(input_pdf):
        print(f"Arquivo modelo '{input_pdf}' não encontrado na pasta atual.")
        print("Certifique-se de que o arquivo está na mesma pasta do script.")
        return
    
    # Obter o nome do paciente
    while True:
        patient_name = input("Digite o nome do paciente: ")
        if patient_name.strip():
            # Normaliza o nome (maiúsculas, sem caracteres especiais)
            formatted_name = normalize_name(patient_name)
            print(f"Nome formatado: {formatted_name}")
            confirmation = input("O nome está correto? (s/n): ").lower()
            if confirmation in ['s', 'sim', 'y', 'yes']:
                break
        else:
            print("O nome não pode estar vazio.")
    
    # Obter a data
    while True:
        date_str = input("Digite a data do pedido (DD/MM/2025): ")
        if validate_date(date_str):
            break
        else:
            print("Data inválida. Use o formato DD/MM/2025 e certifique-se que o ano seja 2025.")
    
    # Gerar nome do arquivo de saída
    base_name = os.path.splitext(input_pdf)[0]
    output_pdf = f"{base_name}_{formatted_name}_{date_str.replace('/', '-')}.pdf"
    
    try:
        # Editar o PDF
        print(f"Editando o arquivo {input_pdf}...")
        if edit_pdf(input_pdf, output_pdf, formatted_name, date_str):
            print(f"PDF editado com sucesso! Arquivo salvo como: {output_pdf}")
    except Exception as e:
        print(f"Ocorreu um erro ao editar o PDF: {str(e)}")
        print("Dica: Verifique se todas as dependências estão instaladas:")
        print("      pip install PyMuPDF")

if __name__ == "__main__":
    main() 