import os

# Base directory for data
DATA_DIR = '../data/'

# Base directory for outputs and figures
OUTPUTS_DIR = '../outputs/'
FIGURES_DIR = os.path.join(OUTPUTS_DIR, 'figures/')

# Ensure directories exist
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(FIGURES_DIR, exist_ok=True)

# File paths
OZ_CLEAN_PARQUET = os.path.join(DATA_DIR, 'oz_clean.parquet')
