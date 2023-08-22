import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import mpld3
from statsmodels.formula.api import ols


def generate_html_report(data, x_col, y_col):
    df = pd.DataFrame(data)
    df['INDEX'] = df.index

    # Correlation
    correlation = df[['INDEX', y_col]].corr()

    # Prediction using OLS
    formula = y_col + " ~ INDEX"
    model = ols(formula, data=df).fit()
    df['PREDICTION'] = model.predict()

    # Plotting
    fig, axes = plt.subplots(2, 4, figsize=(20, 10))
    fig.tight_layout(pad=5)

    # Heatmap
    sns.heatmap(correlation, annot=True, cmap='coolwarm', ax=axes[0, 0])
    axes[0, 0].set_title("Heatmap")

    # Bubble chart
    axes[0, 1].scatter(df['INDEX'], df[y_col], s=df[y_col] /
                       df[y_col].max() * 1000, alpha=0.5)
    axes[0, 1].set_title("Bubble chart")
    axes[0, 1].set_xticks(df['INDEX'])
    axes[0, 1].set_xticklabels(df[x_col].values)

    # Scatter plot
    sns.scatterplot(data=df, x='INDEX', y=y_col, ax=axes[0, 2])
    axes[0, 2].set_xticks(df['INDEX'])
    axes[0, 2].set_xticklabels(df[x_col].values)

    # Connected scatter plot
    sns.lineplot(data=df, x='INDEX', y=y_col, ax=axes[0, 3], marker="o")
    axes[0, 3].set_xticks(df['INDEX'])
    axes[0, 3].set_xticklabels(df[x_col].values)

    # Hexagonal binning
    hb = axes[1, 0].hexbin(df['INDEX'], df[y_col], gridsize=50, cmap='Greens')
    cb = plt.colorbar(hb, ax=axes[1, 0])
    cb.set_label('counts')
    axes[1, 0].set_xticks(df['INDEX'])
    axes[1, 0].set_xticklabels(df[x_col].values)

    # Contour plot
    sns.kdeplot(data=df, x='INDEX', y=y_col, ax=axes[1, 1], fill=True)
    axes[1, 1].set_xticks(df['INDEX'])
    axes[1, 1].set_xticklabels(df[x_col].values)

    # Prediction vs Actual
    sns.lineplot(data=df, x='INDEX', y=y_col,
                 ax=axes[1, 2], marker="o", label='Actual')
    sns.lineplot(data=df, x='INDEX', y='PREDICTION',
                 ax=axes[1, 2], marker="x", label='Prediction')
    axes[1, 2].legend(loc='upper left')
    axes[1, 2].set_xticks(df['INDEX'])
    axes[1, 2].set_xticklabels(df[x_col].values)

    # Placeholder for a potential additional plot
    axes[1, 3].axis("off")

    # Generate HTML using mpld3
    html_str = mpld3.fig_to_html(fig)

    with open("output.html", "w") as f:
        f.write(html_str)

    plt.close()


data = [
    {
        "MONTH_ID": "1",
        "SALES": 785874.4400000008
    },
    {
        "MONTH_ID": "2",
        "SALES": 810441.9
    },
    {
        "MONTH_ID": "3",
        "SALES": 754501.3900000001
    },
    {
        "MONTH_ID": "4",
        "SALES": 669390.9600000003
    },
    {
        "MONTH_ID": "5",
        "SALES": 923972.56
    },
    {
        "MONTH_ID": "6",
        "SALES": 454756.77999999985
    },
    {
        "MONTH_ID": "7",
        "SALES": 514875.9700000001
    },
    {
        "MONTH_ID": "8",
        "SALES": 659310.5699999998
    },
    {
        "MONTH_ID": "9",
        "SALES": 584724.2699999999
    },
    {
        "MONTH_ID": "10",
        "SALES": 1121215.2199999997
    },
    {
        "MONTH_ID": "11",
        "SALES": 2118885.67
    },
    {
        "MONTH_ID": "12",
        "SALES": 634679.1199999998
    }
]

generate_html_report(data, "MONTH_ID", "SALES")
