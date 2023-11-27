import csv, sys
import csv
import os
import subprocess

fasta = '/workspaces/hgvs/assemblies/hg38.fa'

def write_file(template_path, new_file_path, line_to_append):
    # Read the template file
    with open(template_path, 'r', encoding='utf-8') as template_file:
        template_content = template_file.read()

    # Write the template content to the new file
    with open(new_file_path, 'w', encoding='utf-8') as new_file:
        new_file.write(template_content)

    # Append the additional line to the new file
    with open(new_file_path, 'a', encoding='utf-8') as new_file:
        new_file.write('\n' + line_to_append)

def run_bcftools_sort(input_file, output_file):
    try:
        subprocess.run(["bcftools", "sort", "-O", "u", "-o", output_file, input_file], check=True)
        print(f"Sorting {input_file} completed successfully. Output saved to {output_file}")
    except subprocess.CalledProcessError as e:
        print(f"An error occurred: {e}")
        
def run_bcftools_norm(input_vcf, output_vcf):
    try:         
        subprocess.run(["bcftools", "norm", "-cw", "-O", "z", "-o", output_vcf, "--fasta-ref", fasta, input_vcf], check=True)
        print(f"Normalization completed successfully. Output saved to {output_vcf}")
    except subprocess.CalledProcessError as e:
        print(f"An error occurred: {e}")
        
def process_csv(input_file, output_file):
    
    with open(input_file, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        
        for i, row in enumerate(reader):
            success = row.get('Success') == 'True'
            hgvs = row.get('HGVS')
            if success: 
                chr = 'chr' + row.get('Chromosome')
                pos = row.get('Position')
                ref = row.get('Ref')
                alt = row.get('Alt')
                line = f'{chr}\t{pos}\t{hgvs}\t{ref}\t{alt}\t.\t.\t.\n'
                print(f'Processing {i}')
                
                unsorted_file = f'/tmp/temp_unsorted_{i}.vcf'
                sorted_file = f'/tmp/temp_sorted_{i}.vcf'
                
                write_file('header.vcf', unsorted_file ,line)
                
                run_bcftools_sort(unsorted_file, sorted_file)
                run_bcftools_norm(sorted_file,f'{output_file}_{i}.vcf')
                
                os.remove(unsorted_file)
                os.remove(sorted_file)
            else:
                print(f'Skipping {hgvs}')
            
                
def main():
    process_csv("../hgvs_downloads/output_ensemble.csv", "ensemble")
    process_csv("../hgvs_downloads/output_variant_validator.csv", "variant_validator")

if __name__ == '__main__':
    main()
    
