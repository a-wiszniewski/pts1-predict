import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import unittest
import pandas as pd
from utils.encoder import SequenceSubsetter, SequenceEncoder

class TestEncoder(unittest.TestCase):
    
    def test_sequence_subsetter(self):
        X = pd.DataFrame([['MNTE'], ['IPKL']])
        subsetter = SequenceSubsetter(start=1, stop=3)
        X_transformed = subsetter.transform(X)
        expected = pd.DataFrame([['NT'], ['PK']],dtype=object)
        expected.index = expected.index.astype('object')
        pd.testing.assert_frame_equal(X_transformed, expected)
        
    def test_sequence_encoder(self):
        X = pd.DataFrame([['MA'], ['SK']])
        encoder = SequenceEncoder(encoding='blosum62')
        X_transformed = encoder.transform(X)
        expected = pd.DataFrame([
            [
            -1., -1., -2., -3., -1.,  0., -2., -3., -2.,  1.,  2., -1.,  5.,  0., -2., -1., -1., -1.,
            -1.,  1., -3., -1., -1., -4.,  4., -1., -2., -2.,  0., -1., -1.,  0., -2., -1., -1., -1.,
            -1., -2., -1.,  1.,  0., -3., -2.,  0., -2., -1.,  0., -4.
            ],
            [ 
            1., -1.,  1.,  0., -1.,  0.,  0.,  0., -1., -2., -2.,  0., -1., -2., -1.,  4.,  1., -3.,
            -2., -2.,  0.,  0.,  0., -4., -1.,  2.,  0., -1., -3.,  1.,  1., -2., -1., -3., -2.,  5.,
            -1., -3., -1.,  0., -1., -3., -2., -2.,  0.,  1., -1., -4.
            ]
        ])
        pd.testing.assert_frame_equal(X_transformed, expected)
