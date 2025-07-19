import streamlit as st
import pandas as pd

@st.cache_data
def load_data():
    df = pd.read_csv("netflix_titles_sample.csv")
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
# 🎯 Pagination logic
results_per_page = 50
total_results = len(filtered_df)
total_pages = (total_results - 1) // results_per_page + 1

page = st.number_input("Select page", min_value=1, max_value=total_pages, value=1, step=1)
start_idx = (page - 1) * results_per_page
end_idx = start_idx + results_per_page

# 📊 Display paginated results
st.markdown(f"### Showing results {start_idx + 1} to {min(end_idx, total_results)} of {total_results}")
st.dataframe(filtered_df.iloc[start_idx:end_idx][[
    'title',
    'type',
    'country',
    'release_year',
    'rating',
    'duration',
    'listed_in',
    'description'
]])
# 🔍 Search bar
# 🔍 Search bar
# Clean missing values
filtered_df['title'] = filtered_df['title'].fillna('')
filtered_df['description'] = filtered_df['description'].fillna('')

# 🔍 Search bar
search_term = st.text_input("Search by Title or Description")
if search_term:
    filtered_df = filtered_df[
        filtered_df['title'].str.contains(search_term, case=False) |
        filtered_df['description'].str.contains(search_term, case=False)
    ]
st.write(f"🔎 Results found: {len(filtered_df)}")
results_per_page = 50
total_results = len(filtered_df)
total_pages = (total_results - 1) // results_per_page + 1

if total_results == 0:
    st.warning("No results found. Try a different search or filter.")
else:
    page = st.number_input("Select page", min_value=1, max_value=total_pages, value=1, step=1, key="pagination")
    start_idx = (page - 1) * results_per_page
    end_idx = start_idx + results_per_page

    st.markdown(f"### Showing results {start_idx + 1} to {min(end_idx, total_results)} of {total_results}")
    st.dataframe(filtered_df.iloc[start_idx:end_idx][[
        'title', 'type', 'country', 'release_year', 'rating', 'duration', 'listed_in', 'description'
    ]])
