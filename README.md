# Trip Planner AI Service

Project structure

```
├── main.py
├── schemas.py
├── services/
│      └── itinerary_generator.py
├── models/
├── requirements.txt
└── README.md
```

Quick start

- Run the example:

```powershell
python main.py
```

Files

- `main.py`: simple entrypoint that demonstrates generating an itinerary.
- `schemas.py`: small dataclasses for `TripRequest` and `Itinerary`.
- `services/itinerary_generator.py`: placeholder generator function `generate_itinerary`.
- `models/`: package for future domain/database models.
- `requirements.txt`: currently empty (no external dependencies).

Next steps

- Replace the mock `generate_itinerary` with real logic or an API-backed generator.
- Add tests and CI as needed.
