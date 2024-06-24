import io
import base64
import matplotlib.pyplot as plt

def generate_price_movement_image(data, plt_size=(10, 5)):
    plt.figure(figsize=plt_size)
    plt.plot(data['Date'], data['Close'], label='Close Price', color='black')
    plt.scatter(data[data['shares_diff'] > 0]['Date'], data[data['shares_diff'] > 0]['Close'], marker='^', color='green', label='Buy Signal', s=50)
    plt.scatter(data[data['shares_diff'] < 0]['Date'], data[data['shares_diff'] < 0]['Close'], marker='v', color='red', label='Sell Signal', s=50)
    # plt.scatter(filtered_data[filtered_data['shares'] == 0]['Date'], filtered_data[filtered_data['shares'] == 0]['Close'], marker='v', color='red')
    plt.title('Dollar Cost Averaging')
    plt.xlabel('Date')
    plt.ylabel('Close Price')
    plt.legend()
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_base64 = base64.b64encode(buffer.getvalue()).decode()
    buffer.close()
    image_data = f"data:image/png;base64,{image_base64}"
    return image_data

def generate_cost_revenue_image(data, plt_size=(10, 5)):
    plt.figure(figsize=plt_size)
    plt.plot(data['Date'], data['cumulative_cost'], label='Cumulative Cost', color='blue')
    plt.plot(data['Date'], data['amount'], label='Amount', color='red')
    plt.title('Dollar Cost Averaging')
    plt.xlabel('Date')
    plt.ylabel('Amount')
    plt.legend()
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_base64 = base64.b64encode(buffer.getvalue()).decode()
    buffer.close()
    image_data = f"data:image/png;base64,{image_base64}"
    return image_data