#!/bin/bash
set -e

BCFTOOLS_VERSION="1.18"

sudo apt-get update
sudo apt-get install -y wget build-essential bzip2 libz-dev liblzma-dev libbz2-dev libcurl4-openssl-dev

CURRENT_DIR=`pwd`

# Install bcftools
wget -q https://github.com/samtools/bcftools/releases/download/$BCFTOOLS_VERSION/bcftools-$BCFTOOLS_VERSION.tar.bz2
tar -vxjf bcftools-$BCFTOOLS_VERSION.tar.bz2
cd bcftools-$BCFTOOLS_VERSION
sudo make install
cd $CURRENT_DIR
rm -f bcftools-$BCFTOOLS_VERSION.tar.bz2
rm -rf bcftools-$BCFTOOLS_VERSION

# Install vcf_validator_linux
wget -q https://github.com/EBIvariation/vcf-validator/releases/download/v0.9.5/vcf_validator_linux
chmod +x vcf_validator_linux
sudo mv vcf_validator_linux /usr/local/bin