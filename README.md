# Plant PTS1 Predictor

This is a Streamlit app and command line interface (CLI) that predicts the presence of a Peroxisomal Targeting Signal type 1 (PTS1) in a given sequence. The prediction is based on a random forest model trained on 229 plant PTS1 sequences and 6298 non-PTS1 sequences. The model uses the BLOSUM62 encoding and considers the last 20 amino acids of the sequences.

## Installation

1. Clone the repository:

   ```shell
   git clone https://github.com/a-wiszniewski/pts1-predict.git
   ```

2. Install the required dependencies:

   ```shell
   pip install -r requirements.txt
   ```

## Usage

### Streamlit App

To run the Streamlit app, use the following command:

```shell
streamlit run app.py
```

### Command Line Interface (CLI)

To use the CLI, execute the following command:

```shell
python cli.py input_dir [--model MODEL] [--output OUTPUT] [--filter FILTER]
```

- `input_dir` (required): Path to the input directory containing FASTA files.
- `-m MODEL`, `--model MODEL` (optional): Path to the model file (default: `model/model.pkl`).
- `-o OUTPUT`, `--output OUTPUT` (optional): Output filename (default: `output.csv`).
- `-f FILTER`, `--filter FILTER` (optional): Filter sequences predicted to not contain a PTS1 (Y/n) (default: Y).

## App Functionality

The app provides the following features:

- The user can enter FASTA sequences either by typing directly in the text area or by checking the "example sequence" box to use a pre-filled example.
- After entering the sequences, the user can click the "Predict" button to predict the presence of PTS1 in each sequence.
- The results are displayed as a table showing the sequence ID, PTS1 prediction, PTS1 probability, and the original sequence.
- The user can download the result as a CSV file by clicking the "Download result" button.

## CLI Functionality

The CLI allows you to predict PTS1 peroxisomal targeting sequences in FASTA files. Here is an example command:

```shell
python cli.py input_dir --model model/model.pkl --output output.csv --filter Y
```

- `input_dir`: Path to the input directory containing FASTA files.
- `--model MODEL` (optional): Path to the model file (default: `model/model.pkl`).
- `--output OUTPUT` (optional): Output filename (default: `output.csv`).
- `--filter FILTER` (optional): Filter sequences predicted to not contain a PTS1 (Y/n) (default: Y).

The CLI performs the following steps:

1. Parses the command line arguments.
2. Loads the model from the specified file.
3. Initializes an empty DataFrame for storing the results.
4. Iterates over the files in the input directory, reads the FASTA sequences, and predicts the presence of PTS1.
5. Appends the results to the DataFrame.
6. Filters out sequences predicted to not contain a PTS1 if the `--filter` argument is set to 'Y' or 'yes'.
7. Writes the results to a CSV file specified by the `--output` argument.

## Dependencies

The following dependencies are required to run the app and CLI:

- streamlit
- pandas
- numpy
- sklearn

These dependencies can be installed using the `requirements.txt` file provided.

## Model

The model used for prediction is loaded from a file named `model.pkl`. Make sure the file is located in the `model` directory before running the app or CLI.

## Example

Here is an example of a sequence in FASTA format:

```
>AT1G04290
MDLESVKKYLEGDEDEKAKEPMVAKLPHRFLERFVTNGLKVDLIEPGRIVCSMKIPPHLLNAGKFLHGGATATLVDLIGSAVIYTAGASHSGVSVEINVSYLDAAFLDEEIEIESKALRVGKAVAVVSVELRKKTTGKIIAQGRHTKYFAPRSNL
```

You can either use this example sequence by checking the "example sequence" box in the app or enter your own sequences.

## License

This project is licensed under the [MIT License](LICENSE).