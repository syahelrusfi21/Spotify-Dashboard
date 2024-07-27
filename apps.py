# Importing the required modules
import streamlit as st
import pandas as pd
from PIL import Image
import plotly.express as px

# Reading the CSV file
url_data = 'https://github.com/syahelrusfi21/Spotify-Dashboard/raw/main/cleaned_data.csv'
df = pd.read_csv(url_data, encoding='latin1')

# Dashboard title
st.title("Most Streamed Spotify Songs 2024")

# Spotify logo
img = Image.open('spotify_logo.png')
st.sidebar.image(img)

# Sidebar for page selection
page = st.sidebar.selectbox("Choose The Page", ["Song Informations", "Statistics"])

if page == "Song Informations":
    # Sidebar for artist filter
    artist = st.sidebar.selectbox("Choose The Artist", df['Artist'].dropna().unique())

    # Filter data based on the selected artist
    filtered_df = df[df['Artist'] == artist]

    # Adding index column starting from one
    filtered_df = filtered_df.reset_index(drop=True)
    filtered_df.index += 1
    
    # Displaying complete information of the songs by the selected artist with index starting from one and without the original index column
    st.subheader(f"The Songs by {artist}")
    st.dataframe(filtered_df[['Track', 'Album Name', 'Release Date', 'All Time Rank', 'Spotify Streams', 'Spotify Popularity']])

elif page == "Statistics":
    # Statistics visualization options
    statistic_option = st.sidebar.selectbox(
    "Choose The Statistics",
    ["Spotify Streams", "Spotify Popularity", "Descriptive Statistics"]
    )

    # Displaying visualization based on the selected statistics
    if statistic_option == "Spotify Streams":
        # Creating a combination column to ensure uniqueness of each song based on Track, Artist, and Album Name
        df['Track_Artist_Album'] = df['Track'] + ' - ' + df['Artist'] + ' (' + df['Album Name'] + ')'
        
        # Sorting data by 'Spotify Streams' and taking the top 10 songs
        top_10_songs = df.sort_values(by='Spotify Streams', ascending=False).head(10)

        st.subheader("Top 10 Most Streamed Spotify Songs 2024")
        
        # Visualization of the top 10 songs with highest streaming on Spotify
        fig = px.bar(
            top_10_songs,
            x='Spotify Streams',
            y='Track_Artist_Album',
            color='Spotify Streams',
            color_continuous_scale='reds',
            title='Top 10 Most Streamed Spotify Songs 2024',
            labels={'Spotify Streams': 'Streams', 'Track_Artist_Album': 'Track - Artist (Album)'},
            text='Spotify Streams'
        )
        # Trimming labels if too long
        fig.update_layout(
            yaxis_title='Track - Artist (Album)',
            xaxis_title='Spotify Streams',
            yaxis=dict(
                tickmode='array',
                tickvals=top_10_songs['Track_Artist_Album'],
                ticktext=[t if len(t) <= 50 else t[:47] + '...' for t in top_10_songs['Track_Artist_Album']],
                autorange='reversed'
            ),
            xaxis=dict(tickformat=',')
        )
    
        # Adjusting y-axis to rotate labels
        fig.update_yaxes(tickangle=-45)
    
        st.plotly_chart(fig, use_container_width=True)
        
        # Displaying the top 10 songs table
        st.table(top_10_songs[['Track', 'Artist', 'Album Name', 'Release Date', 'Spotify Streams']].reset_index(drop=True))

    elif statistic_option == "Spotify Popularity":
        # Sorting data by 'Spotify Popularity' and taking the top 10 songs
        top_10_popularity = df.sort_values(by='Spotify Popularity', ascending=False).head(10)

        st.subheader("Top 10 Most Popular Spotify Songs 2024")
    
        # Visualization of the top 10 songs with highest popularity on Spotify
        fig = px.bar(
            top_10_popularity,
            x='Spotify Popularity',
            y='Track',
            color='Spotify Popularity',
            color_continuous_scale='greens',
            title='Top 10 Most Popular Spotify Songs 2024',
            labels={'Spotify Popularity': 'Popularity', 'Track': 'Track'},
            text='Spotify Popularity'
        )
        fig.update_layout(
            xaxis_title='Spotify Popularity',
            yaxis_title='Track',
            yaxis=dict(autorange='reversed')  # Reversing the y-axis to maintain order
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Displaying the top 10 songs table
        st.table(top_10_popularity[['Track', 'Artist', 'Album Name', 'Release Date', 'Spotify Popularity']].reset_index(drop=True))

    elif statistic_option == "Descriptive Statistics":
        st.subheader("Descriptive Statistics")

        # Calculating descriptive statistics
        descriptive_stats = df[['Spotify Streams', 'Spotify Popularity']].describe().transpose()
    
        # Displaying descriptive statistics
        st.write(descriptive_stats)

        # Displaying histogram distribution of 'Spotify Streams' and 'Spotify Popularity'
        st.subheader("Distribution of Spotify Streams")
        fig_streams = px.histogram(df, x='Spotify Streams', nbins=30, title='Distribution of Spotify Streams')
        st.plotly_chart(fig_streams, use_container_width=True)

        st.subheader("Distribution of Spotify Popularity")
        fig_popularity = px.histogram(df, x='Spotify Popularity', nbins=30, title='Distribution of Spotify Popularity')
        st.plotly_chart(fig_popularity, use_container_width=True)