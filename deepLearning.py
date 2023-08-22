import numpy as np
import matplotlib.pyplot as plt
import io
import base64
import tensorflow as tf
from sklearn.preprocessing import MinMaxScaler


def generate_sales_chart(data, quarter_key, sales_key):
    # Extracting the data
    quarters = [int(item[quarter_key]) for item in data]
    sales = [item[sales_key] for item in data]

    # Reshape data
    X = np.array(quarters).reshape(-1, 1)
    y = np.array(sales).reshape(-1, 1)

    # Normalize the data
    scaler_x = MinMaxScaler()
    scaler_y = MinMaxScaler()
    X_scaled = scaler_x.fit_transform(X)
    y_scaled = scaler_y.fit_transform(y)

    # Define the neural network model
    model = tf.keras.Sequential([
        tf.keras.layers.Dense(10, input_dim=1, activation='relu'),
        tf.keras.layers.Dense(10, activation='relu'),
        tf.keras.layers.Dense(1)
    ])

    model.compile(loss='mse', optimizer='adam')
    model.fit(X_scaled, y_scaled, epochs=200, verbose=0)

    # Predict the next few quarter sales
    future_quarters = np.array(range(1, len(quarters)+4)).reshape(-1, 1)
    future_quarters_scaled = scaler_x.transform(future_quarters)
    predicted_sales_scaled = model.predict(future_quarters_scaled)
    predicted_sales = scaler_y.inverse_transform(predicted_sales_scaled)

    plt.figure(figsize=(12, 7))

    # Bar chart for actual sales data
    bars = plt.bar(quarters, sales, color='blue',
                   label='Actual Sales', alpha=0.6)

    # Line chart for predicted sales
    plt.plot(future_quarters, predicted_sales, color='red',
             linestyle='--', label='NN Predicted Sales', marker='o')

    # Adding labels for each bar and each point
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2, height,
                 f'{height:.2f}',
                 ha='center', va='bottom',
                 fontsize=9, rotation=0)

    for q, s in zip(future_quarters, predicted_sales):
        plt.text(q, s[0], f'{s[0]:.2f}', ha='left',
                 va='bottom', fontsize=9, rotation=30)

    plt.xlabel(quarter_key)
    plt.ylabel(sales_key)
    plt.legend()
    plt.title(f'{quarter_key} {sales_key} and Deep Learning Prediction')
    plt.xticks(future_quarters.flatten())

    # Save the figure to an HTML file with embedded image
    img = io.BytesIO()
    plt.savefig(img, format="png")
    img_base64 = base64.b64encode(img.getvalue()).decode('utf-8')
    html_code = f'<img src="data:image/png;base64,{img_base64}" />'

    filename = "HTML/sales_chart_nn.html"
    with open(filename, 'w') as file:
        file.write("<div>")
        file.write(html_code)
        file.write("</div>")

    print(f"HTML saved to {filename}")
    return f"data:image/png;base64,{img_base64}"
