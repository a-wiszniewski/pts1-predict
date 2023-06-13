import pandas as pd
from textwrap import wrap

def parse_fasta(fasta):
    """Helper function to parse fasta string and return a list of tuples."""
    sequences = []
    sequence = ''
    seq_id = None
    for line in fasta:
        if line.startswith('>'):
            if seq_id is not None:
                sequences.append((seq_id, sequence))
                sequence = ''
            seq_id = line.lstrip('>').strip()
        else:
            sequence += line.strip()
    if seq_id is not None:
        sequences.append((seq_id, sequence))
    return sequences

def read_fasta(file_or_string):
    """Parse a fasta file or string and return a df of ids and sequences."""
    try:
        with open(file_or_string, 'r') as fasta_file:
            fasta = fasta_file.readlines()
    except FileNotFoundError:
        fasta = file_or_string.splitlines()

    sequences = parse_fasta(fasta)
    return pd.DataFrame(sequences, columns=['id', 'sequence'])

def write_fasta(df, file_name, id='id', sequence='sequence'):
    """Write a fasta file from a df of ids and sequences."""
    try:
        with open(file_name, 'w') as fasta_file:
            for index, row in df.iterrows():
                fasta_file.write(f'>{row[id]}\n')
                fasta_file.write('\n'.join(wrap(row[sequence],width=80)))
                fasta_file.write('\n')
    except IOError:
        print('Error: File not found.')
        return None


