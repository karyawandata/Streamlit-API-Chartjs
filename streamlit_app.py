import streamlit as st
import requests
import json
from streamlit.components.v1 import html

# URL API
API_URL = "http://localhost:8000/sales-by-film-category"

def get_sales_data():
    try:
        response = requests.get(API_URL)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        st.error(f"Error fetching data from API: {e}")
        return None

def create_chart(data):
    categories = [item['category'] for item in data]
    sales = [item['total_sales'] for item in data]
    
    chart_data = {
        'labels': categories,
        'datasets': [{
            'label': 'Total Sales',
            'data': sales,
            'backgroundColor': 'rgba(75, 192, 192, 0.6)',
            'borderColor': 'rgba(75, 192, 192, 1)',
            'borderWidth': 1
        }]
    }
    
    chart_config = {
        'type': 'bar',
        'data': chart_data,
        'options': {
            'responsive': True,
            'scales': {
                'y': {
                    'beginAtZero': True
                }
            }
        }
    }
    
    chart_html = f"""
    <html>
        <head>
            <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
        </head>
        <body>
            <div style="width: 100%; height: 400px;">
                <canvas id="myChart"></canvas>
            </div>
            <script>
                var ctx = document.getElementById('myChart').getContext('2d');
                var chartConfig = {json.dumps(chart_config)};
                new Chart(ctx, chartConfig);
            </script>
        </body>
    </html>
    """
    return chart_html

def main():
    st.title("Sales by Film Category")
    
    data = get_sales_data()
    if data:
        st.write("Data fetched successfully!")
        
        chart_html = create_chart(data)
        html(chart_html, height=450)
    else:
        st.error("Failed to fetch data. Please check if the API server is running.")

if __name__ == "__main__":
    main()