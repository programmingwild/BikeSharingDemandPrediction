# Bike Sharing Demand Prediction

## Dataset
`data/hour.csv` (17,379 rows, UCI Bike Sharing) + `day.csv`.
`train.csv` (10,886) / `test.csv` (6,493) derived in Kaggle format.
Target: `count`. Metric: RMSLE (log1p).

## Results
- Ridge: RMSLE 1.18
- RandomForest: 0.71
- XGBoost (500 trees, depth 7): 0.65
- HistGradientBoosting (best): 0.53

## Run
```
pip install -r requirements.txt
python src/train.py
python src/predict.py   # -> data/submission.csv
streamlit run app.py
```
