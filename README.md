# 🎬 Personalized Movie Recommendation System

## 📌 Overview
This project is a personalized movie recommendation system that suggests movies based on user-selected genres. The system analyzes movie data and ranks recommendations using genre matching, rating, and popularity.

The final system is deployed as an interactive Streamlit web application with a clean UI and movie poster integration.

---

## 🚀 Features

- 🎯 Genre-based personalized recommendations
- ⭐ Ranking based on:
  - Genre match count
  - Vote average (rating)
  - Popularity
- 🎬 Movie poster integration using TMDB API
- 🌟 Highlighted "Top Pick" recommendation
- 🎨 Clean and interactive UI (Streamlit + custom CSS)
- 🧠 Easy-to-use interface for first-time users

---

## 🧠 Project Workflow

### 1. Data Collection
Movie data was collected using the TMDB API, including:
- Title
- Overview
- Genre IDs
- Release date
- Vote average
- Popularity
- Language

---

### 2. Data Preprocessing
- Converted genre IDs to readable genre names
- Removed missing values
- Selected relevant columns
- Saved cleaned dataset as CSV

---

### 3. Exploratory Data Analysis (EDA)
Performed analysis to understand:
- Most common genres
- Rating distribution
- Popularity trends
- Movies released over time
- Average rating by genre

---

### 4. Recommendation System
A genre-based recommendation approach was implemented:

- Users select one or more genres
- Movies are filtered based on selected genres
- Each movie is scored using:
  - Number of matching genres
  - Rating
  - Popularity
- Top results are returned as recommendations

---

### 5. Web Application (Streamlit)
The recommendation system was deployed using Streamlit with features such as:
- Genre selection (multiselect)
- Adjustable number of recommendations
- Top movie highlight section
- Movie cards with:
  - Poster
  - Title
  - Release year
  - Rating
  - Genre match score
  - Popularity

---

### 6. Poster Integration
Movie posters were fetched using the TMDB API:
- Search movie by title
- Retrieve poster path
- Display poster images in the app
- Handle missing posters with fallback image

---

## 🛠️ Tech Stack

- Python
- Pandas
- Streamlit
- TMDB API
- Matplotlib & Seaborn (EDA)
- Scikit-learn (initial experimentation)

---


---

## 💡 Future Improvements

- Add movie-title-based recommendation (content-based filtering)
- Improve recommendation accuracy using NLP (TF-IDF + cosine similarity)
- Add trailer integration
- Enhance UI to Netflix-style layout
- Deploy app online (Streamlit Cloud)

---

## 📊 Key Insight

Genre-based recommendation is effective for first-time users, as it removes the need for prior movie knowledge and provides immediate personalized suggestions.

---

## ✨ Conclusion

This project demonstrates a complete data science workflow, including data collection, preprocessing, analysis, recommendation system design, API integration, and application deployment.

---

## 🙌 Author

Shwe Yamin  
Data Science Graduate | Machine Learning & AI Enthusiast