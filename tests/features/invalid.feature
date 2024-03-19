Feature: HGVS to VCF Conversion
    I want to convert HGVS names to VCF format
    So that I can use them in genomic analyses

    Scenario Outline: Invalid HGVS Conversion
        Given a HGVS name <hgvs_name>
        When the HGVS name conversion is attempted
        Then request is unsuccessful
        And error message <message> is returned

        Examples:
            | hgvs_name                      | message                                            |
            | NM_031206.7:c.1788TGATGAAGA[1] | Invalid HGVS Name:'NM_031206.7:c.1788TGATGAAGA[1]' |
            | NM_001110556.4:c.3396G>T       | transcript is required                             |