import numpy as np
import matplotlib.pyplot as plt
import io
import base64


def generate_sales_chart(data, quarter_key, sales_key):
    # Extracting the data
    quarters = [int(item[quarter_key]) for item in data]
    sales = [item[sales_key] for item in data]

    # Order data by quarters
    order = np.argsort(quarters)
    quarters = np.array(quarters)[order]
    sales = np.array(sales)[order]

    # Calculate the slope of the line formed by the last two data points
    slope = (sales[-1] - sales[-2]) / (quarters[-1] - quarters[-2])

    # Calculate the sales for the next few quarters
    future_quarters = np.array(range(1, len(quarters) + 4))
    predicted_sales = [sales[-1] + slope *
                       (q - quarters[-1]) for q in future_quarters[-3:]]

    # Combining both the original and predicted data
    all_quarters = np.concatenate((quarters, future_quarters[-3:]))
    all_sales = np.concatenate((sales, predicted_sales))

    plt.figure(figsize=(12, 7))

    # Bar chart for actual sales data
    bars = plt.bar(quarters, sales, color='blue',
                   label='Actual Sales', alpha=0.6)

    # Line chart for extrapolated sales
    plt.plot(all_quarters, all_sales, color='red', linestyle='--',
             label='Extrapolated Sales', marker='o')

    # Adding labels for each bar and each point
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2, height,
                 f'{height:.2f}', ha='center', va='bottom', fontsize=9, rotation=0)

    for q, s in zip(all_quarters, all_sales):
        plt.text(q, s, f'{s:.2f}', ha='left',
                 va='bottom', fontsize=9, rotation=30)

    plt.xlabel(quarter_key)
    plt.ylabel(sales_key)
    plt.legend()
    plt.title(f'{quarter_key} {sales_key} and Extrapolation')
    plt.xticks(all_quarters)

    # Save the figure to an HTML file with embedded image
    img = io.BytesIO()
    plt.savefig(img, format="png")
    img_base64 = base64.b64encode(img.getvalue()).decode('utf-8')
    html_code = f'<img src="data:image/png;base64,{img_base64}" />'

    filename = "HTML/sales_chart_extrapolation.html"
    with open(filename, 'w') as file:
        file.write("<div>")
        file.write(html_code)
        file.write("</div>")

    print(f"HTML saved to {filename}")
    return f"data:image/png;base64,{img_base64}"
