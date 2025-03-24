# DNA Sequence Optimizer

This tool helps optimize overlapping gene sequences, inspired by a project in "How to Grow Almost Anything" where we needed to update a protein sequence using AI. However, the sequence overlaps with another sequence.

![Overlapping genes visualization](overlap.png)

## Problem
When two genes overlap in DNA, changing one sequence can break the other. This tool updates codons to keep a base sequence the same and minimize errors with the new sequence. 

## Usage

Run the program interactively:
```bash
python main.py
```

You'll be prompted for:
- DNA sequence: The original DNA sequence
- Gene A start position: Where the first gene starts
- Gene A end position: Where the first gene ends
- Gene B start position: Where the second gene starts  
- Gene B end position: Where the second gene ends
- New Gene B sequence: The new sequence you want for Gene B

### Example

From our test case:

Original sequence A:
- DNA: GATGGAAACCCGATTCCCTCAGCAATCGCAGCAAACTCCGGCATCTACTAA
- protein: DGNPIPSAIAANSGIY

New sequence B:
- DNA: ATGGCGTGGACCAGCATTTATGAACTGGATGCGCTGAACAACTGCCGTAAAGGTCAGCGCCAGGCCGTGGGCAGCAGCCGCCGCTGCCGCCGCCAGCAGCGTAGCAGCACCCTGTACGTGCTGATTTTTCTGGCGATTTTTCGAGCAAATTTACCAACCAGCTGCTGCTGAGCCTGCTGGAAGCGGTGATTCGCACCGTGACCACCCTGCAGCAGCTGCTGACCTGA
- protein: MAWTSIYELDALNNCRKGQRQAVGSSRRCRRQQRSSTLYVLIFLAIFLSKFTNQLLLSLLEAVIRTVTTLQQLLT

The sequences are offset by 1

Result:
- DNA: GATGGCAACCCGATCCCCTCAGCAATTGCAGCAAACTCCGGCATCTACTAAGGGTCAGCGCCAGGCCGTGGGCAGCAGCCGCCGCTGCCGCCGCCAGCAGCGTAGCAGCACCCTGTACGTGCTGATTTTTCTGGCGATTTTTCTGAGCAAATTTACCAACCAGCTGCTGCTGAGCCTGCTGGAAGCGGTGATTCGCACCGTGACCACCCTGCAGCAGCTGCTGACCTGA

Protein: DGNPIPSAIAANSGIY*GSAPGRGQQPPLPPPAA*QHPVRADFSGDFSEQIYQPAAAEPAGSGDSHRDHPAAAADL
Protein offset by 1: MATRSPQQLQQTPASTKGQRQAVGSSRRCRRQQRSSTLYVLIFLAIFLSKFTNQLLLSLLEAVIRTVTTLQQLLT

As you can see the original protein A's protein sequence has not changed but the codons have in order to minimize the errors in the new sequence:
Aequence A protein:           DGNPIPSAIAANSGIY
Aequence A protein in result: DGNPIPSAIAANSGIY

Sequence A DNA:           GATGGAAACCCGATTCCCTCAGCAATCGCAGCAAACTCCGGCATCTACTAA
Sequence A DNA in result: GATGGCAACCCGATCCCCTCAGCAATTGCAGCAAACTCCGGCATCTACTAA