import csv
import unicodedata
from fuzzywuzzy import fuzz

def normalize(text):
    return unicodedata.normalize("NFC", text)

def similarity(a, b):
    
    return fuzz.token_set_ratio(a, b) / 100.0

def tokenize_name(name):
    
    tokens = name.split()
    initials = [token[0] for token in tokens if token]  
    return tokens + initials

def compare_names(name1, name2):
    
    tokens1 = set(tokenize_name(name1))
    tokens2 = set(tokenize_name(name2))
    return similarity(tokens1, tokens2)

def extract_domain(email):
   
    return email.split('@')[-1].split('.')[0]  

def remove_duplicates(input_file, output_file):
    seen = set()
    output_data = []

    with open(input_file, 'r', encoding='utf-8-sig') as infile:  
        reader = csv.DictReader(infile)
        for row in reader:
            
            name = normalize(row['Name']).strip().lower()
            email = normalize(row['Email']).strip().lower()
            phone = normalize(row['Phone Number']).strip().lower()
            key = (name, email, phone)
            
            
            duplicate_found = False
            for seen_key in seen:
                name_similarity = compare_names(name, seen_key[0])
                email_similarity = similarity(email, seen_key[1])
                phone_similarity = similarity(phone, seen_key[2])
                
                if (name_similarity > 0.8 and email_similarity > 0.6 and 
                    phone_similarity > 0.8):
                    duplicate_found = True
                    break
            
            if not duplicate_found:
                output_data.append(row)
                seen.add(key)

    with open(output_file, 'w', encoding='utf-8', newline='') as outfile:  
        writer = csv.DictWriter(outfile, fieldnames=output_data[0].keys())
        writer.writeheader()
        writer.writerows(output_data)

if __name__ == "__main__":
    input_file = "input_data_2.csv"
    output_file = "output_data.csv"
    remove_duplicates(input_file, output_file)




    






