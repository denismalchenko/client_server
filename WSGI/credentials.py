from urllib.parse import parse_qs
from wsgiref.simple_server import make_server
from typing import Any
import json
import subprocess

species_credentials = {
    "Cyberman": "John Lumic",
    "Dalek": "Davros",
    "Judoon": "Shadow Proclamation Convention 15 Enforcer",
    "Human": "Leonardo da Vinci",
    "Ood": "Klineman Halpen",
    "Silence": "Tasha Lem",
    "Slitheen": "Coca-Cola salesman",
    "Sontaran": "General Staal",
    "Time Lord": "Rassilon",
    "Weeping Angel": "The Division Representative",
    "Zygon": "Broton",
}


def application(environ: dict[str, str], start_response: Any) -> list[bytes]:
    query_params = parse_qs(environ["QUERY_STRING"])
    species = query_params.get("species", [""])[0]

    if species in species_credentials:
        status = "200 OK"
        response_data = {"credentials": species_credentials[species]}
    else:
        status = "404 NOT FOUND"
        response_data = {"credentials": "Unknown"}

    response_body = json.dumps(response_data).encode("utf-8")
    response_headers = [
        ("Content-Type", "application/json"),
        ("Content-Encoding", "utf-8"),
        ("Content-Length", str(len(response_body))),
    ]
    start_response(status, response_headers)
    return [response_body]


if __name__ == "__main__":
    port = 8888
    httpd = make_server("", port, application)
    print(f"Serving on port {port}...")
    httpd.serve_forever()
