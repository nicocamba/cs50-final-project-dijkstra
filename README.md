# CS50 Final Project — Galicia Dijkstra Route Finder

A Flask website that finds the shortest route between twenty major towns in Galicia, Spain. It uses Dijkstra's algorithm over a fixed road-distance graph.

## Requirements

- Python 3.10+
- pip

## Run locally

Create and activate a virtual environment, then install the dependency:

```bash
python -m venv .venv
pip install -r requirements.txt
flask --app app run
```

On Windows PowerShell, activate the environment with:

```powershell
.venv\Scripts\Activate.ps1
```

Open http://127.0.0.1:5000 in your browser.

## How it works

The graph stores road distances in kilometres. Dijkstra's algorithm repeatedly explores the lowest-cost route and reconstructs the shortest path from predecessor links. The page displays the ordered towns and total distance.

The app has no external API, database, image assets, or API keys. The graph is static data in `app.py`.

## Structure

- `app.py` — graph, Dijkstra implementation, and Flask endpoint.
- `templates/` — selection and result pages.
- `static/styles.css` — responsive styling.
- `requirements.txt` — dependency list.

Created as a CS50 final project.