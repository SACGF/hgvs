import csv, sys
import requests
from requests.adapters import HTTPAdapter, Retry

import csv
import time
from functools import wraps

def retry(num_attempts, delay_seconds):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            attempts = 0
            while attempts < num_attempts:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    attempts += 1
                    if attempts == num_attempts:
                        raise
                    print(f"Attempt {attempts} failed, retrying in {delay_seconds} seconds...")
                    time.sleep(delay_seconds)
        return wrapper
    return decorator

def read_tsv(file_path):
    rows = []
    with open(file_path, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file, delimiter='\t')
        for row in reader:
            rows.append(row)
    return rows

@retry(num_attempts=3, delay_seconds=2)
def call_http(server, url):
    timeout = 90
    s = requests.Session()

    retries = Retry(total=10,
                    backoff_factor=0.1,
                    status_forcelist=[ 500, 501, 502, 503, 504 ])

    s.mount('https://', HTTPAdapter(max_retries=retries))

    response = s.get(server+url, headers={"Content-Type":"application/json"}, timeout=timeout)
    return response

def get_translation_variant_validator(hgvs_c):
    print (f"\tChecking variant validator")
    server = "https://rest.variantvalidator.org"
    url = "/VariantValidator/variantvalidator/GRCh38/{}/select".format(hgvs_c)

    try:
        response = call_http(server, url)
        if not response.ok:
            return hgvs_c, False, None, None, None, None

        json = response.json()
        hg38_data = json[hgvs_c]["primary_assembly_loci"]["hg38"]["vcf"]

        chromosome = hg38_data.get("chr").replace("chr", "")
        position =  int(hg38_data.get("pos"))
        reference = hg38_data.get("ref")
        alternate = hg38_data.get("alt")
        print (f"\t\tFound {chromosome}:{position}:{reference}:{alternate}")

        return hgvs_c, True, chromosome, int(position), reference, alternate
    except KeyError:
        print (f"\t\t'Key Error for {hgvs_c}")
        return hgvs_c, False, None, None, None, None
    except Exception as e:
        print (f"\t\t'Error for {hgvs_c} {e}")
        return hgvs_c, False, None, None, None, None


def get_translation_ensembl(hgvs_c):
    print (f"\tChecking ensembl")
    server = "https://rest.ensembl.org"
    url = "/variant_recoder/human/{}?fields=None&vcf_string=1".format(hgvs_c)
   
    try:
        response = call_http(server, url)
        if not response.ok:
            return hgvs_c, False, None, None, None, None

        json = response.json()

        # Find the entry for the X chromosome
        for entry in json:
            key = list(entry.keys())[0]
            for item in entry[key]['vcf_string']:
                chromosome, position, reference, alternate = item.split("-")
                if chromosome == "X":
                    print (f"\t\tFound {chromosome}:{position}:{reference}:{alternate}")
                    return hgvs_c, True, chromosome, int(position), reference, alternate
                else:
                    print (f"\t\tIgnoring {chromosome}:{position}:{reference}:{alternate}")

        print (f"None found")
        return hgvs_c, False, None, None, None, None
    except Exception as e:
        print (f"\t\t'Error for {hgvs_c} {e}")
        return hgvs_c, False, None, None, None, None


if __name__ == "__main__":
    print("Running")
    if len(sys.argv) != 4:
        print("Usage: python download.py <input_file> <ensembl_output_file> <variant_validator_output_file>")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file1 = sys.argv[2]
    output_file2 = sys.argv[3]
    print(f"Reading {input_file}")
    data = read_tsv(input_file)
    position=1
    total = len(data)
    print(f"Found {total} variants")
    
    hgvs_column_name = "hgvs_c"

    results = []
    # write file header, overwriting the existing file
    with open(output_file1, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file, delimiter=',')
        writer.writerow(["HGVS", "Success", "Chromosome", "Position", "Ref", "Alt"])
    with open(output_file2, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file, delimiter=',')
        writer.writerow(["HGVS", "Success", "Chromosome", "Position", "Ref", "Alt"])

    # Lookup both APIs for each row and save the results
    for row in data:
        hgvs_c = row.get(hgvs_column_name)
        
        print(f"Progress {position}/{total}")
        
        # Lookup ensebl, write row, appending the existing file
        result1 = get_translation_ensembl(hgvs_c)
        with open(output_file1, 'a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file, delimiter=',')
            writer.writerow(result1)
            
        # Lookup variant validator, write row, appending the existing file        
        result2 = get_translation_variant_validator(hgvs_c)
        with open(output_file2, 'a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file, delimiter=',')
            writer.writerow(result2)

        position = position + 1
        
        
        
        




