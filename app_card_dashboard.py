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
    st.write('Click-Through Rate Percentage - The percentage of clicks over the number of impressions')
    st.write('Unique Click-Through Rate Percentage - The percentage of unique clicks over the number of unique impressions')
    st.write('Utility Rating - The ratio of clicks to unique clicks')
    st.write('Exposure Rating - The ratio of impressions to unique impressions')
    st.write('Ticks mark gamedays')

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

        # Filter titles with less than 20 date entries
        title_counts = df['TITLE'].value_counts()
        valid_titles = title_counts[title_counts >= 20].index.tolist()
        df = df[df['TITLE'].isin(valid_titles)]

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

            # Define the base chart
            base_chart = alt.Chart(card_data).mark_line().encode(
                x=alt.X('date:T', title='Date', axis=alt.Axis(format='%m/%d')),
                y=alt.Y(selected_kpi, title=selected_kpi.capitalize()),
                tooltip=['date:T', selected_kpi]
            ).properties(
                title=f"{selected_kpi} Time-Series for {card_title}",
                width=800,
                height=400
            )

            # Define the dates and colors for vertical lines
            important_dates = pd.DataFrame({
                'date': pd.to_datetime(['2024-05-14', '2024-05-17', '2024-05-23', '2024-05-28', '2024-05-31', '2024-06-04', '2024-06-08', '2024-06-10']),  # Add more dates as needed
                'color': ['red', 'red', 'red', 'red', 'red', 'red', 'red', 'red']  # Add more colors corresponding to dates
            })

            rules = alt.Chart(important_dates).mark_rule().encode(
                x='date:T',
                color=alt.Color('color:N', scale=None)
            )

            # Combine the base chart with the rules
            final_chart = base_chart + rules

            st.altair_chart(final_chart.interactive())

            # Calculate and display pre, post, and game day averages
            pre_game_values = []
            game_day_values = []
            post_game_values = []

            for game_date in important_dates['date']:
                pre_game_date = game_date - pd.Timedelta(days=1)
                post_game_date = game_date + pd.Timedelta(days=1)

                pre_game_values.append(card_data[card_data['date'] == pre_game_date][selected_kpi].mean())
                game_day_values.append(card_data[card_data['date'] == game_date][selected_kpi].mean())
                post_game_values.append(card_data[card_data['date'] == post_game_date][selected_kpi].mean())

            pre_game_mean = pd.Series(pre_game_values).mean()
            game_day_mean = pd.Series(game_day_values).mean()
            post_game_mean = pd.Series(post_game_values).mean()

            st.write(f"The mean {selected_kpi.lower()} one day before game days is: {pre_game_mean}")
            st.write(f"The mean {selected_kpi.lower()} on game days is: {game_day_mean}")
            st.write(f"The mean {selected_kpi.lower()} one day after game days is: {post_game_mean}")

        # Plot the time series for the selected card title and KPI
        if card_title and selected_kpi:
            plot_time_series(card_title, selected_kpi)

if __name__ == "__main__":
    main()
