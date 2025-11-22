# 🔴 Minimal Pokedex

A modern, interactive Pokedex application built with Streamlit and powered by PokeAPI. Experience Pokemon data like never before with a clean, intuitive interface and rich features.

## 🌐 Live Demo

**Try it now:** [https://pokedex-ai.streamlit.app/](https://pokedex-ai.streamlit.app/)

## ✨ Features

### 🏠 Home Page
- **Animated Pokemon Grid** - Browse Pokemon with smooth animated sprites (GIFs)
- **Smart Search** - Autocomplete search to find any Pokemon instantly
- **Generation Filter** - Filter Pokemon by generation (Gen 1-9)
- **Consistent Layout** - Perfectly aligned grid with intelligent fallback for missing sprites
- **Loading Indicator** - Visual feedback while fetching data

### 📋 Detail View
- **High-Quality Artwork** - Official Pokemon artwork in stunning quality
- **Shiny Mode** - Toggle to view rare shiny variants
- **Type Icons** - Beautiful type badges from Pokemon Sword & Shield
- **Essential Info** - Height, Weight, Abilities, Gender Ratio
- **Type Effectiveness** - Interactive modal showing weaknesses, resistances, and immunities
- **Pokedex Description** - Official Pokemon descriptions
- **Base Stats** - Visual stats with color-coded progress bars
- **Pokemon Cries** - Listen to authentic Pokemon sounds
- **Evolution Chain** - View and navigate through evolution stages
- **Varieties & Forms** - Access Mega Evolutions, Gigantamax, and Regional forms

## 🏗️ Architecture

Built with clean, modular architecture for maintainability and scalability:

```
src/
├── config/          # Constants and configuration
├── api/             # PokeAPI client with caching
├── services/        # Business logic layer
│   ├── pokemon_service.py
│   └── type_service.py
└── ui/              # Views and components
    ├── home.py
    ├── detail.py
    └── components/
```

**Key Benefits:**
- 🧩 **Modular Design** - Easy to maintain and extend
- ⚡ **Cached API Calls** - Blazing fast performance
- 🎯 **Separation of Concerns** - Clean code organization
- 🤖 **AI-Ready** - Prepared for future AI integration

## 🚀 Running Locally

### Option 1: Docker (Recommended)
```bash
# Clone the repository
git clone https://github.com/cam-hm/pokedex-ai.git
cd pokedex-ai

# Run with Docker Compose
docker-compose up --build

# Access at http://localhost:8501
```

### Option 2: Manual Setup
```bash
# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run app.py
```

## 🛠️ Tech Stack

- **Frontend:** Streamlit
- **API:** PokeAPI
- **Language:** Python 3.9+
- **Deployment:** Streamlit Cloud
- **Containerization:** Docker

## 📊 Data Source

All Pokemon data is fetched from [PokeAPI](https://pokeapi.co/), a free and open Pokemon API.

## 🎨 Design Philosophy

- **Minimalist** - Clean, distraction-free interface
- **Intuitive** - Easy navigation and discovery
- **Responsive** - Works on all screen sizes
- **Fast** - Optimized with caching and efficient data fetching

## 🔮 Future Roadmap

- 🤖 **AI Integration** - Pokemon analysis and team building
- 🎮 **Advanced Filters** - Filter by type, ability, stats
- 📊 **Stat Comparison** - Compare multiple Pokemon
- 💾 **Favorites** - Save and manage favorite Pokemon
- 🌍 **Multi-language** - Support for multiple languages

## 📝 License

This project uses data from PokeAPI. Pokemon and Pokemon character names are trademarks of Nintendo.

## 🤝 Contributing

Contributions are welcome! Feel free to open issues or submit pull requests.

## 📧 Contact

Created by [@cam-hm](https://github.com/cam-hm)

---

**Enjoy exploring the world of Pokemon!** 🎮✨
