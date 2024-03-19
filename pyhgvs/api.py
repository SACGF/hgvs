from __future__ import print_function
from __future__ import unicode_literals

import os
from pathlib import Path
import logging
import traceback

from fastapi import FastAPI, HTTPException, Request
from typing import Tuple,List
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from pyfaidx import Fasta
import logging.config
from pydantic import BaseModel

import pyhgvs as hgvs
from pyhgvs.models.hgvs_name import InvalidHGVSName
import pyhgvs.utils as hgvs_utils

logging.config.fileConfig('pyhgvs/logging.conf', disable_existing_loggers=False)
logger = logging.getLogger(__name__)

app = FastAPI()

# Read genome sequence using pyfaidx.
file=os.getenv('FASTA')
if file is None:
    raise Exception(f"FASTA env var not set.")

logger.info('Loading FASTA: %s',file)
if not os.path.exists(file):
    raise Exception(f"FASTA file: {file} not found. Please check if file exists")

genome = Fasta(file)

# Read RefSeq transcripts into a python dict.

refgene=os.getenv('REFGENE')
if refgene is None:
    raise Exception(f"REFGENE env var not set.")

logger.info('Loading REFGENE: %s',refgene)
if not os.path.exists(refgene):
    raise Exception(f"REFGENE file: {refgene} not found. Please check if file exists")

with open(refgene) as infile:
    transcripts = hgvs_utils.read_transcripts(infile)

class VCFVariant(BaseModel):
    input: str
    chr: str | None
    pos: int | None
    ref: str | None
    alt: str | None
    message: str | None
    
class HgvsSingleVariantRequest(BaseModel):
    input: str
    normalise: bool | None = False
    ignore_version: bool | None = False
    indels_start_with_same_base: bool | None = False
    prioritise_X_over_Y: bool | None = False

class HgvsSingleVariantResponse(BaseModel):
    response: VCFVariant

class HgvsMultipleVariantRequest(BaseModel):
    input: list[str]
    normalise: bool | None = False
    ignore_version: bool | None = False
    indels_start_with_same_base: bool | None = False
    prioritise_X_over_Y: bool | None = False

class HgvsMultipleVariantResponse(BaseModel):
    response: list[VCFVariant]

# Provide a callback for fetching a transcript by its name.
def get_transcript(name):
    tx = transcripts.get(name)

    if tx is not None:
        if len(tx) != 1:
            raise RuntimeError(f"Multiple loci: {', '.join(list(tx.keys()))} found for transcript: {name}")
        
        return tx[next(iter(tx))]
    else:
        return None

# Provide a callback for fetching a transcript by its name.
def get_transcript_X_over_Y(name):
    tx = transcripts.get(name)

    if tx is not None:
        # Check if both keys 'X' and 'Y' are in the dictionary
        if 'X' in tx and 'Y' in tx:
            return tx['X']

        if len(tx) != 1:
            raise RuntimeError(f"Multiple loci: {', '.join(list(tx.keys()))} found for transcript: {name}")
        
        return tx[next(iter(tx))]
    else:
        return None

@app.get("/")
def get_root():
    return {"App": "HGVS Translator"}

@app.get("/health/alive")
def get_alive():
    return {"status": "alive"}

@app.get("/health/ready")
def get_ready():
    return {"status": "ready"}

class DefaultException(Exception):
    def __init__(self, status_code: int, detail: str):
        self.status_code = status_code
        self.detail = detail

@app.exception_handler(DefaultException)
async def unicorn_exception_handler(request: Request, exc: DefaultException):
    return JSONResponse(
        status_code=exc.status_code,
        content={'error': exc.detail},
    )

@app.post("/translate", response_model=HgvsSingleVariantResponse)
async def translate_hgvs(request: HgvsSingleVariantRequest):
    logger.info('Translating %s', request.input)
    get_transcript_fun = get_transcript_X_over_Y if request.prioritise_X_over_Y else get_transcript
    try:
        chrom, offset, ref, alt = hgvs.parse_hgvs_name(hgvs_name=request.input, 
                                                       genome=genome, 
                                                       get_transcript=get_transcript_fun,
                                                       lazy=request.ignore_version,
                                                       normalize=request.normalise,
                                                       indels_start_with_same_base=request.indels_start_with_same_base)
        logger.info('Translated %s to: %s %s %s %s', request.input, chrom, offset, ref, alt)
        return HgvsSingleVariantResponse(response=VCFVariant(input=request.input, chr=chrom, pos=offset, ref=ref, alt=alt, message=None))

    except InvalidHGVSName as e:
        logging.error(f"Invalid HGVS Name:'{request.input}'")
        raise HTTPException(status_code=400, detail=jsonable_encoder(
            {'error': {'summary':f"Invalid HGVS Name:'{request.input}'",
                       'details': None}}))
    except ValueError as e:
        logging.error(e)
        raise HTTPException(status_code=400, detail=jsonable_encoder(
            {'error': {'summary': str(e),
                       'details': None}}))
    except Exception as e:
        logger.error(e)
        traceback.print_exc()
        raise DefaultException(status_code=500, detail=jsonable_encoder(
            {'error': {'summary':'Unknown error occurred',
                       'details': str(e)}}))

@app.post("/translate_bulk", response_model=HgvsMultipleVariantResponse)
def translate_hgvs_bulk(request: HgvsMultipleVariantRequest):
    vcf_variants_list = []
    logger.info('Translating %s values', {len(request.input)})
    get_transcript_fun = get_transcript_X_over_Y if request.prioritise_X_over_Y else get_transcript
    try:
        for input in request.input:
            try:
                chrom, offset, ref, alt = hgvs.parse_hgvs_name(hgvs_name=input, 
                                                               genome=genome, 
                                                               get_transcript=get_transcript_fun,
                                                               lazy=request.ignore_version,
                                                               normalize=request.normalise,
                                                               indels_start_with_same_base=request.indels_start_with_same_base)
                vcf_variant = VCFVariant(input=input, chr=chrom, pos=offset, ref=ref, alt=alt, message=None)
                
            except InvalidHGVSName as e:
                logging.error(f"Invalid HGVS Name:'{input}'")
                vcf_variant = VCFVariant(input=input, chr=None, pos=None, ref=None, alt=None, message=f"Invalid HGVS Name:'{input}'")
            
            vcf_variants_list.append(vcf_variant)
        return HgvsMultipleVariantResponse(response=vcf_variants_list)
    except ValueError as e:
        logging.error(e)
        raise HTTPException(status_code=400, detail=jsonable_encoder(
            {'error': {'summary': str(e),
                       'details': None}}))
    except Exception as e:
        logger.error(e)
        traceback.print_exc()
        raise DefaultException(status_code=500, detail=jsonable_encoder(
            {'error': {'summary':'Unknown error occurred',
                       'details': str(e)}}))
    
if __name__ == '__main__':
    app.run(debug=True)