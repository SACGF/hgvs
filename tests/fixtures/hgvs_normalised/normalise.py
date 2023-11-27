import csv, sys
import csv
import os
import subprocess

fasta = '/workspaces/hgvs/assemblies/hg38.fa'

def write_file_header(new_file_path, template_path):
    # Read the template file
    with open(template_path, 'r', encoding='utf-8') as template_file:
        template_content = template_file.read()

    # Write the template content to the new file
    with open(new_file_path, 'w', encoding='utf-8') as new_file:
        new_file.write(template_content)
        
def write_file_row(new_file_path, line_to_append):
    
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
    unsorted_file =  'unsorted.vcf'
    sorted_file =  'sorted.vcf'
    
    write_file_header(unsorted_file, 'header.vcf')
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
                line = f'{chr}\t{pos}\t{hgvs}\t{ref}\t{alt}\t.\t.\t.'
                print(f'Processing {i}')
                
                write_file_row(unsorted_file, line)
            else:
                print(f'Skipping {hgvs}')
               
        run_bcftools_sort(unsorted_file, sorted_file)
        run_bcftools_norm(sorted_file, output_file)
        os.remove(unsorted_file)
        os.remove(sorted_file)
                   
                
def main():
    process_csv("../hgvs_downloads/output_ensemble.csv", "normalised_ensemble.vcf")
    process_csv("../hgvs_downloads/output_variant_validator.csv", "normalised_variant_validator.vcf")

if __name__ == '__main__':
    main()
    
