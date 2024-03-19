#!/bin/bash
nohup python -u download.py ../hgvs_vcf_valid.tsv output_ensemble.csv output_variant_validator.csv > output.log 2>&1 &