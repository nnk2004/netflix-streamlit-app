import streamlit as st
import pandas as pd

@st.cache_data
def load_data():
    df = pd.read_csv("netflix_titles.csv")
    df['listed_in'] = df['listed_in'].fillna('')
    df['country'] = df['country'].fillna('Unknown')
    df['date_added'] = pd.to_datetime(df['date_added'], errors='coerce')
    df['year_added'] = df['date_added'].dt.year
    return df

df = load_data()

st.title("🎬 Netflix Content Explorer")
st.markdown("Filter and explore Netflix Movies and TV Shows 📺")

type_filter = st.sidebar.multiselect("Select Type", df['type'].unique(), default=df['type'].unique())
genre_filter = st.sidebar.multiselect("Select Genres", sorted(set(", ".join(df['listed_in']).split(", "))))
year_range = st.sidebar.slider("Release Year", int(df['release_year'].min()), int(df['release_year'].max()), (2010, 2020))

filtered_df = df[df['type'].isin(type_filter)]
if genre_filter:
    filtered_df = filtered_df[filtered_df['listed_in'].str.contains('|'.join(genre_filter), case=False)]
filtered_df = filtered_df[filtered_df['release_year'].between(*year_range)]

st.markdown(f"### 📊 Showing {len(filtered_df)} titles")
st.dataframe(filtered_df[['title', 'type', 'country', 'release_year', 'rating']].head(20))
