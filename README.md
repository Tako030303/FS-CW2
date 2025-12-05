# BuyHomeUZ

## How to Run

1. Create and activate virtual environment:

```bash
python -m venv .venv
.venv\Scripts\activate
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Create `.env` file in `buyhomeuz/` folder:

```
SECRET_KEY=your-secret-key
DEBUG=True
DATABASE_URL=sqlite:///db.sqlite3
```

4. Run migrations:

```bash
cd buyhomeuz
python manage.py migrate
```

5. Start the server:

```bash
python manage.py runserver
```

6. Open: http://127.0.0.1:8000/
