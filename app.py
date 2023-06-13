import streamlit as st
import pandas as pd
from utils.parser import read_fasta
import pickle

# Load the model
@st.cache_resource
def load_model():
    return pickle.load(open('model/model.pkl', 'rb'))
model = load_model()

# Convert the dataframe to a csv file
@st.cache_data
def convert_df(df):
   return df.to_csv(index=False).encode('utf-8')

st.title('Plant PTS1 predictor')
st.markdown('The presence of a Peroxisomal Targeting Signal type 1 (PTS1) in a given sequence is predicted by a random forest model trained on 229 plant PTS1 sequences and 6298 non-PTS1 sequences. The model was trained on the last 20 amino acids of the sequences and uses the BLOSUM62 encoding.\n')

# Example sequence

example = st.checkbox('example sequence')
example_seq = ''
if example:
    example_seq = '>AT1G04290\nMDLESVKKYLEGDEDEKAKEPMVAKLPHRFLERFVTNGLKVDLIEPGRIVCSMKIPPHLLNAGKFLHGGATATLVDLIGSAVIYTAGASHSGVSVEINVSYLDAAFLDEEIEIESKALRVGKAVAVVSVELRKKTTGKIIAQGRHTKYFAPRSNL'

# Fasta sequence input
fasta = st.text_area('Enter fastas:', value=example_seq , height=275, key='fasta-input')

# Predict PTS1 and display the results
if st.button('Predict'):
    seqs = read_fasta(fasta)
    pred = model.predict(seqs['sequence'])
    pred_prob = model.predict_proba(seqs['sequence'])
    result = pd.DataFrame({'id': seqs['id'], 'PTS1': pred, 'PTS1 probability': pred_prob[:,1], 'sequence': seqs['sequence']})
    st.write(result)

    csv = convert_df(result)
    st.download_button("Download result", csv, "result.csv", "text/csv", key='download-csv')
