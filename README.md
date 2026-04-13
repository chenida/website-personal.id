## Setup Environment - Anaconda
```
conda create --name main-ds python=3.13.2
conda activate main-ds
pip install -r requirements.txt
```

## Setup Environment - Shell/Terminal
```
mkdir proyek-streamlit
cd proyek-streamlit
python -m venv venv
pip install streamlit pandas numpy matplotlib seaborn
```

## Run steamlit app
```
streamlit run dashboard.py
```
