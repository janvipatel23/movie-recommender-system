# 🎬 Movie Recommender System

A content-based movie recommendation engine built with **TF-IDF** and **cosine similarity** on the TMDB 5000 movie dataset. Select any movie from a dropdown and instantly get **10 visually rich recommendations** with posters — all in a clean **Streamlit** interface. No API key required.

---

## ✨ Features

- **Content-Based Filtering** — Recommends movies based on overview text similarity using TF-IDF vectorization.
- **Top 10 Recommendations** — Returns the 10 most similar movies ranked by cosine similarity score.
- **Movie Poster Display** — Fetches official posters directly from the TMDB image CDN using `poster_path` stored in the CSV — no API key needed.
- **Visual 2×5 Grid Layout** — Recommendations displayed in a clean two-row, five-column Streamlit grid.
- **Graceful Fallback** — Shows a placeholder image if a poster is unavailable.
- **Two-Phase Architecture** — Data preprocessing (`create_pkl.py`) is cleanly separated from the app (`app.py`).

---

## 🏗️ Architecture

```
PHASE 1 — Data Preprocessing (create_pkl.py)
─────────────────────────────────────────────
tmdb_5000_movies.csv  ─┐
                        ├─► merge on 'title' ─► movies DataFrame
tmdb_5000_credits.csv ─┘
                               │
                               ▼
                    Keep: movie_id, title,
                          overview, poster_path
                               │
                               ▼
                    TF-IDF Vectorizer
                    (stop_words='english')
                    fit_transform(overview)
                               │
                               ▼
                    cosine_similarity(tfidf_matrix)
                    → NxN similarity matrix
                               │
                               ▼
               pickle.dump((movies, cosine_sim))
                               │
                               ▼
                       movie_data.pkl ✅
                    (gitignored — ~178 MB)


PHASE 2 — Streamlit App (app.py)
─────────────────────────────────
pickle.load('movie_data.pkl')
       │
       ▼
Streamlit selectbox (all movie titles)
       │
       ▼ (on button click)
get_recommendations(selected_title)
       │
       ├── Find movie index in DataFrame
       ├── Get cosine_sim row for that movie
       ├── Sort by similarity score (descending)
       └── Return top 10 (skip index 0 = itself)
                    │
                    ▼
         fetch_poster(poster_path)
         → https://image.tmdb.org/t/p/w500{path}
                    │
                    ▼
         2×5 grid (st.columns(5))
         └── st.image() + st.write(title)
```

---

## 🛠️ Tech Stack

| Layer | Technology | Purpose |
|---|---|---|
| **Language** | Python 3.11+ | Core application language |
| **UI Framework** | Streamlit | Interactive web interface with dropdown and grid layout |
| **ML — Vectorization** | scikit-learn `TfidfVectorizer` | Convert movie overviews into TF-IDF sparse vectors |
| **ML — Similarity** | scikit-learn `cosine_similarity` | Compute pairwise similarity between all movies |
| **Data Processing** | Pandas | Load, merge, clean, and filter TMDB CSV datasets |
| **Serialization** | Python `pickle` | Save/load the processed movie data and similarity matrix |
| **Poster Images** | TMDB Image CDN | `https://image.tmdb.org/t/p/w500{poster_path}` |
| **Dataset** | TMDB 5000 Movies & Credits | ~5000 movies with overviews, cast, crew, and poster paths |

---

## 📁 Project Structure

```
movie-recommender-system/
├── app.py                    # Streamlit UI — loads pkl, handles recommendations + poster display
├── create_pkl.py             # Data prep script — merges CSVs, builds TF-IDF + cosine sim, saves pkl
├── tmdb_5000_movies.csv      # TMDB movie metadata (id, title, overview, poster_path, genres...)
├── tmdb_5000_credits.csv     # TMDB cast and crew data (merged on title)
├── pyproject.toml            # Python project config
├── .gitignore                # Excludes movie_data.pkl (178 MB — exceeds GitHub limit)
├── LICENSE                   # Apache-2.0
└── README.md
```

> **Note:** `movie_data.pkl` is excluded from the repo via `.gitignore` because it is ~178 MB. You must generate it locally by running `create_pkl.py` before launching the app.

---

## 🚀 Getting Started

### Prerequisites

- Python 3.11+
- No API keys required

### 1. Clone the Repository

```bash
git clone https://github.com/janvipatel23/movie-recommender-system.git
cd movie-recommender-system
```

### 2. Install Dependencies

```bash
pip install streamlit pandas scikit-learn
```

### 3. Generate the Pickle File (One-Time Setup)

This processes the CSVs, computes the TF-IDF matrix and cosine similarity, and saves `movie_data.pkl`:

```bash
python create_pkl.py
```

Expected output:
```
movies columns: ['budget', 'genres', 'homepage', ...]
credits columns: ['movie_id', 'title', 'cast', 'crew']
after merge columns: ['budget', 'genres', ..., 'cast', 'crew']
movie_data.pkl created! total movies: 4809
```

### 4. Launch the App

```bash
streamlit run app.py
```

Open your browser at `http://localhost:8501`.

---

## 🎯 How the Recommendation Works

### Algorithm — Content-Based Filtering with TF-IDF + Cosine Similarity

**Step 1 — TF-IDF Vectorization**

Each movie's `overview` text is converted into a sparse vector where each dimension represents a word's TF-IDF weight — how important that word is to this movie compared to all others.

```python
tfidf = TfidfVectorizer(stop_words='english')
tfidf_matrix = tfidf.fit_transform(movies['overview'])
# Shape: (4809 movies, N unique words)
```

**Step 2 — Cosine Similarity Matrix**

A full pairwise similarity matrix is computed once and stored. Each cell `[i][j]` holds the cosine similarity between movie `i` and movie `j` (0 = unrelated, 1 = identical).

```python
cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)
# Shape: (4809, 4809)
```

**Step 3 — Recommendation Lookup**

At query time, the app looks up the selected movie's row in the similarity matrix, sorts all other movies by score descending, and returns the top 10 (skipping index 0, which is the movie itself).

```python
sim_scores = sorted(enumerate(cosine_sim[idx]), key=lambda x: x[1], reverse=True)
top_10 = sim_scores[1:11]
```

---

## 🖥️ App UI Layout

```
┌────────────────────────────────────────────────────────┐
│          🎬 Movie Recommendation System                │
│                                                        │
│  Select a movie: [ Avatar              ▼ ]            │
│                                                        │
│  [ Recommend ]                                         │
│                                                        │
│  Top 10 recommended movies:                           │
│                                                        │
│  ┌──────┐ ┌──────┐ ┌──────┐ ┌──────┐ ┌──────┐        │
│  │Poster│ │Poster│ │Poster│ │Poster│ │Poster│        │
│  │  1   │ │  2   │ │  3   │ │  4   │ │  5   │        │
│  └──────┘ └──────┘ └──────┘ └──────┘ └──────┘        │
│  Title 1  Title 2  Title 3  Title 4  Title 5          │
│                                                        │
│  ┌──────┐ ┌──────┐ ┌──────┐ ┌──────┐ ┌──────┐        │
│  │Poster│ │Poster│ │Poster│ │Poster│ │Poster│        │
│  │  6   │ │  7   │ │  8   │ │  9   │ │  10  │        │
│  └──────┘ └──────┘ └──────┘ └──────┘ └──────┘        │
│  Title 6  Title 7  Title 8  Title 9  Title 10         │
└────────────────────────────────────────────────────────┘
```

---

## 📊 Dataset — TMDB 5000

| File | Rows | Key Columns Used |
|---|---|---|
| `tmdb_5000_movies.csv` | ~5000 | `id`, `title`, `overview`, `poster_path` |
| `tmdb_5000_credits.csv` | ~5000 | `movie_id`, `title`, `cast`, `crew` |

Both files are merged on `title`. The final DataFrame retains `movie_id`, `title`, `overview`, and `poster_path` for the recommendation engine.

---

## ⚙️ Configuration Reference

| Parameter | Value | Description |
|---|---|---|
| `TfidfVectorizer stop_words` | `'english'` | Removes common English words from feature space |
| `cosine_similarity` | pairwise NxN | Full similarity matrix computed once at prep time |
| Recommendations returned | `10` | `sim_scores[1:11]` (skips self at index 0) |
| Poster width | `130px` | `st.image(poster_url, width=130)` |
| Grid layout | 2 rows × 5 cols | `st.columns(5)` called twice |
| Poster base URL | `https://image.tmdb.org/t/p/w500` | TMDB image CDN, no API key needed |
| Fallback poster | `https://placehold.co/500x750?text=No+Poster` | Shown when `poster_path` is empty |

---

## 📦 Dependencies

```
streamlit
pandas
scikit-learn
```

Install all at once:

```bash
pip install streamlit pandas scikit-learn
```

---

## 🤝 Contributing

Contributions, bug reports, and feature requests are welcome! Feel free to open a pull request or issue on [GitHub](https://github.com/janvipatel23/movie-recommender-system).

---

## 📄 License

This project is licensed under the **Apache-2.0 License**. See the [LICENSE](./LICENSE) file for details.