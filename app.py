import streamlit as st
from src.data_loader import load_listings, load_demographics
from src.data_cleaning import clean_listings, clean_demographics
from src.data_merging import merge_listings_demographics
from src.data_visualizations import *

st.set_page_config(page_title="Property Investment Dashboard", layout="wide")
st.title("🏘️ Property Investment Dashboard")

@st.cache_data

def load_clean_merge_data(listings_path="data/listings.csv",demographics_path="data/demographics.csv"):
    listings = load_listings(listings_path)
    demographics = load_demographics(demographics_path)

    listings_cleaned = clean_listings(listings)
    demographics_cleaned = clean_demographics(demographics)

    merged_df = merge_listings_demographics(listings_cleaned, demographics_cleaned)

    return merged_df


df = load_clean_merge_data()
df = add_derived_metrics(df)


# Sidebar Filters
st.sidebar.header("Filters")

# ZipCode_prefix Filter
zip_prefixes = ['All'] + sorted(df["zip_prefix"].dropna().unique().tolist())
sel_zip = st.sidebar.selectbox('ZipCode_Prefix', zip_prefixes)

# Listing Price Filter
price_min = int(df["listing_price"].min())
price_max = int(df["listing_price"].max())
price_range = st.sidebar.slider("Listing Price Range",price_min,price_max,(price_min, price_max))

# Median Income Filter
income_min = int(df["median_income"].min())
income_max = int(df["median_income"].max())
income_range = st.sidebar.slider("Median Income Range",income_min,income_max,(income_min,income_max))

#apply filters
filtered_df = df.copy()
if sel_zip != 'All':
		filtered_df = filtered_df[filtered_df['zip_prefix'] == sel_zip]

if price_range != (price_min, price_max) and income_range != (income_min, income_max):
    # Both filters applied
    filtered_df = df[
        (df["listing_price"] >= price_range[0]) &
        (df["listing_price"] <= price_range[1]) &
        (df["median_income"] >= income_range[0]) &
        (df["median_income"] <= income_range[1])
    ]
elif price_range != (price_min, price_max):
    # Only price filter applied
    filtered_df = df[
        (df["listing_price"] >= price_range[0]) &
        (df["listing_price"] <= price_range[1])
    ]
elif income_range != (income_min, income_max):
    # Only income filter applied
    filtered_df = df[
        (df["median_income"] >= income_range[0]) &
        (df["median_income"] <= income_range[1])
    ]

# KPIs
k1, k2, k3 = st.columns(3)

k1.metric("Number of Listings",f"{len(filtered_df):,}")
k2.metric("Avg Price / Sq Ft", f"${filtered_df['price_per_sqft'].mean():,.0f}")
k3.metric("Average Listing Price", f"${filtered_df['listing_price'].mean():,.0f}")


# Visualizations
st.subheader("📈 Market Visualizations")
st.pyplot(plot_price_distribution(filtered_df))
st.pyplot(plot_price_vs_sqft(filtered_df))
st.pyplot(plot_bedrooms_vs_price(filtered_df))
st.pyplot(plot_price_by_zip_prefix(filtered_df))

st.subheader("🏫 Demographics vs Price")
st.pyplot(plot_income_vs_price(filtered_df))
st.pyplot(plot_school_vs_price(filtered_df))
st.pyplot(plot_crime_vs_price(filtered_df))

st.subheader("💰 Investment Efficiency")
st.pyplot(plot_price_per_sqft_vs_income(filtered_df))
st.pyplot(plot_crime_vs_price_per_sqft(filtered_df))

st.subheader("🧠 Correlation Overview")
st.pyplot(plot_correlation_heatmap(filtered_df))

# Data Preview

st.subheader("📄 Sample Data")
st.dataframe(
    filtered_df[
        [
            "raw_address",
            "postal_code",
            "zip_prefix",
            "listing_price",
            "sq_ft",
            "price_per_sqft",
            "median_income",
            "school_rating",
            "crime_index"
        ]
    ].head(20))
