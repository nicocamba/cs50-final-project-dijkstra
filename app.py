from __future__ import annotations
import heapq
from flask import Flask, render_template, request

app = Flask(__name__)
TOWNS = ["Barco de Valdeorras", "Ourense", "Bande", "Monforte", "Verín", "Lalín", "Lugo", "Ribadeo", "Viveiro", "Ferrol", "Coruña", "Santiago",
"Finisterra", "Ribeira", "Pontevedra", "Vigo", "Ribadavia", "Cerdedo", "La Estrada", "Arzúa"]
# Road distances in kilometres. Values >= 10_000 mean there is no direct road.
DISTANCES = [
    [0, 10000, 10000, 71, 100, 10000, 10000, 10000, 10000, 10000, 10000, 10000, 10000, 10000, 10000, 10000, 10000, 10000, 10000, 10000],
    [10000, 0, 40, 47, 69, 54, 93, 10000, 10000, 10000, 10000, 10000, 10000, 10000, 10000, 10000, 29, 65, 10000, 10000],
    [10000, 40, 0, 10000, 67, 10000, 10000, 10000, 10000, 10000, 10000, 10000, 10000, 10000, 10000, 109, 56, 10000, 10000, 10000],
    [71, 47, 10000, 0, 10000, 65, 66, 10000, 10000, 10000, 10000, 10000, 10000, 10000, 10000, 10000, 10000, 101, 10000, 10000],
    [100, 69, 67, 10000, 0, 10000, 10000, 10000, 10000, 10000, 10000, 10000, 10000, 10000, 10000, 10000, 10000, 10000, 10000, 10000],
    [10000, 54, 10000, 65, 10000, 0, 70, 10000, 160, 122, 115, 52, 10000, 10000, 10000, 10000, 60, 39, 39, 41],
    [10000, 93, 10000, 66, 10000, 70, 0, 72, 104, 112, 101, 10000, 10000, 10000, 10000, 10000, 10000, 10000, 10000, 66],
    [10000, 10000, 10000, 10000, 10000, 10000, 72, 0, 64, 10000, 10000, 10000, 10000, 10000, 10000, 10000, 10000, 10000, 10000, 151],
    [10000, 10000, 10000, 10000, 10000, 160, 104, 64, 0, 61, 10000, 156, 10000, 10000, 10000, 10000, 10000, 10000, 10000, 133],
    [10000, 10000, 10000, 10000, 10000, 122, 112, 10000, 61, 0, 54, 95, 10000, 10000, 10000, 10000, 10000, 10000, 10000, 89],
    [10000, 10000, 10000, 10000, 10000, 115, 101, 10000, 10000, 54, 0, 69, 104, 10000, 10000, 10000, 10000, 10000, 10000, 74],
    [10000, 10000, 10000, 10000, 10000, 52, 10000, 10000, 156, 95, 69, 0, 82, 64, 63, 10000, 10000, 10000, 27, 37],
    [10000, 10000, 10000, 10000, 10000, 10000, 10000, 10000, 10000, 10000, 104, 82, 0, 97, 126, 10000, 10000, 10000, 10000, 10000],
    [10000, 10000, 10000, 10000, 10000, 10000, 10000, 10000, 10000, 10000, 10000, 64, 97, 0, 71, 10000, 137, 81, 68, 10000],
    [10000, 10000, 10000, 10000, 10000, 10000, 10000, 10000, 10000, 10000, 10000, 63, 126, 71, 0, 28, 10000, 30, 44, 10000],
    [10000, 10000, 109, 10000, 10000, 10000, 10000, 10000, 10000, 10000, 10000, 10000, 10000, 10000, 28, 0, 67, 10000, 10000, 10000],
    [10000, 29, 56, 10000, 10000, 60, 10000, 10000, 10000, 10000, 10000, 10000, 10000, 137, 10000, 67, 0, 56, 10000, 10000],
    [10000, 65, 10000, 101, 10000, 39, 10000, 10000, 10000, 10000, 10000, 10000, 10000, 81, 30, 10000, 56, 0, 25, 67],
    [10000, 10000, 10000, 10000, 10000, 39, 10000, 10000, 10000, 10000, 10000, 27, 10000, 68, 44, 10000, 10000, 25, 0, 10000],
    [10000, 10000, 10000, 10000, 10000, 41, 66, 151, 133, 89, 74, 37, 10000, 10000, 10000, 10000, 10000, 67, 10000, 0]
]

def shortest_route(start: str, destination: str) -> tuple[list[str] | None, int | None]:
    """Return the shortest route and its distance using Dijkstra's algorithm."""
    indices = {town: index for index, town in enumerate(TOWNS)}
    if start not in indices or destination not in indices:
        return None, None
    source, target = indices[start], indices[destination]
    distances = [float("inf")] * len(TOWNS)
    previous: list[int | None] = [None] * len(TOWNS)
    distances[source] = 0
    queue = [(0, source)]
    while queue:
        distance, current = heapq.heappop(queue)
        if distance != distances[current]:
            continue
        if current == target:
            break
        for neighbor, weight in enumerate(DISTANCES[current]):
            if neighbor == current or weight <= 0 or weight >= 10_000:
                continue
            candidate = distance + weight
            if candidate < distances[neighbor]:
                distances[neighbor] = candidate
                previous[neighbor] = current
                heapq.heappush(queue, (candidate, neighbor))
    if distances[target] == float("inf"):
        return None, None
    route = []
    current: int | None = target
    while current is not None:
        route.append(TOWNS[current])
        current = previous[current]
    return list(reversed(route)), int(distances[target])

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "GET":
        return render_template("index.html", towns=TOWNS)
    start = request.form.get("start", "")
    destination = request.form.get("destination", "")
    if start not in TOWNS or destination not in TOWNS:
        return render_template("index.html", towns=TOWNS, error="Selecciona dos poblaciones válidas."), 400
    route, distance = shortest_route(start, destination)
    if route is None:
        return render_template("index.html", towns=TOWNS, error="No se encontró una ruta entre esas poblaciones."), 404
    return render_template("result.html", start=start, destination=destination, route=route, distance=distance)

if __name__ == "__main__":
    app.run()
