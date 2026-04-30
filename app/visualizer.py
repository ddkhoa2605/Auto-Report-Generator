import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

def plot_revenue_trend(daily_revenue_df: pd.DataFrame, anomalies_df: pd.DataFrame = None):
    """Vẽ biểu đồ xu hướng doanh thu với các điểm bất thường."""
    fig = px.line(
        daily_revenue_df, 
        x='date', 
        y='revenue',
        title='Xu Hướng Doanh Thu Theo Thời Gian',
        labels={'date': 'Ngày', 'revenue': 'Doanh Thu (VNĐ)'},
        template='plotly_white',
        line_shape='spline', # Làm mượt đường kẻ
        color_discrete_sequence=['#636EFA']
    )

    # Nếu có điểm bất thường, đánh dấu chúng lên biểu đồ
    if anomalies_df is not None and not anomalies_df.empty:
        fig.add_trace(
            go.Scatter(
                x=anomalies_df['date'],
                y=anomalies_df['revenue'],
                mode='markers',
                name='Điểm Bất Thường',
                marker=dict(color='red', size=10, symbol='x')
            )
        )

    fig.update_layout(
        hovermode='x unified',
        title_font_size=20,
        margin=dict(l=20, r=20, t=60, b=20)
    )
    return fig

def plot_top_products(top_products_df: pd.DataFrame):
    """Vẽ biểu đồ Top sản phẩm."""
    if top_products_df.empty:
        return None
        
    fig = px.bar(
        top_products_df,
        x='revenue',
        y='product',
        orientation='h',
        title='Top Sản Phẩm Doanh Thu Cao Nhất',
        labels={'product': 'Sản Phẩm', 'revenue': 'Doanh Thu (VNĐ)'},
        color='revenue',
        color_continuous_scale='Viridis',
        template='plotly_white'
    )
    
    fig.update_layout(
        yaxis={'categoryorder': 'total ascending'},
        title_font_size=20,
        margin=dict(l=20, r=20, t=60, b=20)
    )
    return fig

def plot_product_pie(top_products_df: pd.DataFrame):
    """Vẽ biểu đồ tỷ trọng sản phẩm."""
    if top_products_df.empty:
        return None
        
    fig = px.pie(
        top_products_df,
        values='revenue',
        names='product',
        title='Tỷ Trọng Doanh Thu Theo Sản Phẩm',
        hole=0.4, # Tạo hình donut cho hiện đại
        color_discrete_sequence=px.colors.qualitative.Pastel,
        template='plotly_white'
    )
    
    fig.update_traces(textposition='inside', textinfo='percent+label')
    fig.update_layout(
        title_font_size=20,
        margin=dict(l=20, r=20, t=60, b=20)
    )
    return fig
