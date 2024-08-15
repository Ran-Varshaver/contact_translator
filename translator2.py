import vobject
import requests
import json

file_path = 'C:/Users/User/Documents/contactsHE.vcf'
translation_url = 'https://dal.walla.co.il/translator?from=translate.walla.co.il'
output_vcf_path = 'C:/Users/User/Documents/contactsEN.vcf'
output_txt_path = 'C:/Users/User/Documents/contactsEN.txt'

def extract_names_from_vcf(file_path):
    with open(file_path, 'r', encoding='utf-8') as vcf_file:
        contacts = vobject.readComponents(vcf_file)
        names = [contact for contact in contacts if hasattr(contact, 'fn')]
    return names

def is_hebrew(text):
    return any('\u0590' <= char <= '\u05FF' for char in text)

def translate_name(name):
    if is_hebrew(name):
        data = {
            'from': 'he',
            'to': 'en',
            't': name
        }
        response = requests.post(translation_url, json=data)
        if response.status_code == 200:
            try:
                result = response.json()
                return result['data']['res']
            except (KeyError, json.JSONDecodeError):
                return name
        else:
            return name
    return name

def process_batch(names_batch):
    return [translate_name(name) for name in names_batch]

def write_to_vcf(original_contacts, translations):
    with open(output_vcf_path, 'w', encoding='utf-8') as vcf_file:
        for contact in original_contacts:
            if hasattr(contact, 'fn'):
                original_name = contact.fn.value
                translated_name = translations.get(original_name, original_name)
                contact.fn.value = translated_name
                vcf_file.write(contact.serialize())
                
def write_to_txt(names, translations):
    with open(output_txt_path, 'w', encoding='utf-8') as txt_file:
        for original, translated in zip(names, translations):
            txt_file.write(f"{original} -> {translated}\n")

def main():
    print("Starting script")
    original_contacts = extract_names_from_vcf(file_path)
    
    names = [contact.fn.value for contact in original_contacts if hasattr(contact, 'fn')]
    
    batch_size = 10
    translations = {}
    
    for i in range(0, len(names), batch_size):
        batch = names[i:i+batch_size]
        print(f"Processing batch {i // batch_size + 1}")
        batch_translations = process_batch(batch)
        for name, translated in zip(batch, batch_translations):
            translations[name] = translated
    
    print("Writing results to VCF and TXT files")
    write_to_vcf(original_contacts, translations)
    write_to_txt(names, [translations.get(name, name) for name in names])
    
    print("Script completed")

main()
