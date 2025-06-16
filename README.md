# SignalSiege

SignalSiege is a web-based strategy game built with FastAPI, PostgreSQL, Docker, and modern web technologies. The project currently features a backend API connected to a Postgres database, deployed via Docker containers.

## Tech Stack

- **Backend:** Python, FastAPI, SQLAlchemy  
- **Database:** PostgreSQL  
- **Frontend:** TypeScript, HTML, Sass  
- **Deployment:** Docker, Docker Compose, VPS  
- **Version Control:** Git, GitHub  

## Current Features

- RESTful API for game logic and state management  
- Persistent data storage using PostgreSQL  
- Dockerized app and database for easy deployment   

## Getting Started

### Prerequisites

- Docker and Docker Compose installed  
- `.env` file configured with your database credentials and app settings  

### Running Locally

1. Clone the repository  
2. Copy `.env.example` to `.env` and fill in your values  
3. Run `docker-compose up --build` to start the app and database  

The backend will be available on `http://localhost:${SYSTEM_PORT}` (default 8000).

---

## Roadmap

### Short Term

- **User authentication & login system:** Add secure user registration, login, and session management.  
- **Improved AI:** Develop more advanced AI opponents with smarter strategies and difficulty levels.  

### Medium Term

- **Multiplayer support:** Implement real-time multiplayer gameplay with synchronization between clients.  
- **Frontend improvements:** Create a polished UI with React or another modern frontend framework.  

### Long Term

- **Matchmaking system:** Enable players to find and join games with others.  
- **Leaderboards and stats:** Track player performance and rankings.  
- **Mobile-friendly UI:** Responsive design for mobile devices.  

---

## Contributing

Contributions are welcome! Please fork the repo and submit pull requests with descriptive messages. Open issues to discuss bugs or features.

---

## License

[GNU AGPLv3](https://choosealicense.com/licenses/agpl-3.0/)