# project_seating_arrangement
<<<<<<< HEAD
project_seating_arrangement
=======

This CLI tool generates exam seating arrangements from timetable, mapping, and room capacity Excel data, with buffer and mode (sparse/dense) support.

## Usage

### Python CLI
```
python seating_arrangement.py --buffer 5 --mode sparse
```

### Docker Compose
```
docker-compose up --build
```

- Exam dates and slot outputs saved in `output/DATE/Morning|Evening`.
- Master files: `output/op_overall_seating_arrangement.xlsx`, `output/op_seats_left.xlsx`
- Logs/errors in `logs/`

## Local Development
- Requires Python 3.10+
- Install dependencies: `pip install -r requirements.txt`

## Arguments
- `--buffer N`  Subtract N seats from all room capacities
- `--mode sparse|dense`  Use 50% capacity (sparse) or full (dense)

## Excel file requirements
- Place timetable and mapping data in `input_data_tt.xlsx`

## Output
- Excel files per slot/date, summarizing seating, student allocations, and seats left

## Error Handling
- All errors/clashes logged in `logs/errors.txt` and `logs/app.log`.
>>>>>>> f12b5a0 (Initial-commit)
