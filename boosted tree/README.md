# Boosted Trees at the Chai Stall

Running it on your Mac mini

``` bash

brew install uv libomp
mkdir -p ~/boosting-lab && cd ~/boosting-lab
mv ~/Downloads/boosting_lab.ipynb .
uv init
uv add numpy pandas matplotlib scikit-learn xgboost lightgbm ipywidgets jupyterlab
uv run jupyter lab

```

LightGBM needs libomp on a Mac. XGBoost doesn’t.

The notebook is built for learning by doing:

- Build boosting by hand with numpy. You re-run one cell, and each run adds one tree and redraws the red error sticks.
- Check against scikit-learn. Your 10 lines give the same 80 and 43 as the real library.
- Sliders. Watch overfitting happen.
- Real data. Race six models on 20,640 California houses.
- Look inside the model with importance charts and an error map.
- Yes/no classification with the same loop.
- Your own data with a fill-in-the-blanks template.

## Other tools worth knowing

- JupyterLab or VS Code with the Jupyter extension: where you run notebooks.
- XGBoost, LightGBM, CatBoost: the libraries people use at work. CatBoost is especially good with text categories.
- SHAP: explains why the model made one particular prediction.
- dtreeviz: draws prettier tree diagrams than scikit-learn’s.
- Kaggle: free practice data. Try “House Prices” first, then “Titanic".
