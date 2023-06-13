import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import unittest
import pandas as pd
from textwrap import dedent
from tempfile import NamedTemporaryFile
from utils.parser import parse_fasta, read_fasta, write_fasta

class TestFastaFunctions(unittest.TestCase):
    def test_parse_fasta(self):
        fasta = dedent('''
            >seq1
            ATCG
            >seq2
            GCTA
        ''').strip().splitlines()
        expected = [('seq1', 'ATCG'), ('seq2', 'GCTA')]
        self.assertEqual(parse_fasta(fasta), expected)

    def test_read_fasta(self):
        # Test reading from file
        with NamedTemporaryFile(mode='w', delete=False) as tmp_file:
            tmp_file.write('>seq1\nATCG\n>seq2\nGCTA\n')
        expected = pd.DataFrame([('seq1', 'ATCG'), ('seq2', 'GCTA')], columns=['id', 'sequence'])
        self.assertTrue(read_fasta(tmp_file.name).equals(expected))
        # Test reading from string
        fasta_str = '>seq1\nATCG\n>seq2\nGCTA\n'
        self.assertTrue(read_fasta(fasta_str).equals(expected))

    def test_write_fasta(self):
        df = pd.DataFrame([('seq1', 'ATCG'), ('seq2', 'GCTA')], columns=['id', 'sequence'])
        # Test writing to file
        with NamedTemporaryFile(delete=False) as tmp_file:
            write_fasta(df, tmp_file.name)
            tmp_file.flush()
            tmp_file.seek(0)
            expected = dedent('''
                >seq1
                ATCG
                >seq2
                GCTA
            ''').strip()
            self.assertEqual(tmp_file.read().strip().decode('utf-8'), expected)


if __name__ == '__main__':
    unittest.main()
