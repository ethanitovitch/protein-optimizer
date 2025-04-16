import argparse
from functools import lru_cache
from utils import amino_acids_from_1_nucleotide, amino_acids_from_2_nucleotides, amino_acid_from_3_nucleotides, codons_from_amino_acid, similar_amino_acids, amino_acid_type

def get_overlapping_indices(gene_a_start, gene_b_start):
    if gene_a_start < gene_b_start:
        return (gene_a_start + (gene_b_start - gene_a_start) // 3 * 3), gene_b_start
    else:
        return gene_a_start, gene_b_start + (gene_a_start - gene_b_start) // 3 * 3

def compare_codons(codon_a, codon_b, constraints_a, constraints_b, offset):
    if offset < 0:
        has_match = codon_a[:3 - -1*offset] == codon_b[-1*offset:]
        if constraints_b is None:
            return has_match
        else:
            return constraints_b == codon_b[:-1 * offset] and has_match
    else:
        has_match = codon_a[offset:] == codon_b[:3-offset]
        if constraints_a is None:
            return has_match
        else:
            return constraints_a == codon_a[:offset] and has_match

def get_next_constraints(codon_a, codon_b, offset):
    if offset < 0:
        return None, codon_a[3 - -1*offset:]
    else:
        return codon_b[3 - offset:], None

def amino_acid_from_nucleotides(nucleotides):
    if len(nucleotides) == 1:
        return amino_acids_from_1_nucleotide(nucleotides[0])
    elif len(nucleotides) == 2:
        return amino_acids_from_2_nucleotides(nucleotides[0], nucleotides[1])
    elif len(nucleotides) == 3:
        return amino_acid_from_3_nucleotides(nucleotides[0], nucleotides[1], nucleotides[2])
    else:
        raise ValueError("Invalid number of nucleotides")
    
def codon_options_from_nucleotides(codon):
    return codons_from_amino_acid(amino_acid_from_nucleotides(codon))
        

@lru_cache(maxsize=None)
def optimize_recursive(gene_a, gene_b, constraints_a, constraints_b, offset, similar_enabled=True):
    print("-"*100)
    print(f"gene_a: {gene_a}\n\ngene_b: {gene_b}\n\noffset: {offset}\n\nconstraints_a: {constraints_a}\n\nconstraints_b: {constraints_b}")
    if len(gene_a) == 0 and len(gene_b) == 0:
        return "", 0, [], 0
    elif len(gene_a) == 0:
        return gene_b, 0, [], 0
    elif len(gene_b) == 0:
        return gene_a, 0, [], 0
    
    nucleotides_a = gene_a[:3]
    nucleotides_b = gene_b[:3]
    codons_a = codon_options_from_nucleotides(nucleotides_a)
    codons_b = codon_options_from_nucleotides(nucleotides_b)
    print(f"codons_a: {codons_a}\n\ncodons_b: {codons_b}")
    sequences = []
    for codon_a in codons_a:
        found_match = False
        for codon_b in codons_b:
            if compare_codons(codon_a, codon_b, constraints_a, constraints_b, offset):
                print(f"found match: {codon_a} == {codon_b} with offset {offset}")
                constraints_a, constraints_b = get_next_constraints(codon_a, codon_b, offset)
                sequence, errors, similar_switch, index = optimize_recursive(gene_a[3:], gene_b[3:], constraints_a, constraints_b, offset, similar_enabled)
                if len(gene_a[3:]) == 0 and offset > 0:
                    sequence = codon_b[3-offset:] + sequence
                sequences.append((codon_a + sequence, errors, similar_switch, index + 1))
                found_match = True
        if not found_match:
            found_similar_match = False
            if len(nucleotides_b) == 3 and similar_enabled:
                for similar_amino_acid in similar_amino_acids(amino_acid_from_nucleotides(nucleotides_b)):
                    print(f"similar_amino_acid: {similar_amino_acid}")
                    for codon_b in codons_from_amino_acid(similar_amino_acid):
                        if compare_codons(codon_a, codon_b, constraints_a, constraints_b, offset):
                            print(f"found similar match: {codon_a} == {codon_b} with offset {offset} and type: {amino_acid_type(similar_amino_acid)}")
                            constraints_a, constraints_b = get_next_constraints(codon_a, codon_b, offset)
                            sequence, errors, similar_switch, index = optimize_recursive(gene_a[3:], gene_b[3:], constraints_a, constraints_b, offset, similar_enabled)
                            if len(gene_a[3:]) == 0 and offset > 0:
                                sequence = codon_b[3-offset:] + sequence
                            sequences.append((codon_a + sequence, errors, similar_switch + [(index + 1, amino_acid_type(similar_amino_acid))], index + 1))
                            found_similar_match = True
            if not found_similar_match:
                print(f"no match found for {codon_a} and {codons_b} with offset {offset}")
                sequence, errors, similar_switch, index = optimize_recursive(gene_a[3:], gene_b[3:], None, None, offset, similar_enabled)
                if len(gene_a[3:]) == 0 and offset > 0:
                    sequence = codon_b[3-offset:] + sequence
                sequences.append((codon_a + sequence, errors + 1, similar_switch, index + 1))

    print(f"sequences: {sequences}")
    return min(sequences, key=lambda x: (x[1], len(x[2]), x[0][:3] != nucleotides_a))
    

def optimize_protein_sequence(dna_sequence, gene_a_start, gene_a_end, gene_b_start, gene_b_end, new_gene_b, similar_enabled=True):
    # Extract the gene A and gene B sequences
    dna_sequence = dna_sequence.replace(" ", "").replace("\n", "")
    new_gene_b = new_gene_b.replace(" ", "").replace("\n", "")

    reduced_a_start, reduced_b_start = get_overlapping_indices(gene_a_start, gene_b_start)
    gene_a = dna_sequence[reduced_a_start:gene_a_end]
    gene_b = new_gene_b[reduced_b_start - gene_b_start:]
    return optimize_recursive(
        gene_a,
        gene_b,
        None,
        None,
        reduced_b_start - reduced_a_start,
        similar_enabled
    )

if __name__ == "__main__":
    print("Enter DNA sequence optimization parameters:")
    dna_sequence = input("DNA sequence: ").strip()
    gene_a_start = int(input("Gene A start position: "))
    gene_a_end = int(input("Gene A end position: "))
    gene_b_start = int(input("Gene B start position: "))
    gene_b_end = int(input("Gene B end position: "))
    new_gene_b = input("New Gene B sequence: ").strip()

    result, errors = optimize_protein_sequence(
        dna_sequence,
        gene_a_start,
        gene_a_end,
        gene_b_start,
        gene_b_end,
        new_gene_b
    )

    print("\nResults:")
    print(f"Optimized sequence: {result}")
    print(f"Number of errors: {errors}")
