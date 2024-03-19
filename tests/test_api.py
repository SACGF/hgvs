import json
import logging
import csv
import os
import sys

import pytest
from pytest_bdd import scenario, given, scenarios, when, then, parsers
from pyfaidx import Fasta

current_dir = os.path.dirname(os.path.abspath(__file__))
target_folder_path = os.path.join(current_dir, "..")
sys.path.append(target_folder_path)

import pyhgvs as hgvs
import pyhgvs.utils as hgvs_utils
from pyhgvs.models.hgvs_name import InvalidHGVSName

logging.basicConfig(level=logging.DEBUG)

@scenario('features/valid.feature', 'Valid HGVS Conversion')
def test_valid_hgvs_conversion():
    pass

@scenario('features/invalid.feature', 'Invalid HGVS Conversion')
def test_invalid_hgvs_conversion():
    pass

@given(parsers.parse('a HGVS name {hgvs_name}'), target_fixture='hgvs_name')
def hgvs_name(hgvs_name):
    return hgvs_name

@pytest.fixture
def genome():
    file=os.getenv('FASTA')
    logging.info(f"Loading fasta: {file}")

    if not os.path.exists(file):
        raise Exception(f"Fasta file: {file} not found. Please check if file exists or FASTA environment variable has been defined")

    return Fasta(file)

@pytest.fixture
def transcripts():
    refgene=os.getenv('REFGENE')
    logging.info(f"Refgene: {refgene}")

    if not os.path.exists(refgene):
        raise Exception(f"Refgene file: {refgene} not found. Please check if file exists or REFGENE environment variable has been defined")

    with open(refgene) as infile:
        transcripts = hgvs_utils.read_transcripts(infile)
    return lambda name: transcripts.get(name)

@when('the HGVS name is converted to VCF')
def convert_hgvs_to_vcf(client, hgvs_name):
    pytest.response1 = client.post(f"/translate", json={'input': hgvs_name, 'ignore_version': True, 'normalise': True, 'prioritise_X_over_Y': True})
    assert pytest.response1.status_code == 200, f"HTTP status code: {pytest.response1.status_code}"

    pytest.response2 = client.post(f"/translate", json={'input': hgvs_name, 'ignore_version': True, 'normalise': False, 'prioritise_X_over_Y': True})
    assert pytest.response2.status_code == 200, f"HTTP status code: {pytest.response2.status_code}"

    pytest.response3 = client.post(f"/translate", json={'input': hgvs_name, 'ignore_version': True, 'indels_start_with_same_base': False, 'prioritise_X_over_Y': True})
    assert pytest.response3.status_code == 200, f"HTTP status code: {pytest.response3.status_code}"

@when('the HGVS name conversion is attempted')
def convert_hgvs_to_vcf(client, hgvs_name):
    pytest.response = client.post(f"/translate", json={'input': hgvs_name})

def extract_chr_pos_ref_alt(response):
    response_json = json.loads(response.content)

    return response_json['response']['input'], response_json['response']['chr'], response_json['response']['pos'], response_json['response']['ref'], response_json['response']['alt'], response_json['response']['message']

@then(parsers.parse('the VCF representation should match {chr}, {pos:d}, {ref}, {alt}, and {message}'))
def vcf_representation_matches(hgvs_name, chr, pos, ref, alt, message):
    # Assertion logic here
    input1, chr1, pos1, ref1, alt1, message1 = extract_chr_pos_ref_alt(pytest.response1)
    input2, chr2, pos2, ref2, alt2, message2 = extract_chr_pos_ref_alt(pytest.response2)
    input3, chr3, pos3, ref3, alt3, message3 = extract_chr_pos_ref_alt(pytest.response3)

    if message == 'None':
        message = None

    scenario1 = (input1 == hgvs_name) and (chr1 == chr) and (pos1 == pos) and (ref1 == ref) and (alt1 == alt) and (message is None)
    scenario2 = (input2 == hgvs_name) and (chr2 == chr) and (pos2 == pos) and (ref2 == ref) and (alt2 == alt) and (message is None)
    scenario3 = (input3 == hgvs_name) and (chr3 == chr) and (pos3 == pos) and (ref3 == ref) and (alt3 == alt) and (message is None)

    scenario1_status = 'match' if scenario1 else 'non-match'
    scenario2_status = 'match' if scenario2 else 'non-match'
    scenario3_status = 'match' if scenario3 else 'non-match'

    parsed_values = f"\n  Normalised: [{scenario1_status}] {chr1}-{pos1}-{ref1}-{alt1}\n  Non-normalised: [{scenario2_status}] {chr2}-{pos2}-{ref2}-{alt2}\n  Indel-not same base start: [{scenario3_status}] {chr3}-{pos3}-{ref3}-{alt3}"

    assert scenario1 or scenario2 or scenario3, f"Input: {hgvs_name}, Expected: {chr}-{pos}-{ref}-{alt}{parsed_values}"

@then('request is unsuccessful')
def request_unsuccessful():
    assert pytest.response.status_code != 200

@then(parsers.parse('error message {message} is returned'))
def error_message(message):
    response_json = json.loads(pytest.response.content)
    
    assert response_json['detail']['error']['summary'] == message, f"Expected: {message}, but actual is {response_json['detail']['error']['summary']}"

@then(parsers.parse('{chr}, {pos}, {ref}, and {alt} are empty'))
def chr_pos_ref_alt_empty(chr, pos, ref, alt):
    input, chr, pos, ref, alt, message = extract_chr_pos_ref_alt(pytest.response)
    
    chr = None if chr == 'None' else chr
    pos = None if pos == 'None' else pos
    ref = None if ref == 'None' else ref
    alt = None if alt == 'None' else alt

    assert chr == None and pos == None and ref == None and alt == None, f"Expected chr, pos, ref and alt to all be Null, but they are {chr}-{pos}-{ref}-{alt}"