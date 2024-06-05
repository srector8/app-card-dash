# -*- coding: utf-8 -*-
"""App Card Dashboard.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1ga0mmKODgSxxiV1UFegIYMfuPLPGiOoX
"""

import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
from datetime import datetime

def main():
    st.title("App Card Dashboard")

    # Function to load data
    def load_data(file):
        df = pd.read_csv(file)
        return df

    # Function to transform title
    def transform_title(title):
        if pd.isnull(title):
            return title
        else:
            return title.lower().title()

    # Streamlit file uploader
    uploaded_file = 'App_Card_Data_0527_with_dates'

    if uploaded_file is not None:
        df = load_data(uploaded_file)

        # Convert 'DATE' column to datetime if it's not already
        df['date'] = pd.to_datetime(df['date'])

        # Renaming KPI's
        df.rename(columns={
            'CLICKS': 'Clicks',
            'IMPRESSIONS': 'Impressions',
            'CLICKTHROUGH_RATE_PERCENT': 'Click-Through Rate Percent',
            'UNIQUE_IMPRESSIONS': 'Unique Impressions',
            'UNIQUE_CLICKS': 'Unique Clicks',
            'UNIQUE_CLICKTHROUGH_RATE_PERCENT': 'Unique Click-Through Rate Percent',
            'EXPOSURE_RATING': 'Exposure Rating',
            'UTILITY_RATING': 'Utility Rating'
        }, inplace=True)

        # Apply the title transformation
        df['TITLE'] = df['TITLE'].apply(transform_title)

        # List of card titles for dropdown
        card_titles = df['TITLE'].unique()

        # Streamlit selectbox for card titles
        card_title = st.selectbox('Select a card:', card_titles)

        # Function to plot time series
        def plot_time_series(card_title):
            card_data = df[df['TITLE'] == card_title]

            kpis = [
                "Clicks", "Impressions", "Click-Through Rate Percent",
                "Unique Impressions", "Unique Clicks",
                "Unique Click-Through Rate Percent", "Exposure Rating", "Utility Rating"
            ]

            for kpi in kpis:
                plt.figure(figsize=(10, 5))
                plt.bar(card_data['date'], card_data[kpi])
                plt.title(f"{kpi} Time-Series for {card_title}")
                plt.xlabel("Date")
                plt.ylabel(kpi.capitalize())
                plt.xticks(rotation=45)
                st.pyplot(plt)
                plt.clf()

        # Plot the time series for the selected card title
        if card_title:
            plot_time_series(card_title)

if __name__ == "__main__":
    main()
