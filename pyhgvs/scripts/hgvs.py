import argparse
import logging
import os
import sys
import traceback

from pyfaidx import Fasta

import pyhgvs as hgvs
import pyhgvs.utils as hgvs_utils
from pyhgvs.models.hgvs_name import InvalidHGVSName

def process_entries(input_file: str, output_file: str, genome_file: str, transcripts_file: str, lazy: bool = False, normalize: bool = True):
    if not os.path.exists(genome_file):
        raise FileNotFoundError(f"Genome file '{genome_file}' not found.")
    
    logging.debug(f"Opening genome file: {genome_file}")
    genome = Fasta(genome_file)
    
    if not os.path.exists(transcripts_file):
        raise FileNotFoundError(f"Transcripts file '{transcripts_file}' not found.")
    
    logging.debug(f"Opening transcript file: {transcripts_file}")
    with open(transcripts_file) as tf:
        transcripts = hgvs_utils.read_transcripts(tf)

    logging.debug(f"Opening input file: {input_file}, output file: {output_file}")
    with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:    
        outfile.write(f"#lazy={lazy}\n")
        outfile.write(f"#normalize={normalize}\n")
        outfile.write("ID\tchr\tpos\tref\talt\terror\n")
 
        for line in infile:
            line = line.strip()
            try:
                hgvs_name = line
                logging.debug(f"Processing variant: {hgvs_name}")

                chr, pos, ref, alt = hgvs.parse_hgvs_name(hgvs_name=hgvs_name, genome=genome, get_transcript=lambda name: transcripts.get(name), lazy=lazy)
                outfile.write(f"{hgvs_name}\t{chr}\t{pos}\t{ref}\t{alt}\t\n")
            except InvalidHGVSName:
                logging.error(f"Invalid HGVS notation '{hgvs_name}")
                outfile.write(f"{hgvs_name}\t\t\t\t\tInvalid HGVS notation\n")
            except Exception as e:
                error_msg = traceback.format_exc()
                logging.error(f"Encountered error while processing '{hgvs_name}: {str(e)}")
                outfile.write(f"{hgvs_name}\t\t\t\t\t{str(e)}\n")

def main():
    parser = argparse.ArgumentParser(description="Process HGVS entries and generate VCF standard output")
    parser.add_argument("-i", "--input", help="Path to the input file containing HGVS entries.", required=True)
    parser.add_argument("-o", "--output", help="Path to the output file.", required=True)
    parser.add_argument("-g", "--genome", help="Genome fasta reference.", required=True)
    parser.add_argument("-t", "--transcripts", help="Transcripts information.", required=True)
    parser.add_argument("-l", "--lazy", help="Ignore transcript versioning.", action="store_true")
    parser.add_argument("-n", "--normalize", help="Normalise allele according to VCF standard.", action="store_true")
    parser.add_argument("-v", "--verbose", help="Enable verbose logging.", action="store_true")
    
    args = parser.parse_args()

    if args.verbose:
        logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s")
    else:
        logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

    logging.info(f"Input:       {args.input}")
    logging.info(f"Output:      {args.output}")
    logging.info(f"Genome:      {args.genome}")
    logging.info(f"Transcripts: {args.transcripts}")
    logging.info(f"Lazy:        {args.lazy}")
    logging.info(f"Normalise:   {args.normalize}")
    
    process_entries(args.input, args.output, args.genome, args.transcripts, args.lazy, args.normalize)

if __name__ == "__main__":
    main()
