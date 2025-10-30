import argparse
import logging
import os
import pandas as pd

# Logging setup
def setup_logging():
    os.makedirs('logs', exist_ok=True)
    logging.basicConfig(filename='logs/app.log', level=logging.INFO,
                        format='%(asctime)s %(levelname)s:%(message)s')
    error_handler = logging.FileHandler('logs/errors.txt')
    error_handler.setLevel(logging.ERROR)
    logging.getLogger().addHandler(error_handler)

# CLI argument parsing
def parse_args():
    parser = argparse.ArgumentParser(description='Exam Seating Arrangement Generator')
    parser.add_argument('--buffer', type=int, default=0, help='Seats buffer (number to subtract from all room capacities)')
    parser.add_argument('--mode', type=str, choices=['sparse', 'dense'], default='dense', help='Seating mode: sparse (50% capacity) or dense (full)')
    return parser.parse_args()

def load_and_clean_excel(filename):
    try:
        xl = pd.ExcelFile(filename)
        sheets_expected = [
            'in_timetable',
            'in_course_roll_mapping',
            'in_roll_name_mapping',
            'in_room_capacity'
        ]
        data = {}
        for sheet in sheets_expected:
            if sheet in xl.sheet_names:
                df = pd.read_excel(xl, sheet_name=sheet, dtype=str)
                df = df.apply(lambda x: x.str.strip() if x.dtype == "object" else x)
                data[sheet] = df
                logging.info(f"Loaded sheet: {sheet}, shape: {df.shape}")
                print(f"\nSheet: {sheet} ({df.shape[0]} rows, {df.shape[1]} cols)")
                print(df.head(5))
            else:
                logging.error(f"Sheet {sheet} not found in {filename}")
                print(f"Sheet {sheet} not found in your Excel file!")
        # Check and report expected columns present
        timetable_cols = {'Date','Day','Morning','Evening'}
        course_roll_cols = {'rollno','register_sem','schedule_sem','course_code'}
        roll_name_cols = {'Roll','Name'}
        room_capacity_cols = {'Room No.','Exam Capacity','Block'}
        checks = [
            (data.get('in_timetable'), timetable_cols),
            (data.get('in_course_roll_mapping'), course_roll_cols),
            (data.get('in_roll_name_mapping'), roll_name_cols),
            (data.get('in_room_capacity'), room_capacity_cols),
        ]
        for df, expect in checks:
            if df is not None:
                actual = set(df.columns)
                print(f"Required columns: {expect}\nActual columns:   {actual}\n")
                if not expect.issubset(actual):
                    missing = expect - actual
                    logging.error(f"Missing columns in {df}: {missing}")
                    print(f"MISSING COLUMNS: {missing}")
        return data
    except Exception as e:
        logging.error(f"Error loading Excel file: {e}")
        print(f"Error loading Excel: {e}")
        return None

def main():
    setup_logging()
    args = parse_args()
    try:
        logging.info(f'Running with buffer={args.buffer}, mode={args.mode}')
        input_file = 'input_data_tt.xlsx'
        if not os.path.exists(input_file):
            print(f'Input file {input_file} not found.')
            return
        # Load & check all data
        data = load_and_clean_excel(input_file)
        print("\n=== Data loaded and checked. Next: implement seat allocation logic. ===")
    except Exception as e:
        logging.error('Fatal error', exc_info=True)
        print(f'Error occurred: {e}. Check logs/errors.txt for details.')

if __name__ == '__main__':
    main()
