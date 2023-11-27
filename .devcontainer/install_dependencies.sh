
BCFTOOLS_VERSION="1.18"

# ensure we are not in ./devcontainer
cd /workspaces/hgvs

sudo apt-get update
sudo apt-get install -y wget build-essential bzip2 libz-dev liblzma-dev libbz2-dev libcurl4-openssl-dev

# Install bcftools
wget -q https://github.com/samtools/bcftools/releases/download/$BCFTOOLS_VERSION/bcftools-$BCFTOOLS_VERSION.tar.bz2
tar -vxjf bcftools-$BCFTOOLS_VERSION.tar.bz2
cd bcftools-$BCFTOOLS_VERSION
make DESTDIR=bin install

# Install vcf_validator_linux
wget https://github.com/EBIvariation/vcf-validator/releases/download/v0.9.5/vcf_validator_linux
chmod +x vcf_validator_linux  
