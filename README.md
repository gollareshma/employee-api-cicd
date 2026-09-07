# Employee API — CI/CD Pipeline

  A REST API for employee data, built to demonstrate an automated build-and-test pipeline: **Flask + MySQL**,
  containerised with **Docker**, tested and deployed through **Jenkins** on **AWS EC2**.

  ---

  ## What this project demonstrates

  The API itself is intentionally small. The point of the project is everything around it — a code change pushed
  to `main` is automatically checked out, installed, launched, and tested without anyone touching the server.

  ```
  git push ──► Jenkins ──► install deps ──► start API ──► run tests ──► report
                                │                                        │
                                └────────── fails fast if any step ──────┘
  ```

  ## Tech stack

  | Layer | Technology |
  |---|---|
  | API | Flask (Python 3.11) |
  | Database | MySQL |
  | Authentication | JWT (PyJWT) |
  | Testing | pytest |
  | CI/CD | Jenkins |
  | Containerisation | Docker |
  | Hosting | AWS EC2 |

  ---

  ## API endpoints

  | Method | Endpoint | Auth | Returns |
  |---|---|:--:|---|
  | `GET` | `/health` | — | Service status |
  | `POST` | `/auth/login` | — | A JWT valid for 24 hours |
  | `GET` | `/employees/` | 🔒 | Employee records |
  | `GET` | `/analytics/headcount` | 🔒 | Headcount summary |

  Protected routes expect the token in a header:

  ```
  Authorization: Bearer <token>
  ```

  The `token_required` decorator in `app/auth.py` validates it and rejects the request with `401` if it's
  missing, expired, or tampered with.

  ---

  ## Running it locally

  ### 1. Install

  ```bash
  git clone https://github.com/gollareshma/employee-api-cicd.git
  cd employee-api-cicd
  pip install -r requirements.txt
  ```

  `flask-mysqldb` compiles against MySQL client headers. On Ubuntu:

  ```bash
  sudo apt install default-libmysqlclient-dev build-essential pkg-config
  ```

  ### 2. Configure

  Create a `.env` file in the project root:

  ```ini
  DB_HOST=localhost
  DB_USER=your_db_user
  DB_PASSWORD=your_db_password
  DB_NAME=employeedb
  JWT_SECRET=generate-a-long-random-value
  FLASK_ENV=development
  ```

  Generate the JWT secret rather than inventing one:

  ```bash
  python -c "import secrets; print(secrets.token_urlsafe(48))"
  ```

  > ⚠️  **Never commit `.env`.** It holds your database password and the key that signs every login token. Anyone
  who reads it can connect to your database and forge tokens for any user. It belongs in `.gitignore`, and if it
  has ever been committed, the credentials in it must be rotated — deleting the file doesn't remove it from git
  history.

  ### 3. Create the database schema

  ```bash
  python create_tables.py
  ```

  ### 4. Run

  ```bash
  python app.py
  ```

  The API listens on `http://127.0.0.1:5000`.

  ### Try it

  ```bash
  # Log in
  curl -X POST http://127.0.0.1:5000/auth/login \
    -H "Content-Type: application/json" \
    -d '{"username":"admin","password":"your_password"}'

  # Use the returned token
  curl http://127.0.0.1:5000/employees/ \
    -H "Authorization: Bearer <token>"
  ```

  ---

  ## Docker

  ```bash
  docker build -t employee-api .
  docker run -p 5000:5000 --env-file .env employee-api
  ```

  `--env-file` passes configuration at run time, which keeps credentials out of the image. A `.dockerignore`
  containing `.env`, `__pycache__/`, and `venv/` ensures they aren't copied in by the `COPY . .` step either —
  anything baked into an image travels with it to every registry it's pushed to.

  ---

  ## Tests

  ```bash
  python app.py &          # the tests run against a live server
  pytest tests/ -v
  ```

  `tests/test_api.py` covers the health check, a successful login, and a rejected login. These are **integration
  tests** — they make real HTTP requests rather than mocking, so they verify the app actually starts and serves
  traffic, which is exactly what the pipeline needs to know.

  ---

  ## The Jenkins pipeline

  `Jenkinsfile` defines three stages:

  | Stage | What happens |
  |---|---|
  | **Checkout Code** | Pulls `main` from GitHub |
  | **Install Dependencies** | Creates a fresh virtualenv and installs `requirements.txt` |
  | **Start API & Run Tests** | Launches the API in the background, waits for it, runs pytest, then shuts it down
  |

  A failure at any stage fails the build and the pipeline reports it.

  ### Setting it up

  1. Install Jenkins on an EC2 instance and open port `8080` in the security group.
  2. Install the **Pipeline** and **Git** plugins.
  3. **New Item → Pipeline → Pipeline script from SCM**, pointing at this repository.
  4. Add the environment variables Jenkins needs via **Manage Jenkins → Credentials** — not by committing them.
  5. Build.

  > The pipeline builds a fresh virtualenv each run rather than reusing one. That's slower, but it means a
  dependency that only works because it's left over from a previous build fails here instead of in production.

  ---

  ## Project structure

  ```text
  employee-api-cicd/
  ├── app.py               # Application entry point, blueprint registration, /auth/login
  ├── config.py            # Reads configuration from environment variables
  ├── create_tables.py     # Database schema setup
  ├── app/
  │   ├── auth.py          # JWT generation and the token_required decorator
  │   ├── employees.py     # /employees routes
  │   └── analytics.py     # /analytics routes
  ├── tests/
  │   └── test_api.py      # Integration tests
  ├── Dockerfile
  ├── Jenkinsfile          # CI/CD pipeline definition
  └── requirements.txt
  ```

  ---

  ## Author

  **Golla Reshma** — B.Tech (CSE — AI & ML)
