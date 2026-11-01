import random
import sqlite3
import time
from contextlib import closing
from datetime import datetime


DATABASE_PATH = "factory.db"


def initialize_database() -> tuple[int, float]:
    with closing(sqlite3.connect(DATABASE_PATH)) as conn:
        with conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS production (
                    Time TEXT,
                    Production_Count INTEGER,
                    Machine_Status TEXT,
                    Robot_Status TEXT,
                    Inspection TEXT,
                    Packing_Status TEXT,
                    Temperature REAL,
                    Conveyor_Speed REAL,
                    Cycle_Time REAL,
                    Power_kW REAL
                )
            """)

            columns = {
                column[1]
                for column in cursor.execute("PRAGMA table_info(production)")
            }
            if "Machine_Health" not in columns:
                cursor.execute(
                    "ALTER TABLE production "
                    "ADD COLUMN Machine_Health REAL DEFAULT 100"
                )

    return read_latest_state()


def read_latest_state() -> tuple[int, float]:
    with closing(sqlite3.connect(DATABASE_PATH)) as conn:
        last_row = conn.execute("""
            SELECT Production_Count, Machine_Health
            FROM production
            ORDER BY rowid DESC
            LIMIT 1
        """).fetchone()

    if last_row is None:
        return 0, 100.0

    production_count = 0 if last_row[0] is None else int(last_row[0])
    machine_health = 100.0 if last_row[1] is None else float(last_row[1])
    return production_count, machine_health


def save_data(data: tuple) -> None:
    with closing(sqlite3.connect(DATABASE_PATH)) as conn:
        with conn:
            conn.execute("""
                INSERT INTO production
                (Time, Production_Count, Machine_Status, Robot_Status,
                 Inspection, Packing_Status, Temperature, Conveyor_Speed,
                 Cycle_Time, Power_kW, Machine_Health)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, data)


def main() -> None:
    production_count, machine_health = initialize_database()
    print("🚀 Factory Simulator Started...\n")

    try:
        while True:
            # The dashboard can reset the database while this process is running.
            production_count, machine_health = read_latest_state()

            machine_status = random.choices(
                ["Running", "Idle", "Maintenance", "Fault"],
                weights=[90, 5, 3, 2]
            )[0]

            if machine_status == "Running":
                production_count += 1

            if machine_status == "Running":
                machine_health -= 0.02
            elif machine_status == "Idle":
                machine_health -= 0.005
            elif machine_status == "Maintenance":
                machine_health += 0.10
            else:
                machine_health -= 0.20

            machine_health = max(0.0, min(100.0, machine_health))

            if machine_status == "Running":
                conveyor_speed = round(random.uniform(0.90, 1.20), 2)
            elif machine_status == "Idle":
                conveyor_speed = round(random.uniform(0.10, 0.40), 2)
            else:
                conveyor_speed = 0.00

            if machine_status == "Running":
                robot_status = random.choices(
                    ["Active", "Idle"],
                    weights=[95, 5]
                )[0]
            elif machine_status == "Idle":
                robot_status = "Idle"
            else:
                robot_status = "Offline"

            if machine_status == "Running":
                packing_status = "Running"
            elif machine_status == "Idle":
                packing_status = "Waiting"
            else:
                packing_status = "Stopped"

            if machine_status == "Running":
                if machine_health > 80:
                    cycle_time = round(random.uniform(1.8, 2.4), 2)
                elif machine_health > 60:
                    cycle_time = round(random.uniform(2.6, 3.4), 2)
                elif machine_health > 40:
                    cycle_time = round(random.uniform(3.6, 4.5), 2)
                else:
                    cycle_time = round(random.uniform(4.8, 6.0), 2)
            else:
                cycle_time = 0.00

            if machine_status == "Running":
                power = round(2 + conveyor_speed * 1.5, 2)
            elif machine_status == "Idle":
                power = round(random.uniform(0.8, 1.5), 2)
            else:
                power = round(random.uniform(0.2, 0.8), 2)

            temperature = round(28 + power * 3 + random.uniform(-1, 1), 1)

            if machine_status == "Fault":
                inspection = random.choices(
                    ["OK", "Defect"],
                    weights=[30, 70]
                )[0]
            elif machine_status == "Maintenance":
                inspection = "Defect"
            else:
                defect_chance = min(3 + (100 - machine_health) * 0.3, 50)
                inspection = random.choices(
                    ["OK", "Defect"],
                    weights=[100 - defect_chance, defect_chance]
                )[0]

            data = (
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                production_count,
                machine_status,
                robot_status,
                inspection,
                packing_status,
                temperature,
                conveyor_speed,
                cycle_time,
                power,
                round(machine_health, 2)
            )

            save_data(data)
            print({
                "Time": data[0],
                "Production_Count": data[1],
                "Machine_Status": data[2],
                "Robot_Status": data[3],
                "Inspection": data[4],
                "Packing_Status": data[5],
                "Temperature": data[6],
                "Conveyor_Speed": data[7],
                "Cycle_Time": data[8],
                "Power_kW": data[9],
                "Machine_Health": data[10]
            })

            time.sleep(1)
    except KeyboardInterrupt:
        print("\n🛑 Factory Simulator Stopped.")


if __name__ == "__main__":
    main()
