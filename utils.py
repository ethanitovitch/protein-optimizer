CODON_NARROWER = {
    "G": {
        "G": {
            "G": "G",
            "A": "G",
            "T": "G",
            "C": "G",
        },
        "A": {
            "G": "E",
            "A": "E",
            "T": "D",
            "C": "D",
        },
        "T": {
            "G": "V",
            "A": "V",
            "T": "V",
            "C": "V",
        },
        "C": {
            "G": "A",
            "A": "A",
            "T": "A",
            "C": "A",
        },
    },
    "A": {
        "G": {
            "G": "R",
            "A": "R",
            "T": "S",
            "C": "S",
        },
        "A": {
            "G": "K",
            "A": "K",
            "T": "N",
            "C": "N",
        },
        "T": {
            "G": "M",
            "A": "I",
            "T": "I",
            "C": "I",
        },
        "C": {
            "G": "T",
            "A": "T",
            "T": "T",
            "C": "T",
        },
    },
    "T": {
        "G": {
            "G": "W",
            "A": "STOP",
            "T": "C",
            "C": "C",
        },
        "A": {
            "G": "STOP",
            "A": "STOP",
            "T": "Y",
            "C": "Y",
        },
        "T": {
            "G": "L",
            "A": "L",
            "T": "F",
            "C": "F",
        },
        "C": {
            "G": "S",
            "A": "S",
            "T": "S",
            "C": "S",
        },
    },
    "C": {
        "G": {
            "G": "R",
            "A": "R",
            "T": "R",
            "C": "R",
        },
        "A": {
            "G": "Q",
            "A": "Q",
            "T": "H",
            "C": "H",
        },
        "T": {
            "G": "L",
            "A": "L",
            "T": "L",
            "C": "L",
        },
        "C": {
            "G": "P",
            "A": "P",
            "T": "P",
            "C": "P",
        },
    },
}

SIMILAR_AMINO_ACIDS = {
    "R": {
      "type": "positive",
      "amino_acids": ["H", "K"],
    },
    "K": {
      "type": "positive",
      "amino_acids": ["R", "H"],
    },
    "H": {
      "type": "positive",
      "amino_acids": ["R", "K"],
    },
    "D": {
      "type": "negative",
      "amino_acids": ["E"],
    },
    "E": {
      "type": "negative",
      "amino_acids": ["D"],
    },
    "S": {
      "type": "neutral",
      "amino_acids": ["T", "N", "Q"],
    },
    "T": {
      "type": "neutral",
      "amino_acids": ["S", "N", "Q"],
    },
    "N": {
      "type": "neutral",
      "amino_acids": ["S", "T", "Q"],
    },
    "Q": {
      "type": "neutral",
      "amino_acids": ["S", "T", "N"],
    },
    "C": {
      "type": "special",
      "amino_acids": [],
    },
    "G": {
      "type": "special",
      "amino_acids": [],
    },
    "P": {
      "type": "special",
      "amino_acids": [],
    },
    "A": {
        "type": "hydrophobic",
        "amino_acids": ["V", "L", "I", "M", "F", "Y", "W"],
    },
    "V": {
        "type": "hydrophobic",
        "amino_acids": ["A", "L", "I", "M", "F", "Y", "W"],
    },
    "L": {
        "type": "hydrophobic",
        "amino_acids": ["A", "V", "I", "M", "F", "Y", "W"],
    },
    "I": {
        "type": "hydrophobic",
        "amino_acids": ["A", "V", "L", "M", "F", "Y", "W"],
    },
    "M": {
        "type": "hydrophobic",
        "amino_acids": ["A", "V", "L", "I", "F", "Y", "W"],
    },
    "F": {
        "type": "hydrophobic",
        "amino_acids": ["A", "V", "L", "I", "M", "Y", "W"],
    },
    "Y": {
        "type": "hydrophobic",
        "amino_acids": ["A", "V", "L", "I", "M", "F", "W"],
    },
    "W": {
        "type": "hydrophobic",
        "amino_acids": ["A", "V", "L", "I", "M", "F", "Y"],
    },
}
AMINO_ACID_TO_CODONS = {}
for nucleotide in CODON_NARROWER:
    for nucleotide_2 in CODON_NARROWER[nucleotide]:
        for nucleotide_3 in CODON_NARROWER[nucleotide][nucleotide_2]:
            amino_acid = CODON_NARROWER[nucleotide][nucleotide_2][nucleotide_3]
            if amino_acid not in AMINO_ACID_TO_CODONS:
                AMINO_ACID_TO_CODONS[amino_acid] = []
            AMINO_ACID_TO_CODONS[amino_acid].append(nucleotide + nucleotide_2 + nucleotide_3)

def amino_acids_from_1_nucleotide(nucleotide):
    return list(set([y for x in CODON_NARROWER[nucleotide].values() for y in x.values()]))

def amino_acids_from_2_nucleotides(nucleotide_1, nucleotide_2):
    return list(set(CODON_NARROWER[nucleotide_1][nucleotide_2].values()))

def amino_acid_from_3_nucleotides(nucleotide_1, nucleotide_2, nucleotide_3):
    return CODON_NARROWER[nucleotide_1][nucleotide_2][nucleotide_3]

def codons_from_amino_acid(amino_acid):
    return AMINO_ACID_TO_CODONS[amino_acid]

def reverse_translate(protein_sequence):
    return ''.join([codons_from_amino_acid(amino_acid)[0] for amino_acid in protein_sequence])

def similar_amino_acids(amino_acid):
    return SIMILAR_AMINO_ACIDS[amino_acid]["amino_acids"]

def amino_acid_type(amino_acid):
    return SIMILAR_AMINO_ACIDS[amino_acid]["type"]