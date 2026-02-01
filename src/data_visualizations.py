import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np


def add_derived_metrics(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df = df[df["sq_ft"].notna() & (df["sq_ft"] > 0)]
    df["price_per_sqft"] = df["listing_price"] / df["sq_ft"]
    return df


def plot_price_distribution(df):
    plt.figure(figsize=(10,6))
    prices = df["listing_price"].dropna()
    sns.histplot(prices, bins=30, kde=True, stat="density", color="skyblue", alpha=0.7)
    plt.title("Distribution of Listing Prices")
    plt.xlabel("Listing Price")
    plt.ylabel("Density")
    plt.tight_layout()
    return plt.gcf()


def plot_price_vs_sqft(df):
    plt.figure(figsize=(10,6))
    data = df.dropna(subset=["sq_ft", "listing_price", "bedrooms"])

    sns.scatterplot(
        x="sq_ft",
        y="listing_price",
        hue="bedrooms",
        size="bedrooms",
        sizes=(20, 200),
        palette="viridis",
        alpha=0.7,
        data=data,
        legend="brief")

    plt.title("Listing Price vs Square Footage")
    plt.xlabel("Square Footage")
    plt.ylabel("Listing Price")
    plt.tight_layout()
    return plt.gcf()


def plot_bedrooms_vs_price(df):
    plt.figure(figsize=(10, 6))
    data = df.dropna(subset=["bedrooms", "listing_price"])

    sns.boxplot(x="bedrooms",y="listing_price",data=data,palette="pastel")

    plt.title("Bedrooms vs Listing Price")
    plt.xlabel("Bedrooms")
    plt.ylabel("Listing Price")
    plt.tight_layout()
    return plt.gcf()


def plot_price_by_zip_prefix(df):
    plt.figure(figsize=(10, 6))
    data = df.dropna(subset=["zip_prefix", "listing_price"])

    sns.boxplot(x="zip_prefix",y="listing_price",data=data,palette="pastel")

    plt.title("Listing Price Distribution by ZIP Prefix")
    plt.xlabel("ZIP Prefix")
    plt.ylabel("Listing Price")
    plt.xticks(rotation=45)
    plt.tight_layout()
    return plt.gcf()



def plot_income_vs_price(df):
    plt.figure(figsize=(10, 6))
    data = df.dropna(subset=["median_income", "listing_price"])

    sns.regplot(x="median_income",y="listing_price",data=data,scatter_kws={"alpha":0.7},line_kws={"color":"red"})

    plt.title("Median Income vs Listing Price")
    plt.xlabel("Median Income")
    plt.ylabel("Listing Price")
    plt.tight_layout()
    return plt.gcf()


def plot_school_vs_price(df):
    plt.figure(figsize=(10, 6))
    data = df.dropna(subset=["school_rating", "listing_price"])

    sns.regplot(x="school_rating",y="listing_price",data=data,scatter_kws={"alpha": 0.7},line_kws={"color": "red"})

    plt.title("School Rating vs Listing Price")
    plt.xlabel("School Rating")
    plt.ylabel("Listing Price")
    plt.tight_layout()
    return plt.gcf()


def plot_crime_vs_price(df):
    plt.figure(figsize=(10, 6))
    data = df.dropna(subset=["crime_index", "listing_price"])

    sns.boxplot(x="crime_index",y="listing_price",data=data,palette="pastel")

    plt.title("Listing Price by Crime Index")
    plt.xlabel("Crime Index")
    plt.ylabel("Listing Price")
    plt.tight_layout()
    return plt.gcf()


def plot_price_per_sqft_vs_income(df):
    plt.figure(figsize=(10, 6))
    data = df.dropna(subset=["median_income", "price_per_sqft"])

    sns.regplot(x="median_income",y="price_per_sqft",data=data,scatter_kws={"alpha": 0.7},line_kws={"color": "red"})

    plt.title("Price per Sq.Ft vs Median Income")
    plt.xlabel("Median Income")
    plt.ylabel("Price per Sq.Ft")
    plt.tight_layout()
    return plt.gcf()


def plot_price_per_sqft_vs_bedrooms(df):
    plt.figure(figsize=(10,6))
    data = df.dropna(subset=["bedrooms", "price_per_sqft"])
    
    sns.boxplot(x="bedrooms", y="price_per_sqft", data=data, palette="pastel")
    
    plt.title("Price per Sq.Ft by Number of Bedrooms")
    plt.xlabel("Bedrooms")
    plt.ylabel("Price per Sq.Ft")
    plt.tight_layout()
    return plt.gcf()


def plot_crime_vs_price_per_sqft(df):
    plt.figure(figsize=(10, 6))
    data = df.dropna(subset=["crime_index", "price_per_sqft"])

    sns.boxplot(x="crime_index",y="price_per_sqft",data=data,palette="pastel")

    plt.title("Price per Sq.Ft by Crime Index")
    plt.xlabel("Crime Index")
    plt.ylabel("Price per Sq.Ft")
    plt.tight_layout()
    return plt.gcf()


def plot_correlation_heatmap(df):
    corr_columns = ["listing_price", "sq_ft", "bedrooms", "median_income", "school_rating"]
    corr_df = df[corr_columns].dropna()
    corr_matrix = corr_df.corr(method="pearson")

    plt.figure(figsize=(10, 8))
    sns.heatmap(
        corr_matrix,
        annot=True,
        fmt=".2f",
        cmap="coolwarm",
        center=0,
        linewidths=0.5,
        cbar=True,
        square=True)
    
    plt.title("Correlation Heatmap: Property Price vs Key Demographics", fontsize=14)
    plt.xticks(rotation=45)
    plt.yticks(rotation=0)
    plt.tight_layout()
    return plt.gcf()