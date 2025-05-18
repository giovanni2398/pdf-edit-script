#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re
from datetime import datetime
from PyPDF2 import PdfReader, PdfWriter
from PyPDF2.generic import DecodedStreamObject, NameObject, createStringObject
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

def edit_pdf_text(input_pdf, output_pdf, patient_name, date_str):
    """
    Edita o PDF substituindo o nome do paciente e a data
    """
    reader = PdfReader(input_pdf)
    writer = PdfWriter()
    
    # Processar a única página do PDF
    page = reader.pages[0]
    contents = page['/Contents'].get_object()
    
    # Se o conteúdo for um array, precisamos processar cada item
    if isinstance(contents, list):
        for i in range(len(contents)):
            if isinstance(contents[i], DecodedStreamObject):
                content_data = contents[i].get_data().decode('utf-8')
                
                # Substitui o nome do paciente
                content_data = re.sub(r'Paciente: [^\n\r]*', f'Paciente: {patient_name}', content_data)
                
                # Substitui a data
                content_data = re.sub(r'Data: [^\n\r]*', f'Data: {date_str}', content_data)
                
                # Atualiza o conteúdo
                contents[i] = DecodedStreamObject()
                contents[i].set_data(content_data.encode('utf-8'))
    else:
        content_data = contents.get_data().decode('utf-8')
        
        # Substitui o nome do paciente
        content_data = re.sub(r'Paciente: [^\n\r]*', f'Paciente: {patient_name}', content_data)
        
        # Substitui a data
        content_data = re.sub(r'Data: [^\n\r]*', f'Data: {date_str}', content_data)
        
        # Atualiza o conteúdo
        new_content = DecodedStreamObject()
        new_content.set_data(content_data.encode('utf-8'))
        page[NameObject('/Contents')] = new_content
    
    writer.add_page(page)
    
    # Salva o PDF modificado
    with open(output_pdf, 'wb') as out_file:
        writer.write(out_file)

def main():
    # Verificar se existem arquivos PDF na pasta atual
    pdf_files = [f for f in os.listdir('.') if f.endswith('.pdf') and f != 'output.pdf']
    
    if not pdf_files:
        print("Nenhum arquivo PDF encontrado na pasta atual.")
        print("Por favor, coloque o arquivo modelo de pedido médico na pasta do projeto.")
        return
    
    # Se houver mais de um PDF, permite ao usuário escolher
    if len(pdf_files) > 1:
        print("Vários arquivos PDF encontrados. Escolha um pelo número:")
        for i, file in enumerate(pdf_files, 1):
            print(f"{i}. {file}")
        
        while True:
            try:
                choice = int(input("Digite o número do arquivo: "))
                if 1 <= choice <= len(pdf_files):
                    input_pdf = pdf_files[choice-1]
                    break
                else:
                    print("Número inválido. Tente novamente.")
            except ValueError:
                print("Por favor, digite um número válido.")
    else:
        input_pdf = pdf_files[0]
    
    # Obter o nome do paciente
    while True:
        patient_name = input("Digite o nome do paciente: ")
        if patient_name.strip():
            # Normaliza o nome (maiúsculas, sem caracteres especiais)
            formatted_name = normalize_name(patient_name)
            print(f"Nome formatado: {formatted_name}")
            confirmation = input("O nome está correto? (s/n): ").lower()
            if confirmation == 's' or confirmation == 'sim':
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
    output_pdf = f"{base_name}_editado_{datetime.now().strftime('%Y%m%d%H%M%S')}.pdf"
    
    try:
        # Editar o PDF
        print(f"Editando o arquivo {input_pdf}...")
        edit_pdf_text(input_pdf, output_pdf, formatted_name, date_str)
        print(f"PDF editado com sucesso! Arquivo salvo como: {output_pdf}")
    except Exception as e:
        print(f"Ocorreu um erro ao editar o PDF: {str(e)}")

if __name__ == "__main__":
    main() 