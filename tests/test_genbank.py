import pytest
from genbankparser.genbank import Genbank
import os
import json


def perform_genbank_test(
    gb,
    path,
    locus,
    length,
    definition,
    accession,
    version,
    keywords,
    comment,
    features,
    json_data,
    source = None,
    reference = None
):
    assert gb.locus == locus
    assert gb.length == length
    assert gb.definition == definition
    assert gb.accession == accession
    assert gb.version == version
    assert gb.keywords == keywords
    assert gb.comment == comment
    assert len(gb.features) == len(features)
    assert gb.features == features
    
    #测试json文件
    gb.export_features_to_json()
    base_path = os.path.splitext(path)[0]
    json_path = f"{base_path}.json"

    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f) 

    assert data == json_data

    

def test_genbank_01():
    path = os.path.join(os.path.dirname(__file__), 'noref.gb')
    gb = Genbank(path, debug=True)
    length = 1622
    locus = "NM_006141"
    definition = "Homo sapiens dynein, cytoplasmic, light intermediate polypeptide 2 (DNCLI2), mRNA."
    accession = "NM_006141"
    version = "NM_006141.1  GI:5453633"
    keywords = "."
    comment = "PROVISIONAL REFSEQ: This record has not yet been subject to final NCBI review. The reference sequence was derived from AF035812.1."
    features = {
    "UnknownLocustag": [
        {
            "type": "source",
            "location": (
                1,
                1622,
                False
            ),
            "qualifiers": {
                "organism": "Homo sapiens",
                "db_xref": "taxon:9606",
                "map": "16"
            }
        },
        {
            "type": "gene",
            "location": (
                1,
                1622,
                False
            ),
            "qualifiers": {
                "gene": "DNCLI2",
                "note": "LIC2",
                "db_xref": "LocusID:1783"
            }
        },
        {
            "type": "CDS",
            "location":(
                7,
                1485,
                False
            ),
            "qualifiers": {
                "gene": "DNCLI2",
                "note": "similar to R. norvegicus and G. gallus dynein light intermediate chain 2, Swiss-Prot Accession Numbers Q62698 and Q90828, respectively",
                "codon_start": "1",
                "db_xref": "GI:5453634",
                "product": "dynein, cytoplasmic, light intermediate polypeptide 2",
                "protein_id": "NP_006132.1",
                "translation": "MAPVGVEKKLLLGPNGPAVAAAGDLTSEEEEGQSLWSSILSEVSTRARSKLPSGKNILVFGEDGSGKTTLMTKLQGAEHGKKGRGLEYLYLSVHDEDRDDHTRCNVWILDGDLYHKGLLKFAVSAESLPETLVIFVADMSRPWTVMESLQKWASVLREHIDKMKIPPEKMRELERKFVKDFQDYMEPEEGCQGSPQRRGPLTSGSDEENVALPLGDNVLTHNLGIPVLVVCTKCDAVSVLEKEHDYRDEHLDFIQSHLRRFCLQYGAALIYTSVKEEKNLDLLYKYIVHKTYGFHFTTPALVVEKDAVFIPAGWDNEKKIAILHENFTTVKPEDAYEDFIVKPPVRKLVHDKELAAEDEQVFLMKQQSLLAKQPATPTRASESPARGPSGSPRTQGRGGPASVPSSSPGTSVKKPDPNIKNNAASEGVLASFFNSLLSKKTGSPGSPGAGGVQSTAKKSGQKTVLSNVQEELDRMTRKPDSMVTNSSTENEA"
            }
        }
    ]
    }

    json_data = {
    "UnknownLocustag": [
        {
            "type": "source",
            "location": [
                1,
                1622,
                False
            ],
            "qualifiers": {
                "organism": "Homo sapiens",
                "db_xref": "taxon:9606",
                "map": "16"
            }
        },
        {
            "type": "gene",
            "location": [
                1,
                1622,
                False
            ],
            "qualifiers": {
                "gene": "DNCLI2",
                "note": "LIC2",
                "db_xref": "LocusID:1783"
            }
        },
        {
            "type": "CDS",
            "location": [
                7,
                1485,
                False
            ],
            "qualifiers": {
                "gene": "DNCLI2",
                "note": "similar to R. norvegicus and G. gallus dynein light intermediate chain 2, Swiss-Prot Accession Numbers Q62698 and Q90828, respectively",
                "codon_start": "1",
                "db_xref": "GI:5453634",
                "product": "dynein, cytoplasmic, light intermediate polypeptide 2",
                "protein_id": "NP_006132.1",
                "translation": "MAPVGVEKKLLLGPNGPAVAAAGDLTSEEEEGQSLWSSILSEVSTRARSKLPSGKNILVFGEDGSGKTTLMTKLQGAEHGKKGRGLEYLYLSVHDEDRDDHTRCNVWILDGDLYHKGLLKFAVSAESLPETLVIFVADMSRPWTVMESLQKWASVLREHIDKMKIPPEKMRELERKFVKDFQDYMEPEEGCQGSPQRRGPLTSGSDEENVALPLGDNVLTHNLGIPVLVVCTKCDAVSVLEKEHDYRDEHLDFIQSHLRRFCLQYGAALIYTSVKEEKNLDLLYKYIVHKTYGFHFTTPALVVEKDAVFIPAGWDNEKKIAILHENFTTVKPEDAYEDFIVKPPVRKLVHDKELAAEDEQVFLMKQQSLLAKQPATPTRASESPARGPSGSPRTQGRGGPASVPSSSPGTSVKKPDPNIKNNAASEGVLASFFNSLLSKKTGSPGSPGAGGVQSTAKKSGQKTVLSNVQEELDRMTRKPDSMVTNSSTENEA"
            }
        }
    ]
    }
    perform_genbank_test(
        gb, path, locus, length, definition, accession, version, keywords, comment, features, json_data
    )
    


def test_genbank_02():
    path = os.path.join(os.path.dirname(__file__), 'empty.gb')
    gb = Genbank(path, debug=True)
    length = 0
    locus = None
    definition = None
    accession = None
    version = None
    keywords = None
    comment = None
    features = {}
    json_data = {}
    perform_genbank_test(
        gb, path, locus, length, definition, accession, version, keywords, comment, features, json_data
    )

def test_genbank_03():
    path = os.path.join(os.path.dirname(__file__), 'iro.gb')
    gb = Genbank(path, debug=True)
    length = 1326
    locus = 'IRO125195'
    definition = 'Homo sapiens mRNA full length insert cDNA clone EUROIMAGE 125195.'
    accession = 'AL109817'
    version = 'AL109817.1  GI:5731880'
    keywords = 'FLI_CDNA.'
    comment = 'EURO-IMAGE Consortium Contact: Auffray C CNRS UPR 420 - Genetique Moleculaire et Biologie du Developement IFR 1221 - Rue Guy Moquet 19, Batiment G - BP 8 94801 Villejuif  Cedex, FRANCE Tel: ++33-1-49 58 34 98 Fax: ++33-1-49 58 35 09 e-mail: auffray@infobiogen.fr This clone is available royalty-free through IMAGE Consortium Distributors. IMPORTANT: This sequence represents the full insert of this IMAGE cDNA clone. No attempt has been made to verify whether this corresponds to the full-length of the original mRNA from which it was derived.'
    features = {
    "UnknownLocustag": [
        {
            "type": "source",
            "location": (
                1,
                1326,
                False
            ),
            "qualifiers": {
                "organism": "Homo sapiens",
                "db_xref": "taxon:9606",
                "chromosome": "21",
                "clone": "IMAGE cDNA clone 125195",
                "clone_lib": "Soares fetal liver spleen 1NFLS",
                "note": "contains Alu repeat; likely to be be derived from unprocessed nuclear RNA or genomic DNA; encodes putative exons identical to FTCD; formimino transferase cyclodeaminase; formimino transferase (EC 2.1.2.5) /formimino tetrahydro folate cyclodeaminase (EC 4.3.1.4)"
            }
        },
        {
            "type": "gene",
            "location": (
                341,
                756,
                False
            ),
            "qualifiers": {
                "gene": "FTCD"
            }
        },
        {
            "type": "exon",
            "location": (
                341,
                384,
                False
            ),
            "qualifiers": {
                "gene": "FTCD",
                "number": "1"
            }
        },
        {
            "type": "intron",
            "location": (
                385,
                617,
                False
            ),
            "qualifiers": {
                "gene": "FTCD",
                "number": "1"
            }
        },
        {
            "type": "exon",
            "location": (
                618,
                756,
                False
            ),
            "qualifiers": {
                "gene": "FTCD",
                "number": "2"
            }
        }
    ]
}
    json_data = {
    "UnknownLocustag": [
        {
            "type": "source",
            "location": [
                1,
                1326,
                False
            ],
            "qualifiers": {
                "organism": "Homo sapiens",
                "db_xref": "taxon:9606",
                "chromosome": "21",
                "clone": "IMAGE cDNA clone 125195",
                "clone_lib": "Soares fetal liver spleen 1NFLS",
                "note": "contains Alu repeat; likely to be be derived from unprocessed nuclear RNA or genomic DNA; encodes putative exons identical to FTCD; formimino transferase cyclodeaminase; formimino transferase (EC 2.1.2.5) /formimino tetrahydro folate cyclodeaminase (EC 4.3.1.4)"
            }
        },
        {
            "type": "gene",
            "location": [
                341,
                756,
                False
            ],
            "qualifiers": {
                "gene": "FTCD"
            }
        },
        {
            "type": "exon",
            "location": [
                341,
                384,
                False
            ],
            "qualifiers": {
                "gene": "FTCD",
                "number": "1"
            }
        },
        {
            "type": "intron",
            "location": [
                385,
                617,
                False
            ],
            "qualifiers": {
                "gene": "FTCD",
                "number": "1"
            }
        },
        {
            "type": "exon",
            "location": [
                618,
                756,
                False
            ],
            "qualifiers": {
                "gene": "FTCD",
                "number": "2"
            }
        }
    ]
}
    perform_genbank_test(
        gb, path, locus, length, definition, accession, version, keywords, comment, features, json_data
    )

def test_genbank_04():
    path = os.path.join(os.path.dirname(__file__), 'protein_refseq.gb')
    gb = Genbank(path, debug=True)
    length = 182
    locus = 'NP_034640'
    definition = 'interferon beta, fibroblast [Mus musculus].'
    accession = 'NP_034640'
    version = 'NP_034640.1  GI:6754304'
    keywords = '.'
    comment = 'PROVISIONAL REFSEQ: This record has not yet been subject to final NCBI review. The reference sequence was derived from K00020.1.'
    features = {
    "UnknownLocustag": [
        {
            "type": "source",
            "location": (
                1,
                182,
                False
            ),
            "qualifiers": {
                "organism": "Mus musculus",
                "db_xref": "taxon:10090",
                "chromosome": "4",
                "map": "4 42.6 cM"
            }
        },
        {
            "type": "Protein",
            "location": (
                1,
                182,
                False
            ),
            "qualifiers": {
                "product": "interferon beta, fibroblast"
            }
        },
        {
            "type": "sig_peptide",
            "location": (
                1,
                21,
                False
            ),
            "qualifiers": {}
        },
        {
            "type": "Region",
            "location": (
                1,
                182,
                False
            ),
            "qualifiers": {
                "region_name": "Interferon alpha/beta domain",
                "db_xref": "CDD:pfam00143",
                "note": "interferon"
            }
        },
        {
            "type": "mat_peptide",
            "location": (
                22,
                182,
                False
            ),
            "qualifiers": {
                "product": "ifn-beta"
            }
        },
        {
            "type": "Region",
            "location": (
                56,
                170,
                False
            ),
            "qualifiers": {
                "region_name": "Interferon alpha, beta and delta.",
                "db_xref": "CDD:IFabd",
                "note": "IFabd"
            }
        },
        {
            "type": "CDS",
            "location": (
                1,
                182,
                False
            ),
            "qualifiers": {
                "gene": "Ifnb",
                "db_xref": "MGD:MGI:107657",
                "coded_by": "NM_010510.1:21..569"
            }
        }
    ]
}
    json_data = {
    "UnknownLocustag": [
        {
            "type": "source",
            "location": [
                1,
                182,
                False
            ],
            "qualifiers": {
                "organism": "Mus musculus",
                "db_xref": "taxon:10090",
                "chromosome": "4",
                "map": "4 42.6 cM"
            }
        },
        {
            "type": "Protein",
            "location": [
                1,
                182,
                False
            ],
            "qualifiers": {
                "product": "interferon beta, fibroblast"
            }
        },
        {
            "type": "sig_peptide",
            "location": [
                1,
                21,
                False
            ],
            "qualifiers": {}
        },
        {
            "type": "Region",
            "location": [
                1,
                182,
                False
            ],
            "qualifiers": {
                "region_name": "Interferon alpha/beta domain",
                "db_xref": "CDD:pfam00143",
                "note": "interferon"
            }
        },
        {
            "type": "mat_peptide",
            "location": [
                22,
                182,
                False
            ],
            "qualifiers": {
                "product": "ifn-beta"
            }
        },
        {
            "type": "Region",
            "location": [
                56,
                170,
                False
            ],
            "qualifiers": {
                "region_name": "Interferon alpha, beta and delta.",
                "db_xref": "CDD:IFabd",
                "note": "IFabd"
            }
        },
        {
            "type": "CDS",
            "location": [
                1,
                182,
                False
            ],
            "qualifiers": {
                "gene": "Ifnb",
                "db_xref": "MGD:MGI:107657",
                "coded_by": "NM_010510.1:21..569"
            }
        }
    ]
}
    perform_genbank_test(
        gb, path, locus, length, definition, accession, version, keywords, comment, features, json_data
    )
    