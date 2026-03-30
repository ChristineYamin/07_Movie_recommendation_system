import ast
import pandas as pd
import requests
from pathlib import Path
import streamlit as st

# 1. PAGE CONFIGURATION
st.set_page_config(
    page_title="Movie Recommendation System", page_icon="🎬", layout="wide"
)

# 2. CUSTOM CSS FOR MINIMALIST VIBE
st.markdown(
    """
    <style>
    /* Soften the edges of buttons */
    .stButton>button {
        border-radius: 20px !important;
        transition: all 0.3s ease;
    }
    /* Style custom movie cards */
    .movie-card {
        background-color: #ffffff;
        padding: 20px;
        border-radius: 12px;
        border: 1px solid #eaeaea;
        box-shadow: 0 2px 4px rgba(0,0,0,0.02);
        margin-bottom: 15px;
    }
    .movie-card:hover {
        border-color: #ff4b4b;
        box-shadow: 0 4px 8px rgba(0,0,0,0.05);
    }
    /* Poster hover effect */
    img:hover {
        transform: scale(1.05);
        transition: 0.3s;
    }
    .movie-poster {
        border-radius: 6px;
        width: 100%;
        transition: 0.3s;
    }
    .movie-poster:hover {
        transform: scale(1.05);
    
    }
    </style>
""",
    unsafe_allow_html=True,
)


# 3. LOAD DATA
BASE_DIR = Path(__file__).resolve().parent

@st.cache_data
def load_data():
    file_path = BASE_DIR / "data" / "movies_dataset_cleaned.csv"
    df = pd.read_csv(file_path)
    df["genres"] = df["genres"].apply(ast.literal_eval)
    return df


movies_df = load_data()


# 4. TMDB SETUP & POSTER FETCHING FUNCTION
TMDB_API_KEY = "4db017d7f69398f91238d85a3fab3d43"

def get_movie_poster(movie_title):
    """Fetch poster URL from TMDB API using movie title."""
    try:
        url = "https://api.themoviedb.org/3/search/movie"
        params = {
            "api_key": TMDB_API_KEY,
            "query": movie_title
        }

        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()

        if data.get("results") and data["results"][0].get("poster_path"):
            poster_path = data["results"][0]["poster_path"]
            return f"https://image.tmdb.org/t/p/w500{poster_path}"

    except Exception:
        pass

    return "https://via.placeholder.com/500x750.png?text=No+Poster+Available"
# 5. GENRE EXTRACTION
all_genres = sorted(
    set(
        genre
        for genres_list in movies_df["genres"]
        for genre in genres_list
    )
)


# 6. RECOMMENDATION LOGIC
def recommend_by_genres_v2(selected_genres, df, top_n=10):
    temp_df = df.copy()

    temp_df["genre_match_count"] = temp_df["genres"].apply(
        lambda genres: sum(genre in genres for genre in selected_genres)
    )

    temp_df = temp_df[temp_df["genre_match_count"] > 0]

    temp_df = temp_df.sort_values(
        by=["genre_match_count", "vote_average", "popularity"], ascending=False
    )

    temp_df = temp_df.drop_duplicates(subset=["title"])

    return temp_df[
        [
            "title",
            "genres",
            "genre_match_count",
            "vote_average",
            "popularity",
            "release_date",
        ]
    ].head(top_n)


# 7. APP UI
st.title("🎬 Personalized Movie Recommendation System")
st.write(
    "Select your favorite genres and get movie recommendations based on genre match, rating, and popularity."
)

selected_genres = st.multiselect(
    "Choose your favorite genres:", options=all_genres
)

top_n = st.slider(
    "Number of recommendations:", min_value=5, max_value=20, value=10
)

# Button containment
col_btn, _ = st.columns([1, 5])
with col_btn:
    get_rec = st.button("Get Recommendations", use_container_width=True)

if get_rec:
    if not selected_genres:
        st.warning("Please select at least one genre.")
    else:
        recommendations = recommend_by_genres_v2(
            selected_genres, movies_df, top_n
        )

        if recommendations.empty:
            st.error("No recommendations found for the selected genres.")
        else:
            st.success(
                f"Showing top {top_n} recommendations based on your selected genres 🎯"
            )

            # 🎯 Top movie highlight
            top_movie = recommendations.iloc[0]
            top_poster = get_movie_poster(top_movie["title"])

            st.markdown(
                f"""
                <div style="background-color: #fff4f4; padding: 25px; border-radius: 12px; border: 1px solid #ffccd2; margin-bottom: 25px; display: flex; align-items: center;">
                    <img src="{top_poster}" style="border-radius: 8px; width: 100px; margin-right: 20px;">
                    <div>
                        <h2 style="margin-top:0; color: #ff4b4b;">🌟 Top Pick: {top_movie['title']}</h2>
                        <p style="margin-bottom:5px;"><b>⭐ Rating:</b> {top_movie['vote_average']} | <b>🔥 Popularity:</b> {top_movie['popularity']}</p>
                        <p style="margin-bottom:0; color: #555;"><b>🏷️ Genres:</b> {', '.join(top_movie['genres'])}</p>
                    </div>
                </div>
            """,
                unsafe_allow_html=True,
            )

            st.subheader("Recommend Movies")

            # 🎯 Displaying the rest as interactive "Cards" with Posters
            for index, row in recommendations.reset_index(drop=True).iterrows():
                # Skip the top movie since we highlighted it above
                if index == 0:
                    continue

                genres_str = ", ".join(row["genres"])
                release_year = (
                    row["release_date"][:4]
                    if pd.notna(row["release_date"])
                    else "N/A"
                )

                # Fetch the poster from TMDB API
                poster_url = get_movie_poster(row["title"])

                # Create 2 columns inside the loop (1 part poster, 8 parts text)
                col_img, col_txt = st.columns([1, 8])

                with col_img:
                    st.markdown(
                        f'<img src="{poster_url}" class="movie-poster"          >',
                        unsafe_allow_html=True,
                    )

                with col_txt:
                    st.markdown(
                        f"""
                        <div style="padding-left: 10px;">
                            <h4 style="margin: 0; color: #2c3e50;">{row['title']} <span style="font-size: 14px; color: #7f8c8d;">({release_year})</span></h4>
                            <p style="margin: 5px 0; font-size: 14px; color: #555;">⭐ <b>{row['vote_average']:.1f}</b> | Genres: {genres_str}</p>
                            <p style="margin: 0; font-size: 12px; color: #95a5a6;">Match Score: {row['genre_match_count']} | Popularity: {row['popularity']}</p>
                        </div>
                    """,
                        unsafe_allow_html=True,
                    )

                # Light spacer between movies
                st.markdown(
                    "<div style='margin-bottom: 15px;'></div>",
                    unsafe_allow_html=True,
                )