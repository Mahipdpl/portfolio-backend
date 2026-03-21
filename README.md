# Mahesh Portfolio — Backend API

FastAPI backend with SQLite, JWT auth, and email notifications.

## Stack
- **FastAPI** — modern async Python web framework
- **SQLite** — zero-config file-based database
- **SQLAlchemy** — ORM
- **JWT (python-jose)** — admin authentication
- **Passlib/bcrypt** — password hashing

---

## Quick Start

### 1. Clone & create virtual environment
```bash
cd portfolio-backend
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure environment
```bash
cp .env.example .env
# Edit .env — set SECRET_KEY and optionally SMTP settings
```

### 4. Run the server
```bash
uvicorn app.main:app --reload
```

Server starts at: http://localhost:8000  
Interactive API docs: http://localhost:8000/docs

---

## Default Admin Credentials
```
Username: mahesh
Password: admin123
```
**Change this immediately after first login via `/api/admin/change-password`**

---

## API Endpoints

### Public
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/projects/` | List all projects |
| GET | `/api/projects/{id}` | Get single project |
| GET | `/api/skills/` | List all skill groups |
| GET | `/api/certifications/` | List all certifications |
| POST | `/api/contact/` | Submit contact message |

### Auth
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/auth/login` | Get JWT token |

### Admin (requires Bearer token)
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET/POST | `/api/admin/projects` | List / create projects |
| PUT/DELETE | `/api/admin/projects/{id}` | Update / delete project |
| GET/POST | `/api/admin/skills` | List / create skill groups |
| PUT/DELETE | `/api/admin/skills/{id}` | Update / delete skill group |
| GET/POST | `/api/admin/certifications` | List / create certifications |
| PUT/DELETE | `/api/admin/certifications/{id}` | Update / delete certification |
| GET | `/api/admin/messages` | View contact messages |
| PATCH | `/api/admin/messages/{id}/read` | Mark message as read |
| DELETE | `/api/admin/messages/{id}` | Delete message |
| POST | `/api/admin/change-password` | Change admin password |

---

## Email Notifications

To receive an email when someone submits the contact form:

1. Enable 2FA on your Gmail account
2. Go to https://myaccount.google.com/apppasswords
3. Generate an app password for "Mail"
4. Add to `.env`:
   ```
   SMTP_USER=your-gmail@gmail.com
   SMTP_PASS=xxxx xxxx xxxx xxxx
   NOTIFY_EMAIL=mahipdpl123@gmail.com
   ```

---

## Connecting to the React Frontend

In your React portfolio, replace the static data arrays with API calls:

```js
// Example: fetch projects
const res = await fetch("http://localhost:8000/api/projects/");
const projects = await res.json();
```

---

## Production Deployment

For deployment (Render, Railway, Fly.io):
1. Switch SQLite → PostgreSQL (change `SQLALCHEMY_DATABASE_URL`)
2. Set a strong `SECRET_KEY` in environment variables
3. Set `allow_origins` in CORS to your actual frontend domain
