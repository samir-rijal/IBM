import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import warnings
warnings.filterwarnings('ignore')

# Set page config
st.set_page_config(
    page_title="BMW Data Insights Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
        .metric-box { 
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 20px;
            border-radius: 10px;
            text-align: center;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }
        .insight-card {
            background: #f0f2f6;
            padding: 15px;
            border-radius: 8px;
            border-left: 4px solid #667eea;
            margin: 10px 0;
        }
        h1 { color: #003A70; }
        h2 { color: #1F4788; }
    </style>
""", unsafe_allow_html=True)

# Load data
@st.cache_data
def load_data():
    try:
        file = r"BMW sales data (2010-2024).csv"
        df = pd.read_csv(file)
        return df
    except:
        st.error("Could not load data. Please ensure CSV file exists.")
        return None

df = load_data()

if df is None:
    st.stop()

st.success("✅ Data loaded successfully!")

# ============================================
# HEADER
# ============================================
st.markdown("# 📊 BMW Sales Data Insights Dashboard")
st.markdown("*Filter and explore key insights from BMW sales analysis (2010-2024)*")
st.markdown("---")

# ============================================
# SIDEBAR FILTERS
# ============================================
st.sidebar.markdown("## 🔍 Filter Options")

# Get unique values for filters
models = sorted(df['Model'].unique().tolist())
regions = sorted(df['Region'].unique().tolist())
fuel_types = sorted(df['Fuel_Type'].unique().tolist())
transmissions = sorted(df['Transmission'].unique().tolist())
colors = sorted(df['Color'].unique().tolist())

# Create filter widgets
with st.sidebar.expander("📍 Model Filters", expanded=True):
    selected_models = st.multiselect(
        "Select Models:",
        options=models,
        default=models[:3] if len(models) > 3 else models,
        key="models"
    )

with st.sidebar.expander("🌍 Regional Filters", expanded=True):
    selected_regions = st.multiselect(
        "Select Regions:",
        options=regions,
        default=regions,
        key="regions"
    )

with st.sidebar.expander("⛽ Vehicle Filters", expanded=True):
    selected_fuel = st.multiselect(
        "Select Fuel Types:",
        options=fuel_types,
        default=fuel_types,
        key="fuel"
    )
    
    selected_transmission = st.multiselect(
        "Select Transmission:",
        options=transmissions,
        default=transmissions,
        key="transmission"
    )

with st.sidebar.expander("🎨 Color Filters", expanded=True):
    selected_colors = st.multiselect(
        "Select Colors:",
        options=colors,
        default=colors[:5] if len(colors) > 5 else colors,
        key="colors"
    )

# Year range slider
year_range = st.sidebar.slider(
    "📅 Select Year Range:",
    min_value=int(df['Year'].min()),
    max_value=int(df['Year'].max()),
    value=(int(df['Year'].min()), int(df['Year'].max())),
    key="year_range"
)

# Price range slider
price_min = int(df['Price_USD'].min())
price_max = int(df['Price_USD'].max())
price_range = st.sidebar.slider(
    "💰 Select Price Range (USD):",
    min_value=price_min,
    max_value=price_max,
    value=(price_min, price_max),
    key="price_range"
)

# Mileage range slider
mileage_min = int(df['Mileage_KM'].min())
mileage_max = int(df['Mileage_KM'].max())
mileage_range = st.sidebar.slider(
    "📍 Select Mileage Range (KM):",
    min_value=mileage_min,
    max_value=mileage_max,
    value=(mileage_min, mileage_max),
    key="mileage_range"
)

# Apply all filters
filtered_df = df[
    (df['Model'].isin(selected_models)) &
    (df['Region'].isin(selected_regions)) &
    (df['Fuel_Type'].isin(selected_fuel)) &
    (df['Transmission'].isin(selected_transmission)) &
    (df['Color'].isin(selected_colors)) &
    (df['Year'] >= year_range[0]) &
    (df['Year'] <= year_range[1]) &
    (df['Price_USD'] >= price_range[0]) &
    (df['Price_USD'] <= price_range[1]) &
    (df['Mileage_KM'] >= mileage_range[0]) &
    (df['Mileage_KM'] <= mileage_range[1])
]

# Display filter summary
st.sidebar.markdown("---")
st.sidebar.markdown(f"**📊 Filtered Records:** `{len(filtered_df):,}` / `{len(df):,}`")
st.sidebar.markdown(f"**Filter Coverage:** `{(len(filtered_df)/len(df)*100):.1f}%`")

# Check if filtered data is empty
if len(filtered_df) == 0:
    st.warning("⚠️ No data matches your filter selections. Please adjust your filters.")
    st.stop()

# ============================================
# KEY METRICS
# ============================================
st.markdown("## 📈 Key Metrics")

metric_col1, metric_col2, metric_col3, metric_col4, metric_col5 = st.columns(5)

with metric_col1:
    st.metric(
        "📊 Total Records",
        f"{len(filtered_df):,}",
        delta=f"{len(filtered_df)/len(df)*100:.1f}% of total"
    )

with metric_col2:
    total_sales = filtered_df['Sales_Volume'].sum()
    st.metric(
        "🏆 Total Sales Volume",
        f"{total_sales:,.0f}",
        delta=f"Avg: {filtered_df['Sales_Volume'].mean():.0f}"
    )

with metric_col3:
    avg_price = filtered_df['Price_USD'].mean()
    st.metric(
        "💰 Avg Price",
        f"${avg_price:,.0f}",
        delta=f"Range: ${filtered_df['Price_USD'].min():,.0f} - ${filtered_df['Price_USD'].max():,.0f}"
    )

with metric_col4:
    avg_mileage = filtered_df['Mileage_KM'].mean()
    st.metric(
        "📍 Avg Mileage",
        f"{avg_mileage:,.0f} KM",
        delta=f"Max: {filtered_df['Mileage_KM'].max():,.0f} KM"
    )

with metric_col5:
    engine_size = filtered_df['Engine_Size_L'].mean()
    st.metric(
        "🔧 Avg Engine Size",
        f"{engine_size:.2f}L",
        delta=f"Range: {filtered_df['Engine_Size_L'].min():.2f}L - {filtered_df['Engine_Size_L'].max():.2f}L"
    )

st.markdown("---")

# ============================================
# TAB LAYOUT
# ============================================
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "📊 Sales Overview",
    "🏪 Price & Value Analysis",
    "🌍 Regional Insights",
    "🚗 Model Comparison",
    "📉 Statistical Analysis",
    "🎯 Detailed Data"
])

# ============================================
# TAB 1: SALES OVERVIEW
# ============================================
with tab1:
    st.subheader("Sales Overview & Trends")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Sales volume by year
        yearly_sales = filtered_df.groupby('Year')['Sales_Volume'].agg(['sum', 'mean']).reset_index()
        fig = px.line(
            yearly_sales, 
            x='Year', 
            y='sum',
            markers=True,
            title="Total Sales Volume by Year",
            labels={'sum': 'Sales Volume', 'Year': 'Year'},
            template="plotly_white"
        )
        fig.update_traces(line=dict(color='#667eea', width=3))
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Sales classification distribution
        sales_class = filtered_df['Sales_Classification'].value_counts().reset_index()
        sales_class.columns = ['Classification', 'Count']
        fig = px.pie(
            sales_class,
            values='Count',
            names='Classification',
            title="Sales Classification Distribution",
            color_discrete_map={'High': '#667eea', 'Low': '#f093fb', 'Medium': '#4facfe'}
        )
        st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Top models by sales
        top_models = filtered_df.groupby('Model')['Sales_Volume'].sum().nlargest(10).reset_index()
        if len(top_models) > 0:
            fig = px.bar(
                top_models,
                x='Sales_Volume',
                y='Model',
                orientation='h',
                title="Top 10 Models by Sales Volume",
                labels={'Sales_Volume': 'Total Sales', 'Model': 'Model'},
                color='Sales_Volume',
                color_continuous_scale='Blues'
            )
            st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Fuel type distribution
        fuel_dist = filtered_df['Fuel_Type'].value_counts().reset_index()
        fuel_dist.columns = ['Fuel Type', 'Count']
        fig = px.bar(
            fuel_dist,
            x='Fuel Type',
            y='Count',
            title="Vehicle Count by Fuel Type",
            color='Count',
            color_continuous_scale='Greens'
        )
        st.plotly_chart(fig, use_container_width=True)

# ============================================
# TAB 2: PRICE & VALUE ANALYSIS
# ============================================
with tab2:
    st.subheader("Price & Value Insights")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Price distribution histogram
        fig = px.histogram(
            filtered_df,
            x='Price_USD',
            nbins=40,
            title="Price Distribution",
            labels={'Price_USD': 'Price (USD)'},
            color_discrete_sequence=['#667eea'],
            template="plotly_white"
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Price by model (box plot)
        top_models_for_price = filtered_df.groupby('Model')['Sales_Volume'].sum().nlargest(8).index.tolist()
        filtered_top_models = filtered_df[filtered_df['Model'].isin(top_models_for_price)]
        
        fig = px.box(
            filtered_top_models,
            x='Model',
            y='Price_USD',
            title="Price Distribution by Top 8 Models",
            labels={'Price_USD': 'Price (USD)', 'Model': 'Model'},
            color='Model',
            template="plotly_white"
        )
        st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    
    # Price statistics by model
    st.subheader("Price Statistics by Model")
    price_stats = filtered_df.groupby('Model')['Price_USD'].agg([
        ('Count', 'count'),
        ('Avg Price', 'mean'),
        ('Min Price', 'min'),
        ('Max Price', 'max'),
        ('Std Dev', 'std')
    ]).round(2).sort_values('Avg Price', ascending=False)
    
    st.dataframe(price_stats, use_container_width=True)
    
    st.markdown("---")
    
    # Price trends
    st.subheader("Average Price Trends Over Years")
    yearly_price = filtered_df.groupby('Year')['Price_USD'].mean().reset_index()
    fig = px.area(
        yearly_price,
        x='Year',
        y='Price_USD',
        title="Average Price Trend (2010-2024)",
        labels={'Price_USD': 'Average Price (USD)', 'Year': 'Year'},
        color_discrete_sequence=['#667eea'],
        template="plotly_white"
    )
    st.plotly_chart(fig, use_container_width=True)

# ============================================
# TAB 3: REGIONAL INSIGHTS
# ============================================
with tab3:
    st.subheader("Regional Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Regional sales
        regional_sales = filtered_df.groupby('Region').agg({
            'Sales_Volume': 'sum',
            'Price_USD': 'mean'
        }).reset_index().sort_values('Sales_Volume', ascending=False)
        
        fig = px.bar(
            regional_sales,
            x='Region',
            y='Sales_Volume',
            title="Total Sales by Region",
            labels={'Sales_Volume': 'Total Sales', 'Region': 'Region'},
            color='Sales_Volume',
            color_continuous_scale='Blues',
            template="plotly_white"
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Average price by region
        fig = px.box(
            filtered_df,
            x='Region',
            y='Price_USD',
            title="Price Distribution by Region",
            labels={'Price_USD': 'Price (USD)', 'Region': 'Region'},
            color='Region',
            template="plotly_white"
        )
        st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    
    # Regional statistics table
    st.subheader("Regional Performance Metrics")
    regional_stats = filtered_df.groupby('Region').agg({
        'Sales_Volume': ['sum', 'mean'],
        'Price_USD': ['mean', 'min', 'max'],
        'Mileage_KM': 'mean',
        'Model': 'nunique'
    }).round(2)
    regional_stats.columns = ['Total Sales', 'Avg Sales', 'Avg Price', 'Min Price', 'Max Price', 'Avg Mileage', 'Unique Models']
    st.dataframe(regional_stats, use_container_width=True)

# ============================================
# TAB 4: MODEL COMPARISON
# ============================================
with tab4:
    st.subheader("Model Performance Analysis")
    
    # Model selection for comparison
    selected_models_comp = st.multiselect(
        "Select Models to Compare:",
        options=filtered_df['Model'].unique(),
        default=filtered_df['Model'].unique()[:5],
        key="model_comp"
    )
    
    if len(selected_models_comp) > 0:
        comparison_df = filtered_df[filtered_df['Model'].isin(selected_models_comp)]
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Engine size vs Price
            fig = px.scatter(
                comparison_df,
                x='Engine_Size_L',
                y='Price_USD',
                color='Model',
                size='Sales_Volume',
                title="Engine Size vs Price",
                labels={'Engine_Size_L': 'Engine Size (L)', 'Price_USD': 'Price (USD)'},
                template="plotly_white"
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Sales volume comparison
            model_comp = comparison_df.groupby('Model')['Sales_Volume'].sum().reset_index()
            fig = px.bar(
                model_comp,
                x='Model',
                y='Sales_Volume',
                title="Sales Volume Comparison",
                labels={'Sales_Volume': 'Total Sales', 'Model': 'Model'},
                color='Sales_Volume',
                color_continuous_scale='Viridis',
                template="plotly_white"
            )
            st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("---")
        
        # Model comparison table
        st.subheader("Model Statistics")
        model_stats = comparison_df.groupby('Model').agg({
            'Sales_Volume': ['sum', 'mean'],
            'Price_USD': ['mean', 'min', 'max'],
            'Engine_Size_L': 'mean',
            'Mileage_KM': 'mean',
            'Year': 'nunique'
        }).round(2)
        model_stats.columns = ['Total Sales', 'Avg Sales', 'Avg Price', 'Min Price', 'Max Price', 'Avg Engine', 'Avg Mileage', 'Years']
        st.dataframe(model_stats.sort_values('Total Sales', ascending=False), use_container_width=True)

# ============================================
# TAB 5: STATISTICAL ANALYSIS
# ============================================
with tab5:
    st.subheader("Statistical Insights")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("### 📊 Sales Volume Statistics")
        sales_stats = {
            'Mean': f"{filtered_df['Sales_Volume'].mean():.2f}",
            'Median': f"{filtered_df['Sales_Volume'].median():.2f}",
            'Std Dev': f"{filtered_df['Sales_Volume'].std():.2f}",
            'Min': f"{filtered_df['Sales_Volume'].min():.2f}",
            'Max': f"{filtered_df['Sales_Volume'].max():.2f}"
        }
        for key, value in sales_stats.items():
            st.markdown(f"**{key}:** {value}")
    
    with col2:
        st.markdown("### 💰 Price Statistics")
        price_stats_dict = {
            'Mean': f"${filtered_df['Price_USD'].mean():,.0f}",
            'Median': f"${filtered_df['Price_USD'].median():,.0f}",
            'Std Dev': f"${filtered_df['Price_USD'].std():,.0f}",
            'Min': f"${filtered_df['Price_USD'].min():,.0f}",
            'Max': f"${filtered_df['Price_USD'].max():,.0f}"
        }
        for key, value in price_stats_dict.items():
            st.markdown(f"**{key}:** {value}")
    
    with col3:
        st.markdown("### 📍 Mileage Statistics")
        mileage_stats = {
            'Mean': f"{filtered_df['Mileage_KM'].mean():,.0f} KM",
            'Median': f"{filtered_df['Mileage_KM'].median():,.0f} KM",
            'Std Dev': f"{filtered_df['Mileage_KM'].std():,.0f}",
            'Min': f"{filtered_df['Mileage_KM'].min():,.0f} KM",
            'Max': f"{filtered_df['Mileage_KM'].max():,.0f} KM"
        }
        for key, value in mileage_stats.items():
            st.markdown(f"**{key}:** {value}")
    
    st.markdown("---")
    
    # Correlation heatmap
    st.subheader("Correlation Analysis")
    
    # Encode categorical variables for correlation
    from sklearn.preprocessing import LabelEncoder
    
    corr_df = filtered_df.copy()
    le_dict = {}
    categorical_cols = ['Model', 'Region', 'Fuel_Type', 'Transmission', 'Color']
    
    for col in categorical_cols:
        if col in corr_df.columns:
            le = LabelEncoder()
            corr_df[col] = le.fit_transform(corr_df[col].astype(str))
            le_dict[col] = le
    
    # Select numerical columns
    numerical_cols = ['Sales_Volume', 'Price_USD', 'Mileage_KM', 'Engine_Size_L', 'Year']
    corr_matrix = corr_df[numerical_cols].corr()
    
    fig = go.Figure(data=go.Heatmap(
        z=corr_matrix.values,
        x=corr_matrix.columns,
        y=corr_matrix.columns,
        colorscale='RdBu',
        zmid=0
    ))
    fig.update_layout(title="Correlation Matrix", template="plotly_white")
    st.plotly_chart(fig, use_container_width=True)

# ============================================
# TAB 6: DETAILED DATA
# ============================================
with tab6:
    st.subheader("Raw Data Explorer")
    
    # Data display options
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        search_column = st.selectbox(
            "Search by column:",
            options=filtered_df.columns,
            key="search_col"
        )
    
    with col2:
        search_value = st.text_input(
            "Search value:",
            key="search_val"
        )
    
    with col3:
        rows_to_display = st.number_input(
            "Rows to display:",
            min_value=10,
            max_value=len(filtered_df),
            value=50,
            step=10
        )
    
    # Apply search filter
    if search_value:
        display_df = filtered_df[
            filtered_df[search_column].astype(str).str.contains(search_value, case=False)
        ].head(rows_to_display)
        st.info(f"Found {len(display_df)} matching records")
    else:
        display_df = filtered_df.head(rows_to_display)
    
    # Display dataframe
    st.dataframe(display_df, use_container_width=True)
    
    st.markdown("---")
    
    # Download options
    col1, col2, col3 = st.columns(3)
    
    with col1:
        csv = filtered_df.to_csv(index=False)
        st.download_button(
            label="📥 Download All Filtered Data (CSV)",
            data=csv,
            file_name="bmw_filtered_data.csv",
            mime="text/csv"
        )
    
    with col2:
        excel_buffer = pd.ExcelWriter('bmw_data.xlsx', engine='openpyxl')
        filtered_df.to_excel(excel_buffer, index=False)
        excel_buffer.close()
        
        with open('bmw_data.xlsx', 'rb') as f:
            st.download_button(
                label="📊 Download All Filtered Data (Excel)",
                data=f.read(),
                file_name="bmw_filtered_data.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
    
    with col3:
        summary_stats = filtered_df.describe().T
        csv_summary = summary_stats.to_csv()
        st.download_button(
            label="📈 Download Summary Statistics (CSV)",
            data=csv_summary,
            file_name="bmw_summary_stats.csv",
            mime="text/csv"
        )

# ============================================
# FOOTER
# ============================================
st.markdown("---")
st.markdown("""
<div style='text-align: center'>
    <p>🏎️ BMW Sales Data Insights Dashboard | 2010-2024 Analysis</p>
    <p>Built with Streamlit & Plotly | Advanced Filtering & Analytics</p>
</div>
""", unsafe_allow_html=True)