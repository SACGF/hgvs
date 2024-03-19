## Validation 
The below steps were executed to investigate if the conversion from hgvs to genomic coordinates works as well using this library as using hte ensembl or variant validator REST API's

### Third Party API Differences
Using two third party API's to convert them into genomic co-ordinates
- Ensembl [rest.ensembl.org](https://rest.ensembl.org) -> [output](hgvs_downloads/output_ensemble.csv)
- Variant Validator: [rest.variantvalidator.org](https://rest.variantvalidator.org) -> [output](hgvs_downloads/output_variant_validator.csv)


- Execute the step
```bash
python download.py ../hgvs_vcf_valid.tsv output_ensemble.csv output_variant_validator.csv
```

- Both files have the same number of lines
```bash
cat output_ensemble.csv | wc -l
1955
cat output_variant_validator.csv | wc -l
1955
```

- A number of differences become apparent
```bash
diff --side-by-side --suppress-common-lines --ignore-case output_ensemble.csv output_variant_validator.csv 
```

```diff
NM_001042750.2:c.1535-12_1535-3del,True,X,124061758,TTTT      | NM_001042750.2:c.1535-12_1535-3del,True,X,124061743,CTTTTTTTT
NM_001110556.2:c.2280+266_2827-25delinsTG,True,X,1543618      | NM_001110556.2:c.2280+266_2827-25delinsTG,True,X,154361812,GG
NM_000276.4:c.2360_2361del,True,X,129588903,GTG,G             | NM_000276.4:c.2360_2361del,True,X,129588901,CTG,C
NM_005629.4:c.1141+15_1141+16dup,True,X,153693602,C,CCC       | NM_005629.4:c.1141+15_1141+16dup,True,X,153693597,A,ACC
NM_000117.3:c.284_298del,True,X,154380251,TATGAAGAGAGCTA      | NM_000117.3:c.284_298del,True,X,154380246,ACTACTATGAAGAGAG,A
NM_000276.4:c.1244+1338_1366del,True,X,129564123,CTCACCA      | NM_000276.4:c.1244+1338_1366del,True,X,129564122,GCTCACCATCAC
NM_000132.4:c.2945dup,True,X,154930845,T,TT                   | NM_000132.4:c.2945dup,True,X,154930844,A,AT
NM_005120.3:c.4618-106del,True,X,71134250,AA,A                | NM_005120.3:c.4618-106del,True,X,71134230,CA,C
NM_005391.5:c.751-267_751-266del,True,X,24527306,AAA,A        | NM_005391.5:c.751-267_751-266del,True,X,24527293,GAA,G
NM_001291867.2:c.310_345del,True,X,17376066,GCCCGCAGCCGG      | NM_001291867.2:c.310_345del,True,X,17376059,AGGCGGCGCCCGCAGCC
NM_001399.5:c.213del,True,X,69616520,AA,A                     | NM_001399.5:c.213del,True,X,69616519,GA,G
NM_004006.3:c.1306dup,True,X,32644157,C,CC                    | NM_004006.3:c.1306dup,True,X,32644156,A,AC
NM_004006.3:c.8627dup,True,X,31479024,T,TT                    | NM_004006.3:c.8627dup,True,X,31479023,C,CT
NM_000132.4:c.4825dup,True,X,154928965,T,TT                   | NM_000132.4:c.4825dup,True,X,154928964,G,GT
NM_001323289.2:c.404-135dup,True,X,18581756,T,TT              | NM_001323289.2:c.404-135dup,True,X,18581753,C,CT
NM_001099922.3:c.2369-214dup,True,X,111730181,T,TT            | NM_001099922.3:c.2369-214dup,True,X,111730177,A,AT
NM_000444.6:c.101del,True,X,22033105,GG,G                     | NM_000444.6:c.101del,True,X,22033103,TG,T
NM_000166.6:c.313del,True,X,71224019,AA,A                     | NM_000166.6:c.313del,True,X,71224016,GA,G
NM_000116.5:c.754_763del,True,X,154420711,GCTCCGGGCGG,G       | NM_000116.5:c.754_763del,True,X,154420707,AGCGGCTCCGG,A
NM_004006.3:c.10224dup,True,X,31177970,A,AA                   | NM_004006.3:c.10224dup,True,X,31177969,G,GA
NM_001034853.2:c.793_794dup,True,X,38304776,T,TGT             | NM_001034853.2:c.793_794dup,True,X,38304774,G,GGT
NM_173495.3:c.1835_1839delinsGAA,True,X,23393352,ATGTTG,      | NM_173495.3:c.1835_1839delinsGAA,True,X,23393353,TGTTG,GAA
NM_000444.6:c.1266del,True,X,22114549,TT,T                    | NM_000444.6:c.1266del,True,X,22114547,GT,G
NM_001110556.2:c.2318_2319dup,True,X,154362747,T,TTT          | NM_001110556.2:c.2318_2319dup,True,X,154362745,C,CTT
NM_005120.3:c.6348_6359dup,True,X,71141321,A,ACCAGCAGCAA      | NM_005120.3:c.6348_6359dup,True,X,71141301,A,ACAGCAACACCAG
NM_006517.5:c.855dup,True,X,74524638,C,CC                     | NM_006517.5:c.855dup,True,X,74524635,G,GC
NM_000252.3:c.1400del,True,X,150660416,TT,T                   | NM_000252.3:c.1400del,True,X,150660413,AT,A
NM_001323289.2:c.663dup,True,X,18588062,T,TT                  | NM_001323289.2:c.663dup,True,X,18588057,C,CT
NM_001110792.2:c.756dup,True,X,154031108,G,GG                 | NM_001110792.2:c.756dup,True,X,154031107,T,TG
NM_001353921.2:c.31-29709dup,True,X,63754420,T,TT             | NM_001353921.2:c.31-29709dup,False,,,,
NM_000307.5:c.1086_*3del,True,X,83509409,GACTG,G              | NM_000307.5:c.1086_*3del,True,X,83509406,TCTGA,T
NM_000061.3:c.215dup,True,X,101374561,T,TT                    | NM_000061.3:c.215dup,True,X,101374560,A,AT
NM_000166.6:c.316_320del,True,X,71224022,GCTACG,G             | NM_000166.6:c.316_320del,True,X,71224021,TGCTAC,T
NM_004006.3:c.10633_10634dup,True,X,31147439,T,TAT            | NM_004006.3:c.10633_10634dup,True,X,31147437,C,CAT
NM_000390.4:c.1153dup,True,X,85956166,G,GG                    | NM_000390.4:c.1153dup,True,X,85956165,T,TG
NM_000533.5:c.428del,True,X,103786700,GG,G                    | NM_000533.5:c.428del,True,X,103786698,TG,T
NM_000132.4:c.170_179dup,True,X,154999574,A,ATTGAATGGAA       | NM_000132.4:c.170_179dup,True,X,154999564,G,GTTGAATGGAA
NM_000390.4:c.42_47delinsGGGAA,True,X,86047485,CGTCCCT,C      | NM_000390.4:c.42_47delinsGGGAA,True,X,86047486,GTCCCT,TTCCC
NM_000444.6:c.2083del,True,X,22245344,TT,T                    | NM_000444.6:c.2083del,True,X,22245343,AT,A
NM_004586.3:c.212dup,True,X,20209319,A,AA                     | NM_004586.3:c.212dup,True,X,20209318,T,TA
NM_001184880.2:c.883_886dup,True,X,100407715,T,TCACT          | NM_001184880.2:c.883_886dup,True,X,100407711,C,CCACT
NM_001368397.1:c.1287+15_1287+26dup,True,X,12706941,T,TT      | NM_001368397.1:c.1287+15_1287+26dup,True,X,12706923,C,CTTTTTT
NM_001042351.3:c.-9+340=,False,,,,                            | NM_001042351.3:c.-9+340=,True,X,154547128,C,C
NM_001015877.2:c.27dup,True,X,134377644,A,AA                  | NM_001015877.2:c.27dup,True,X,134377638,G,GA
NM_000397.4:c.388del,True,X,37793714,CC,C                     | NM_000397.4:c.388del,True,X,37793712,GC,G
NM_001008537.3:c.926_982dup,True,X,74743631,G,GAAAGAGTAG      | NM_001008537.3:c.926_982dup,True,X,74743574,A,AAAAGAGTAGTCTTG
NM_005391.5:c.1077+12del,True,X,24531781,TT,T                 | NM_005391.5:c.1077+12del,True,X,24531778,GT,G
NM_001363.5:c.1036+6_1036+7del,True,X,154770884,GAG,G         | NM_001363.5:c.1036+6_1036+7del,True,X,154770882,AAG,A
NM_000276.4:c.40-80dup,True,X,129540664,G,GG                  | NM_000276.4:c.40-80dup,True,X,129540654,T,TG
NM_004006.3:c.9290dup,True,X,31223118,T,TT                    | NM_004006.3:c.9290dup,True,X,31223117,G,GT
NM_001079855.2:c.64del,True,X,2843268,CC,C                    | NM_001079855.2:c.64del,True,X,2843266,GC,G
NM_000052.7:c.1543+240dup,True,X,77998924,A,AA                | NM_000052.7:c.1543+240dup,True,X,77998915,T,TA
NM_000266.4:c.339dup,True,X,43949862,G,GG                     | NM_000266.4:c.339dup,True,X,43949861,T,TG
NM_000377.3:c.560-5dup,True,X,48686776,C,CC                   | NM_000377.3:c.560-5dup,True,X,48686772,T,TC
NM_002764.4:c.705-135_705-131del,True,X,107647470,TAATAT      | NM_002764.4:c.705-135_705-131del,True,X,107647467,TTATAA,T
NM_000284.4:c.1066_1074dup,True,X,19359554,G,GGATCCTGAG       | NM_000284.4:c.1066_1074dup,True,X,19359545,C,CGATCCTGAG
NM_000531.6:c.42del,True,X,38352737,TT,T                      | NM_000531.6:c.42del,True,X,38352734,CT,C
NM_000444.6:c.1996_1999del,True,X,22227536,GCAGG,G            | NM_000444.6:c.1996_1999del,True,X,22227533,AAGGC,A
NM_000444.6:c.1982_1986dup,True,X,22227527,T,TTAAAT           | NM_000444.6:c.1982_1986dup,True,X,22227522,A,ATAAAT
NM_000252.3:c.342_342+4del,True,X,150614698,AAGTAA,A          | NM_000252.3:c.342_342+4del,True,X,150614694,TGTAAA,T
NM_000117.3:c.717_718del,True,X,154381148,TCT,T               | NM_000117.3:c.717_718del,True,X,154381146,CCT,C
NM_000444.6:c.1806dup,True,X,22221650,G,GG                    | NM_000444.6:c.1806dup,True,X,22221648,T,TG
NM_000390.4:c.437_440dup,True,X,85963930,A,ACTTA              | NM_000390.4:c.437_440dup,True,X,85963926,G,GCTTA
NM_001184880.2:c.2263_2288+1dup,True,X,100403549,C,CCCTC      | NM_001184880.2:c.2263_2288+1dup,True,X,100403522,A,ACCTCTTTCC
NM_004586.3:c.1959+2dup,True,X,20161642,A,AA                  | NM_004586.3:c.1959+2dup,True,X,20161641,T,TA
NM_033380.3:c.2965_2982del,True,X,108624282,AGACCCAGGGCA      | NM_033380.3:c.2965_2982del,True,X,108624276,GCCTGGAGACCCAGGGC
NM_001167.4:c.*5519del,True,X,123912699,TT,T                  | NM_001167.4:c.*5519del,True,X,123912686,GT,G
NM_001110792.2:c.792_799dup,True,X,154031072,G,GGCTTCCTG      | NM_001110792.2:c.792_799dup,True,X,154031064,C,CGCTTCCTG
NM_000033.4:c.692_694delinsC,True,X,153725957,CGGG,CC         | NM_000033.4:c.692_694delinsC,True,X,153725958,GGG,C
NM_000052.7:c.31dup,True,X,77971672,A,AA                      | NM_000052.7:c.31dup,True,X,77971671,T,TA
NM_139058.3:c.435_461dup,True,X,25013560,G,GGCGGCGGCCGCG      | NM_139058.3:c.435_461dup,True,X,25013533,C,CGCGGCGGCCGCGGCCGC
NM_000489.6:c.663-18dup,True,X,77684611,T,TT                  | NM_000489.6:c.663-18dup,True,X,77684610,A,AT
NM_000397.4:c.674+62dup,True,X,37796203,C,CC                  | NM_000397.4:c.674+62dup,True,X,37796201,T,TC
NM_001323289.2:c.282+4del,True,X,18575493,AA,A                | NM_001323289.2:c.282+4del,True,X,18575492,TA,T
NM_004006.3:c.2614dup,True,X,32491285,T,TT                    | NM_004006.3:c.2614dup,True,X,32491284,A,AT
NM_005391.5:c.-148_-140dup,True,X,24465316,C,CTGCTGCGGC       | NM_005391.5:c.-148_-140dup,True,X,24465305,T,TGCTGCTGCG
NM_004006.3:c.8344_8359dup,True,X,31507327,T,TTCCACTTGAA      | NM_004006.3:c.8344_8359dup,True,X,31507311,C,CTCCACTTGAAGTTCA
NM_001042750.2:c.1535-15_1535-3del,True,X,124061755,TTTT      | NM_001042750.2:c.1535-15_1535-3del,True,X,124061743,CTTTTTTTT
NM_001378477.3:c.70_93del,True,X,41473537,CCGCGCTTGTCCCG      | NM_001378477.3:c.70_93del,True,X,41473528,GGCCTGCGCCCGCGCTTGT
NM_005660.3:c.747_757dup,True,X,48905162,C,CCCCACCAGAGC       | NM_005660.3:c.747_757dup,True,X,48905151,G,GCCCACCAGAGC
NM_001110792.2:c.1075_1231delinsGT,True,X,154030632,GGGT      | NM_001110792.2:c.1075_1231delinsGT,True,X,154030633,GGTCCTCGG
NM_001379110.1:c.448-9_459del,True,X,135998472,TTTTTGTCA      | NM_001379110.1:c.448-9_459del,True,X,135998465,TTTTTTTTTTTTGT
NM_001356.5:c.1635_1636insCT,True,X,41346878,T,TCT            | NM_001356.5:c.1635_1636insCT,True,X,41346877,T,TTC
NM_001184880.2:c.1172dup,True,X,100407426,T,TT                | NM_001184880.2:c.1172dup,True,X,100407425,A,AT
NM_001323289.2:c.463+269_463+273del,True,X,18582218,CTTC      | NM_001323289.2:c.463+269_463+273del,True,X,18582216,GACTTC,G
NM_006517.5:c.407dup,True,X,74422044,A,AA                     | NM_006517.5:c.407dup,True,X,74422037,G,GA
NM_000166.6:c.843_846del,True,X,71224549,CGGCC,C              | NM_000166.6:c.843_846del,True,X,71224548,TCGGC,T
NM_004187.5:c.589dup,True,X,53217211,G,GG                     | NM_004187.5:c.589dup,True,X,53217210,A,AG
NM_001008537.3:c.4248dup,True,X,74740309,A,AA                 | NM_001008537.3:c.4248dup,True,X,74740308,C,CA
NM_001099857.5:c.518+118=,False,,,,                           | NM_001099857.5:c.518+118=,True,X,154558768,G,G
NM_001291867.2:c.400del,True,X,17376156,CC,C                  | NM_001291867.2:c.400del,True,X,17376154,GC,G
NM_005120.3:c.6321_6335del,True,X,71141282,AGCAGCAGCAACA      | NM_005120.3:c.6321_6335del,True,X,71141271,ACAGCAACAGCAGCAG,A
NM_000330.4:c.26dup,True,X,18672043,A,AA                      | NM_000330.4:c.26dup,True,X,18672042,C,CA
NM_004006.3:c.8145dup,True,X,31627745,T,TT                    | NM_004006.3:c.8145dup,True,X,31627744,G,GT
NM_001291415.2:c.3426_3429del,True,X,45082774,TATCT,T         | NM_001291415.2:c.3426_3429del,True,X,45082772,CCTAT,C
NM_005032.7:c.672_673del,True,X,115634969,CTC,C               | NM_005032.7:c.672_673del,True,X,115634968,CCT,C
NM_000444.6:c.457dup,True,X,22077496,G,GG                     | NM_000444.6:c.457dup,True,X,22077495,T,TG
NM_000074.3:c.322_325del,True,X,136654405,AGAAA,A             | NM_000074.3:c.322_325del,True,X,136654399,GAAGA,G
NM_001110792.2:c.772_779delinsGTG,True,X,154031084,GATCA      | NM_001110792.2:c.772_779delinsGTG,True,X,154031085,ATCACCAT,C
NM_000531.6:c.78-102_78-99del,True,X,38367188,AGAAA,A         | NM_000531.6:c.78-102_78-99del,True,X,38367185,AAAAG,A
NM_004006.3:c.8284dup,True,X,31507387,T,TT                    | NM_004006.3:c.8284dup,True,X,31507386,A,AT
NM_005032.7:c.1263-309del,True,X,115645762,CC,C               | NM_005032.7:c.1263-309del,True,X,115645757,AC,A
NM_001184880.2:c.2581_2582delinsG,True,X,100402557,AGG,A      | NM_001184880.2:c.2581_2582delinsG,True,X,100402558,GG,C
NM_000033.4:c.900+6dup,True,X,153726172,G,GG                  | NM_000033.4:c.900+6dup,True,X,153726168,T,TG
NM_000444.6:c.978_979del,True,X,22099049,TCT,T                | NM_000444.6:c.978_979del,True,X,22099047,ACT,A
NM_000397.4:c.978del,True,X,37803956,TT,T                     | NM_000397.4:c.978del,True,X,37803952,AT,A
NM_001356.5:c.1733dup,True,X,41346976,A,AA                    | NM_001356.5:c.1733dup,True,X,41346975,C,CA
NM_019045.5:c.1054-9del,True,X,118396960,TT,T                 | NM_019045.5:c.1054-9del,True,X,118396949,GT,G
NM_000533.5:c.453+28_453+46del,True,X,103786753,ATAACAAG      | NM_000533.5:c.453+28_453+46del,True,X,103786751,CAATAACAAGGGG
NM_014271.4:c.894_903del,True,X,29917578,TTTGGGAAAGT,T        | NM_014271.4:c.894_903del,True,X,29917575,GAGTTTGGGAA,G
```

### Third Party API Failures
These items failed when attempting to look them up against the third party APIs hence were missing from the normalisation step.
The overlap suggests the variants themselves might be wrong?

- Failed the Ensembl Api
    ```
    NM_001042351.3:c.-9+340=
    NM_002764.3:c.-153delG
    NM_001099857.5:c.518+118=
    NM_001012989.3:c.350A>G
    ```

- Failed Variant Validator Api
    ```
    NM_001353921.2:c.31-29709dup
    NM_002764.3:c.-153delG
    NM_001012989.3:c.350A>G
    ```

### Normalisation

Converted the files into a VCF, sorted then normalised them using BCFTools
- [normalised_ensemble.vcf](hgvs_normalised/normalised_ensemble.vcf)
- [normalised_variant_validator.vcf](hgvs_normalised/normalised_variant_validator.vcf)

- Execute the step
```bash
python normalise.py
```
- Compare the file sizes

There is only one line difference between the two normalised files, due to one more item failing the ensembl api than the vv api
```bash
cat normalised_ensemble.vcf | grep chrX | wc -l
1951
cat normalised_variant_validator.vcf | grep chrX | wc -l
1952
```

- Compare the normalised differences
```bash
diff --side-by-side --suppress-common-lines --ignore-case normalised_ensemble.vcf normalised_variant_validator.vcf 
```

- Very minimal differences
```diff
normalised_ensemble.vcf                                         normalised_variant_validator.vcf
chrX    63754408        NM_001353921.2:c.31-29709dup    a     <
chrX    124061743       NM_001042750.2:c.1535-15_1535-3del    <
                                                              > chrX    124061743       NM_001042750.2:c.1535-15_1535-3del
                                                              > chrX    154547128       NM_001042351.3:c.-9+340=        C
                                                              > chrX    154558768       NM_001099857.5:c.518+118=       G
```
- `NM_001353921.2:c.31-29709dup` - this failed the api variant validator api lookup
- `NM_001042351.3:c.-9+340=` this failed the ensembl api lookup
- `NM_001099857.5:c.518+118=` this failed the ensembl api lookup
- `NM_001042750.2:c.1535-15_1535-3del` There appears to be a case difference but the diff command was case insensitive, not sure what else is different
