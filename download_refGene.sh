#!/bin/sh
set -e

# Check if a command line argument is provided
if [ $# -ne 1 ]; then
    echo "Usage: $0 <-hg38|-hg38_sample>"
    exit 1
fi

# Store the parameter in a variable
parameter="$1"

# Download and index the genome based on the parameter
case "$parameter" in
    "-hg38")
        echo "Downloading Refseq (ncbiRefSeq)"
        mkdir -p reference
        docker run -e MYSQL_ALLOW_EMPTY_PASSWORD=1 --rm mysql mysql -ugenome -hgenome-euro-mysql.soe.ucsc.edu --compression-algorithms zlib -AD hg38 -BNe "SELECT r.bin,
            r.name,
            REPLACE(r.chrom, 'chr', '') AS chrom,
            r.strand,
            r.txStart,
            r.txEnd,
            r.cdsStart,
            r.cdsEnd,
            r.exonCount,
            CONVERT(r.exonStarts using utf8) AS exonStarts,
            CONVERT(r.exonEnds using utf8) AS exonEnds,
            r.score,
            r.name2,
            r.cdsStartStat,
            r.cdsEndStat,
            CONVERT(r.exonFrames using utf8) AS exonFrames
        FROM hg38.ncbiRefSeq r
        WHERE r.chrom IN ('chr1','chr2','chr3','chr4','chr5','chr6','chr7','chr8','chr9','chr10','chr11','chr12','chr13','chr14','chr15','chr16','chr17','chr18','chr19','chr20','chr21','chr22','chrX','chrY','chrM')
        ;" > reference/genes.refGene
        
        echo "Downloading Refseq (refGene)"
        docker run -e MYSQL_ALLOW_EMPTY_PASSWORD=1 --rm mysql mysql -ugenome -hgenome-euro-mysql.soe.ucsc.edu --compression-algorithms zlib -AD hg38 -BNe "WITH ncbi_names AS
        (
            SELECT DISTINCT REGEXP_REPLACE(name, '\.[0-9]+$', '') AS name 
            FROM hg38.ncbiRefSeq
        ), version_info AS (
            SELECT acc, version
            FROM hgFixed.gbCdnaInfo
            WHERE organism = 3218 -- Homo sapien
            AND type = 'mRNA'
            AND SUBSTR(acc, 1, 2) IN ('NM','NR','XM','XR')
        )
        SELECT r.bin,
            CONCAT(r.name, '.', g.version) AS name,
            REPLACE(r.chrom, 'chr', '') AS chrom,
            r.strand,
            r.txStart,
            r.txEnd,
            r.cdsStart,
            r.cdsEnd,
            r.exonCount,
            CONVERT(r.exonStarts using utf8) AS exonStarts,
            CONVERT(r.exonEnds using utf8) AS exonEnds,
            r.score,
            r.name2,
            r.cdsStartStat,
            r.cdsEndStat,
            CONVERT(r.exonFrames using utf8) AS exonFrames
        FROM hg38.refGene r, version_info g
        WHERE r.chrom IN ('chr1','chr2','chr3','chr4','chr5','chr6','chr7','chr8','chr9','chr10','chr11','chr12','chr13','chr14','chr15','chr16','chr17','chr18','chr19','chr20','chr21','chr22','chrX','chrY','chrM')
        AND r.name = g.acc
        AND r.name NOT IN (SELECT name FROM ncbi_names)
        ;" >> reference/genes.refGene

        echo Downloading LRG Refgene
        if [ ! -f reference/LRG_RefSeqGene ]; then
            mkdir -p reference
            wget -nv -c -O reference/LRG_RefSeqGene -nv -c https://ftp.ncbi.nlm.nih.gov/refseq/H_sapiens/RefSeqGene/LRG_RefSeqGene
        fi

        echo Downloading and indexing hg38
        if [ ! -f assemblies/Homo_sapiens.GRCh38.dna.primary_assembly.fa.fai ]; then
            mkdir -p assemblies
            wget -nv -c -O assemblies/Homo_sapiens.GRCh38.dna.primary_assembly.fa.gz https://ftp.ensembl.org/pub/release-110/fasta/homo_sapiens/dna/Homo_sapiens.GRCh38.dna.primary_assembly.fa.gz
            gunzip assemblies/Homo_sapiens.GRCh38.dna.primary_assembly.fa.gz
            docker run --rm -v ./assemblies:/assemblies emihat/alpine-samtools:latest samtools faidx assemblies/Homo_sapiens.GRCh38.dna.primary_assembly.fa
        fi
        ;;
    "-hg38_sample")
        echo "Downloading Refseq (ncbiRefSeq and refGene)"
        docker run -e MYSQL_ALLOW_EMPTY_PASSWORD=1 --rm mysql mysql -ugenome -hgenome-mysql.cse.ucsc.edu --compression-algorithms zlib -AD hg38 -BNe "WITH ncbi AS
        (
            SELECT r.bin,
                r.name,
                REPLACE(r.chrom, 'chr', '') AS chrom,
                r.strand,
                r.txStart,
                r.txEnd,
                r.cdsStart,
                r.cdsEnd,
                r.exonCount,
                CONVERT(r.exonStarts using utf8) AS exonStarts,
                CONVERT(r.exonEnds using utf8) AS exonEnds,
                r.score,
                r.name2,
                r.cdsStartStat,
                r.cdsEndStat,
                r.exonFrames
            FROM hg38.ncbiRefSeq r
           WHERE r.chrom IN ('chrX','chrY')
        ), refGene AS (
            SELECT r.bin,
                CONCAT(r.name, '.', g.version) AS name,
                REPLACE(r.chrom, 'chr', '') AS chrom,
                r.strand,
                r.txStart,
                r.txEnd,
                r.cdsStart,
                r.cdsEnd,
                r.exonCount,
                CONVERT(r.exonStarts using utf8) AS exonStarts,
                CONVERT(r.exonEnds using utf8) AS exonEnds,
                r.score,
                r.name2,
                r.cdsStartStat,
                r.cdsEndStat,
                r.exonFrames
            FROM hg38.refGene r, hgFixed.gbCdnaInfo g
            WHERE r.chrom IN ('chrX','chrY')
            AND r.name = g.acc
        )
        SELECT *
        FROM ncbi
        UNION ALL
        SELECT *
        FROM refGene 
        WHERE REGEXP_REPLACE(name, '\.[0-9]+$', '') NOT IN (SELECT REGEXP_REPLACE(name, '\.[0-9]+$', '')
                                                            FROM ncbi)
        ;" > tests/fixtures/genes.refGene

        echo Downloading LRG Refgene
        if [ ! -f tests/fixtures/LRG_RefSeqGene ]; then
            wget -nv -c -O tests/fixtures/LRG_RefSeqGene -nv -c https://ftp.ncbi.nlm.nih.gov/refseq/H_sapiens/RefSeqGene/LRG_RefSeqGene
        fi

        echo Downloading and indexing hg38 \(chrX\) and \(chrY\)
        if [ ! -f tests/fixtures/Homo_sapiens.GRCh38.dna.chromosome.X.Y.fa.fai ]; then
            wget -nv -c -O tests/fixtures/Homo_sapiens.GRCh38.dna.chromosome.X.fa.gz https://ftp.ensembl.org/pub/release-110/fasta/homo_sapiens/dna/Homo_sapiens.GRCh38.dna.chromosome.X.fa.gz
            wget -nv -c -O tests/fixtures/Homo_sapiens.GRCh38.dna.chromosome.Y.fa.gz https://ftp.ensembl.org/pub/release-110/fasta/homo_sapiens/dna/Homo_sapiens.GRCh38.dna.chromosome.Y.fa.gz
            gunzip tests/fixtures/Homo_sapiens.GRCh38.dna.chromosome.X.fa.gz
            gunzip tests/fixtures/Homo_sapiens.GRCh38.dna.chromosome.Y.fa.gz
            cat tests/fixtures/Homo_sapiens.GRCh38.dna.chromosome.X.fa > tests/fixtures/Homo_sapiens.GRCh38.dna.chromosome.X.Y.fa
            cat tests/fixtures/Homo_sapiens.GRCh38.dna.chromosome.Y.fa >> tests/fixtures/Homo_sapiens.GRCh38.dna.chromosome.X.Y.fa
            rm tests/fixtures/Homo_sapiens.GRCh38.dna.chromosome.X.fa
            rm tests/fixtures/Homo_sapiens.GRCh38.dna.chromosome.Y.fa
            docker run --rm -v ./tests/fixtures:/assemblies emihat/alpine-samtools:latest samtools faidx assemblies/Homo_sapiens.GRCh38.dna.chromosome.X.Y.fa
        fi
        ;;
    *)
        echo "Unknown parameter: $parameter"
        exit 1
        ;;
esac

echo "Done"
