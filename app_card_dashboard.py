# -*- coding: utf-8 -*-
"""App Card Dashboard.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1ga0mmKODgSxxiV1UFegIYMfuPLPGiOoX
"""

import pandas as pd
import altair as alt
import streamlit as st

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
    uploaded_file = 'App_Card_Data_0527_with_dates.csv'

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

        # List of KPIs
        kpis = [
            "Clicks", "Impressions", "Click-Through Rate Percent",
            "Unique Impressions", "Unique Clicks",
            "Unique Click-Through Rate Percent", "Exposure Rating", "Utility Rating"
        ]

        # Streamlit selectbox for KPIs
        selected_kpi = st.selectbox('Select a KPI:', kpis)

        # Function to plot time series
        def plot_time_series(card_title, selected_kpi):
            card_data = df[df['TITLE'] == card_title]

            chart = alt.Chart(card_data).mark_line().encode(
                x=alt.X('date:T', title='Date', axis=alt.Axis(format='%m/%d')),
                y=alt.Y(selected_kpi, title=selected_kpi.capitalize()),
                tooltip=['date:T', selected_kpi]
            ).properties(
                title=f"{selected_kpi} Time-Series for {card_title}",
                width=800,
                height=400
            ).interactive()

            st.altair_chart(chart)

        # Plot the time series for the selected card title and KPI
        if card_title and selected_kpi:
            plot_time_series(card_title, selected_kpi)

if __name__ == "__main__":
    main()

