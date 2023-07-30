import argparse
import os
import pandas as pd
import pickle

from utils.parser import read_fasta

def main():

    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Predict PTS1 peroxisomal targeting sequences in FASTA files')
    parser.add_argument('input_dir', type=str, help='Path to input directory containing FASTA files')
    parser.add_argument('-m','--model', type=str, default='model/model.pkl', help='Path to model file (default: model/model.pkl)')
    parser.add_argument('-o','--output', type=str, default='output.csv', help='Output filename (default: output.csv)')
    parser.add_argument('-f','--filter', type=str, help='Filter sequences predicted to not contain a PTS1 (Y/n)', default='Y')
    args = parser.parse_args()

    filter_sequence = args.filter.lower() in ['y', 'yes']

    # Load model
    model = pickle.load(open(args.model, 'rb'))

    # Initialize empty DataFrame
    results = pd.DataFrame(columns=['filename','id', 'PTS1', 'PTS1 probability', 'sequence'])

    # Iterate over files in input directory
    for filename in os.listdir(args.input_dir):
        if filename.endswith('.fasta') or filename.endswith('.fa'):
            filepath = os.path.join(args.input_dir, filename)
            seqs = read_fasta(filepath)
            pred = model.predict(seqs['sequence'])
            pred_prob = model.predict_proba(seqs['sequence'])
            result = pd.DataFrame({'filename': filename, 'id': seqs['id'], 'PTS1': pred, 'PTS1 probability': pred_prob[:,1], 'sequence': seqs['sequence']})
            results = pd.concat([results, result], ignore_index=True)

    # Filter sequences predicted to not contain a PTS1
    if filter_sequence:
        results = results[results['PTS1'] == 1]

    # Write results to CSV file
    results.to_csv(args.output, index=False)

if __name__ == '__main__':
    main()
