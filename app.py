import streamlit as st
import pandas as pd
import ast

# Page config
st.set_page_config(
    page_title="Movie Recommendation System"
    page_icon="🎬"
    layout="wide"
)

#Load data
@st.cache_data
def load_data():
    df = pd.read_csv("C:/Projects/07_Movie_Recommendation_System/data/movies_dataset_cleaned.csv")
    df["genres"] = df["genres"].apply(ast.literal_eval)
    return df

movies_df = load_data()


# Get all unique genres
all_genres = sorted(
    set(
        genre 
        for genres_list in movies_df["genres"]
        for genre in genres_list

    )
)

# Recommendatipn function
def recommend_by_genres_v2(selected_genres, df, top_n=10):
    temp_df = df.copy()

    temp_df["genre_match_count"] = temp_df["genres"].apply(
        lambda genres: sum(genre in genres for genre in selected_genres)
    )

    temp_df = temp_df[temp_df["genre_match_count"] > 0]

    temp_df = temp_df.sort_values(
        by=["genre_match_count", "vote_average", "popularity"],
        ascending=False
    )

    temp_df = temp_df.drop_duplicates(subset=["title"])

    return temp_df[[
        "title",
        "genres",
        "genre_match_count",
        "vote_average",
        "popularity",
        "release_date"
    ]].head(top_n)

# App UI
st.title("🎬 Personalized Movie Recommendation System")
st.write(
    "Select your favourite genres and get movie recommendations based on genre match, ratingg and popularity."
)

selected_genres = st.multiselect(
    "Choose your favourite genres:",
    options=all_genres
)

top_n = st.slider(
    "Number od recommendations:",
    min_value=5,
    max_value=20,
    value=10
)

if st.button("Get Recommendations"):
    if not selected_genres:
        st.warning("Please select at least one genre")
    else:
        recommendations = recommend_by_genres_v2(selected_genres, movies_df, top_n)

        if recommendations.empty:
            st.error("No recommendations found for the selected genres.")
        else:
            st.subheader("Recomend Movies")
            recommendations["genres"] = recommendations["genres"].apply(lambda x:", ".join(x))
            st.dataframe(recommendations, use_container_width=True)