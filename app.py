from datetime import datetime, timedelta
from pathlib import Path
import sqlite3
import random
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from streamlit_autorefresh import st_autorefresh

ROOT = Path(__file__).resolve().parent
DB_PATH = ROOT / "factory.db"
st.set_page_config(page_title="Smart Factory Digital Twin", page_icon="🏭", layout="wide")
st_autorefresh(interval=2000, key="factory_refresh")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&display=swap');
.stApp{background:radial-gradient(circle at 70% 0%,#10243d,#071426 45%,#050d19);font-family:Inter,sans-serif}
[data-testid="stSidebar"]{display:none}
[data-testid="stMainBlockContainer"]{max-width:100%;padding:1rem 1.1rem 2rem}
[data-testid="stSidebar"] .stButton button{background:transparent;border:0;color:white;text-align:left;font-size:1rem;border-radius:7px}
[data-testid="stSidebar"] .stButton button:hover{background:#1269d6}
h1,h2,h3,h4,p,span,label{color:#f7f9fc!important}.brand{text-align:center;padding:1rem .2rem 1.2rem;border-bottom:1px solid #5a6779;margin-bottom:1rem}
.hero small{display:block;margin-top:.35rem;color:#d9e8f7!important}.panel-title{color:#f4f8ff!important}.panel small{color:#c8d8e8!important}.pill,.signal{color:#f4f8ff!important}.mini-kpi,.mini-kpi *{color:#f4f8ff!important}.mini-label{color:#d9e7f4!important}.mini-value{color:#ffffff!important}.health-line,.health-line *{color:#f4f8ff!important}
.stTabs [data-baseweb="tab"]{color:#dce9f7!important}.stTabs [data-baseweb="tab"][aria-selected="true"]{color:#ffffff!important}.stTabs button[role="tab"] p{color:inherit!important}
div[data-testid="stDataFrame"] [data-testid="stElementToolbar"]{background:#dce9f5!important;border:1px solid #9fb8cc!important;border-radius:7px!important;box-shadow:0 2px 8px #0005!important}div[data-testid="stDataFrame"] [data-testid="stElementToolbar"] button{background:#eaf3fa!important;color:#17324a!important;opacity:1!important;border-radius:5px!important}div[data-testid="stDataFrame"] [data-testid="stElementToolbar"] button:hover{background:#c9e5f3!important;color:#08233b!important}div[data-testid="stDataFrame"] [data-testid="stElementToolbar"] svg{color:#17324a!important}
div[data-baseweb="popover"],div[data-baseweb="popover"] *,div[data-baseweb="tooltip"],div[data-baseweb="tooltip"] *{color:#17324a!important}div[data-baseweb="popover"] [role="dialog"],div[data-baseweb="popover"]>div,div[data-baseweb="tooltip"]>div{background:#f4f8fc!important}
.brand-icon{font-size:2.6rem}.brand-title{font-size:1.2rem;font-weight:800;line-height:1.2}.brand-sub{margin-top:.75rem;font-size:.9rem}
.hero h1{margin:0;font-size:2.05rem;font-weight:800;letter-spacing:.01em}.hero p{margin:.1rem 0 0;font-size:1rem;color:#d8e5f3!important}.logo{color:#ff4b5c;font-size:1.2rem;font-weight:800}
.pill{border:1px solid #2c8a62;background:#073728;border-radius:7px;text-align:center;padding:.48rem .5rem;font-weight:600}.pill.blue{border-color:#1966ae;background:#08254d}.pill.warn{border-color:#6d6b48;background:#30322a}
.panel{background:linear-gradient(145deg,rgba(14,34,54,.98),rgba(5,18,33,.98));border:1px solid #08bcd4;border-radius:11px;padding:.65rem .8rem;margin-bottom:.45rem;box-shadow:0 7px 20px #0003}.panel-title{font-size:1rem;font-weight:800;margin-bottom:.45rem}
.kpi{min-height:88px;border-radius:10px;padding:.7rem .9rem;border:1px solid #1884c8;background:linear-gradient(135deg,#083765,#06223d)}.kpi.green{border-color:#0ebd7e;background:linear-gradient(135deg,#074732,#073228)}.kpi.purple{border-color:#8151dc;background:linear-gradient(135deg,#3a236d,#24164c)}.kpi.pink{border-color:#ed477e;background:linear-gradient(135deg,#5a1d46,#3d1538)}.kpi.teal{border-color:#08bad1;background:linear-gradient(135deg,#064b5b,#063544)}
.kpi-label{font-size:.82rem;font-weight:600}.kpi-value{font-size:1.55rem;font-weight:800;margin-top:.18rem}div[data-testid="stDataFrame"]{border:1px solid #2d4965;border-radius:9px}div.stButton>button{background:#096bd5;color:white;border:0;border-radius:7px;font-weight:700}
.stDownloadButton button{background:linear-gradient(135deg,#08b8df,#0875d1)!important;color:#ffffff!important;border:1px solid #35d9f0!important;border-radius:8px!important;font-weight:700!important;box-shadow:0 4px 14px rgba(0,174,225,.2)}.stDownloadButton button:hover{background:linear-gradient(135deg,#20d4ec,#0b8bea)!important;border-color:#7cefff!important;color:#ffffff!important}
.mini-kpi{border:1px solid #147398;border-left:4px solid #08d4e5;border-radius:10px;background:linear-gradient(135deg,#102c43,#0a1d31);padding:.55rem .7rem;min-height:72px}.mini-label{font-size:.77rem;font-weight:600;color:#d9e7f4!important}.mini-value{font-size:1.34rem;font-weight:700;margin-top:.12rem}.signal{border:1px solid #087d78;background:#063b3d;border-radius:7px;padding:.42rem .55rem;font-size:.81rem;font-weight:600;margin:.22rem 0}.health-line{display:flex;align-items:center;gap:.45rem;margin:.38rem 0;font-size:.78rem}.health-line span:first-child{width:4rem}.health-track{height:7px;border-radius:8px;background:#cbd5df;flex:1;overflow:hidden}.health-fill{height:100%;background:#08c4e8;border-radius:8px}.event{display:grid;grid-template-columns:1.1fr 1fr .8fr .7fr;gap:.3rem;padding:.3rem .42rem;margin:.18rem 0;border-radius:6px;background:#092a3b;font-size:.68rem;white-space:nowrap}.riskbar{height:9px;background:#d5e0ea;border-radius:8px;margin:.5rem 0}.riskfill{height:100%;background:linear-gradient(90deg,#00d5ab,#00a5e8);border-radius:8px}.stPlotlyChart{border-radius:9px;overflow:hidden}
/* Light blue-gray theme: dark text remains readable across cards, tabs and widgets. */
.stApp{background:linear-gradient(135deg,#eaf3f8 0%,#dce9f1 55%,#e7f0f5 100%)!important;color:#17324a!important}
h1,h2,h3,h4,p,span,label,small,strong{color:#17324a!important}
.hero p,.hero small{color:#405a70!important}
.panel{background:linear-gradient(145deg,rgba(250,253,255,.98),rgba(234,244,250,.98))!important;border-color:#3aaec2!important;box-shadow:0 5px 16px rgba(36,76,101,.12)!important}
.panel-title{color:#16364d!important}.panel small{color:#4a6174!important}
.mini-kpi{background:linear-gradient(135deg,#f8fcff,#e6f2f8)!important;border-color:#55aabc!important;border-left-color:#08aeca!important}
.mini-kpi,.mini-kpi *{color:#17324a!important}.mini-label{color:#496277!important}.mini-value{color:#102e44!important}
.pill{background:#d9f1e9!important;border-color:#55af8a!important;color:#174d3b!important}.pill.blue{background:#dcecff!important;border-color:#66a6dd!important;color:#18466c!important}.pill.warn{background:#fff1cf!important;border-color:#d3ad52!important;color:#60480e!important}
.signal{background:#e0f4ed!important;border-color:#71b99d!important;color:#174b39!important}
.health-line,.health-line *{color:#17324a!important}.health-track{background:#c9d9e3!important}
.stTabs [data-baseweb="tab"],.stTabs [data-baseweb="tab"][aria-selected="true"]{color:#17324a!important}.stTabs button[role="tab"] p{color:inherit!important}
</style>
""", unsafe_allow_html=True)

def initialize_database():
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("""
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
                Power_kW REAL,
                Machine_Health REAL
            )
        """)
        columns = {
            column[1] for column in conn.execute("PRAGMA table_info(production)")
        }
        if "Machine_Health" not in columns:
            conn.execute(
                "ALTER TABLE production ADD COLUMN Machine_Health REAL DEFAULT 100"
            )
        conn.execute("""
            CREATE TABLE IF NOT EXISTS demo_state (
                key TEXT PRIMARY KEY,
                value TEXT NOT NULL
            )
        """)

        if conn.execute("SELECT COUNT(*) FROM production").fetchone()[0] == 0:
            rng = random.Random(42)
            rows = []
            production_count = 0
            machine_health = 100.0
            start_time = datetime.now()

            for index in range(120):
                machine_status = rng.choices(
                    ["Running", "Idle", "Maintenance", "Fault"],
                    weights=[90, 5, 3, 2],
                )[0]
                if machine_status == "Running":
                    production_count += 1
                    machine_health -= 0.02
                    conveyor_speed = round(rng.uniform(0.90, 1.20), 2)
                    cycle_time = round(rng.uniform(1.8, 2.4), 2)
                    power = round(2 + conveyor_speed * 1.5, 2)
                elif machine_status == "Idle":
                    machine_health -= 0.005
                    conveyor_speed = round(rng.uniform(0.10, 0.40), 2)
                    cycle_time = 0.0
                    power = round(rng.uniform(0.8, 1.5), 2)
                else:
                    machine_health += (
                        0.10 if machine_status == "Maintenance" else -0.20
                    )
                    conveyor_speed = 0.0
                    cycle_time = 0.0
                    power = round(rng.uniform(0.2, 0.8), 2)
                machine_health = max(0.0, min(100.0, machine_health))
                temperature = round(28 + power * 3 + rng.uniform(-1, 1), 1)
                inspection = (
                    "Defect"
                    if machine_status == "Fault" and rng.random() < 0.7
                    else "Pass"
                )
                robot_status = "Active" if machine_status == "Running" else "Idle"
                packing_status = (
                    "Running" if machine_status == "Running" else "Waiting"
                )
                timestamp = start_time - timedelta(seconds=2 * (119 - index))
                rows.append((
                    timestamp.strftime("%Y-%m-%d %H:%M:%S"),
                    production_count,
                    machine_status,
                    robot_status,
                    inspection,
                    packing_status,
                    temperature,
                    conveyor_speed,
                    cycle_time,
                    power,
                    round(machine_health, 2),
                ))

            conn.executemany("""
                INSERT INTO production
                (Time, Production_Count, Machine_Status, Robot_Status, Inspection,
                 Packing_Status, Temperature, Conveyor_Speed, Cycle_Time, Power_kW,
                 Machine_Health)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, rows)

def append_demo_reading():
    with sqlite3.connect(DB_PATH, timeout=10) as conn:
        conn.execute("BEGIN IMMEDIATE")
        latest = conn.execute("""
            SELECT Production_Count, Machine_Health
            FROM production
            ORDER BY rowid DESC
            LIMIT 1
        """).fetchone()
        production_count = int(latest[0] or 0)
        machine_health = float(latest[1] if latest[1] is not None else 100.0)
        maintenance_row = conn.execute(
            "SELECT value FROM demo_state WHERE key = 'maintenance_until'"
        ).fetchone()
        maintenance_until = (
            datetime.strptime(maintenance_row[0], "%Y-%m-%d %H:%M:%S")
            if maintenance_row
            else None
        )
        maintenance_active = (
            maintenance_until is not None and datetime.now() < maintenance_until
        )
        machine_status = (
            "Maintenance"
            if maintenance_active
            else random.choices(
                ["Running", "Idle", "Maintenance", "Fault"],
                weights=[90, 5, 3, 2],
            )[0]
        )
        if maintenance_active:
            machine_health = 100.0
        if machine_status == "Running":
            production_count += 1
            machine_health -= 0.02
            conveyor_speed = round(random.uniform(0.90, 1.20), 2)
            cycle_time = round(
                random.uniform(1.8, 2.4)
                if machine_health > 80
                else random.uniform(2.6, 3.4)
                if machine_health > 60
                else random.uniform(3.6, 4.5)
                if machine_health > 40
                else random.uniform(4.8, 6.0),
                2,
            )
            power = round(2 + conveyor_speed * 1.5, 2)
            robot_status = random.choices(["Active", "Idle"], weights=[95, 5])[0]
            packing_status = "Running"
        elif machine_status == "Idle":
            machine_health -= 0.005
            conveyor_speed = round(random.uniform(0.10, 0.40), 2)
            cycle_time = 0.0
            power = round(random.uniform(0.8, 1.5), 2)
            robot_status = "Idle"
            packing_status = "Waiting"
        elif machine_status == "Maintenance":
            machine_health += 0.10
            conveyor_speed = 0.0
            cycle_time = 0.0
            power = round(random.uniform(0.2, 0.8), 2)
            robot_status = "Offline"
            packing_status = "Stopped"
        else:
            machine_health -= 0.20
            conveyor_speed = 0.0
            cycle_time = 0.0
            power = round(random.uniform(0.2, 0.8), 2)
            robot_status = "Offline"
            packing_status = "Stopped"

        machine_health = max(0.0, min(100.0, machine_health))
        temperature = round(28 + power * 3 + random.uniform(-1, 1), 1)
        if maintenance_active:
            inspection = "Pass"
        elif machine_status == "Fault":
            inspection = random.choices(["OK", "Defect"], weights=[30, 70])[0]
        elif machine_status == "Maintenance":
            inspection = "Defect"
        else:
            defect_chance = min(3 + (100 - machine_health) * 0.3, 50)
            inspection = random.choices(
                ["OK", "Defect"],
                weights=[100 - defect_chance, defect_chance],
            )[0]

        conn.execute("""
            INSERT INTO production
            (Time, Production_Count, Machine_Status, Robot_Status, Inspection,
             Packing_Status, Temperature, Conveyor_Speed, Cycle_Time, Power_kW,
             Machine_Health)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
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
            round(machine_health, 2),
        ))
        conn.execute("""
            DELETE FROM production
            WHERE rowid NOT IN (
                SELECT rowid FROM production ORDER BY rowid DESC LIMIT 2000
            )
        """)

def perform_maintenance():
    now = datetime.now()
    maintenance_until = now + timedelta(seconds=30)
    with sqlite3.connect(DB_PATH, timeout=10) as conn:
        conn.execute("BEGIN IMMEDIATE")
        latest = conn.execute("""
            SELECT Production_Count
            FROM production
            ORDER BY rowid DESC
            LIMIT 1
        """).fetchone()
        production_count = int(latest[0] or 0)
        conn.execute("""
            INSERT INTO demo_state (key, value)
            VALUES ('maintenance_until', ?)
            ON CONFLICT(key) DO UPDATE SET value = excluded.value
        """, (maintenance_until.strftime("%Y-%m-%d %H:%M:%S"),))
        conn.execute("""
            INSERT INTO production
            (Time, Production_Count, Machine_Status, Robot_Status, Inspection,
             Packing_Status, Temperature, Conveyor_Speed, Cycle_Time, Power_kW,
             Machine_Health)
            VALUES (?, ?, 'Maintenance', 'Offline', 'Pass', 'Stopped',
                    30, 0, 0, 0.5, 100)
        """, (now.strftime("%Y-%m-%d %H:%M:%S"), production_count))
        conn.execute("""
            DELETE FROM production
            WHERE rowid NOT IN (
                SELECT rowid FROM production ORDER BY rowid DESC LIMIT 2000
            )
        """)

def load_data():
   with sqlite3.connect(DB_PATH) as conn:
       return pd.read_sql_query("SELECT * FROM production ORDER BY rowid", conn)

@st.cache_data
def load_obj_mesh(obj_file):
    """Read a Wavefront OBJ and its MTL colors for an interactive Plotly mesh."""
    material_colors = {}
    mtl_file = Path(obj_file).with_suffix(".mtl")
    if mtl_file.exists():
        current_material = None
        with mtl_file.open(encoding="utf-8", errors="ignore") as source:
            for line in source:
                parts = line.split()
                if len(parts) >= 2 and parts[0] == "newmtl":
                    current_material = parts[1]
                elif len(parts) >= 4 and parts[0] == "Kd" and current_material:
                    rgb = [max(0, min(255, round(float(value) * 255))) for value in parts[1:4]]
                    material_colors[current_material] = "#%02x%02x%02x" % tuple(rgb)

    vertices, triangles, face_colors = [], [], []
    active_color = "#b8c6d1"
    with Path(obj_file).open(encoding="utf-8", errors="ignore") as source:
        for line in source:
            parts = line.split()
            if not parts:
                continue
            if parts[0] == "v" and len(parts) >= 4:
                vertices.append(tuple(float(value) for value in parts[1:4]))
            elif parts[0] == "usemtl" and len(parts) >= 2:
                active_color = material_colors.get(parts[1], "#b8c6d1")
            elif parts[0] == "f" and len(parts) >= 4:
                face = []
                for item in parts[1:]:
                    vertex_index = int(item.split("/", 1)[0])
                    face.append(vertex_index - 1 if vertex_index > 0 else len(vertices) + vertex_index)
                for index in range(1, len(face) - 1):
                    triangles.append((face[0], face[index], face[index + 1]))
                    face_colors.append(active_color)
    return vertices, triangles, face_colors

@st.cache_resource
def build_cad_figure(obj_file):
    vertices, triangles, face_colors = load_obj_mesh(obj_file)
    if not vertices or not triangles:
        return None
    cad = go.Figure(go.Mesh3d(
        x=[point[0] for point in vertices],
        y=[point[1] for point in vertices],
        z=[point[2] for point in vertices],
        i=[face[0] for face in triangles],
        j=[face[1] for face in triangles],
        k=[face[2] for face in triangles],
        facecolor=face_colors,
        flatshading=True,
        lighting=dict(ambient=0.68, diffuse=0.82, specular=0.18, roughness=0.7),
        hoverinfo="skip",
        name="Assembly line CAD",
    ))
    cad.update_layout(
        height=430,
        margin=dict(l=0, r=0, t=0, b=0),
        paper_bgcolor="rgba(0,0,0,0)",
        showlegend=False,
        uirevision="assembly-cad",
        scene=dict(
            xaxis=dict(visible=False),
            yaxis=dict(visible=False),
            zaxis=dict(visible=False),
            aspectmode="data",
            bgcolor="rgba(0,0,0,0)",
            camera=dict(eye=dict(x=1.5, y=1.5, z=1.1)),
        ),
    )
    return cad

def card(icon,label,value,style=""):
    return f'<div class="kpi {style}"><div class="kpi-label">{icon} &nbsp;{label}</div><div class="kpi-value">{value}</div></div>'

with st.sidebar:
    st.markdown('<div class="brand"><div class="brand-icon">🏭</div><div class="brand-title">Smart Factory<br>Digital Twin</div><div class="brand-sub">Manufacturing Assembly Line</div></div>',unsafe_allow_html=True)
    for item in ["⌂  Dashboard","▥  Factory View","🤖  AI Maintenance","⌁  Data Analysis","▣  Data Logs","⚙  Settings"]:
        st.button(item,width="stretch")
    st.markdown(f'<b>System Status</b><br><br>🟢 Factory Online<br>🗄️ Database: SQLite<br>◷ Last Update<br>&nbsp;&nbsp;{datetime.now().strftime("%d-%b-%Y %H:%M:%S")}',unsafe_allow_html=True)

initialize_database()
append_demo_reading()
df=load_data()
if df.empty: st.error("No factory data is available."); st.stop()
latest=df.iloc[-1]; health=float(latest["Machine_Health"])
production=int(latest["Production_Count"]); power=float(latest["Power_kW"]); temp=float(latest["Temperature"])
speed=float(latest["Conveyor_Speed"]); cycle=float(latest["Cycle_Time"])
total=len(df); availability=df["Machine_Status"].eq("Running").mean()*100 if total else 0
performance=random.uniform(88,94) if health>=60 else random.uniform(70,82)
quality=df["Inspection"].ne("Defect").mean()*100 if total else 0
oee=availability*performance*quality/10000; risk=max(0.0,100-health)
factory_state = (
    "🛠  Maintenance in Progress"
    if latest["Machine_Status"] == "Maintenance"
    else "🏭  Factory Online"
)
factory_label = (
    "🟡 Maintenance in progress"
    if latest["Machine_Status"] == "Maintenance"
    else "🟢 Factory Online"
)
robot_state = (
    f"🤖  Robot {latest['Robot_Status']}"
)
risk_message, risk_background, risk_border = (
    ("🟢 Low estimated risk. Continue routine monitoring.", "#d9f1e6", "#79bb9a")
    if risk < 25
    else ("🟡 Moderate estimated risk. Review the latest machine signals.", "#fff1cf", "#d3ad52")
    if risk < 60
    else ("🔴 Elevated estimated risk. Schedule a maintenance review.", "#fbe3e3", "#d47a7a")
)

st.markdown(f'<div class="hero"><h1>🏭 SMART FACTORY DIGITAL TWIN</h1><p>Industry 4.0 Manufacturing Monitoring System</p><small>{factory_label} &nbsp;&nbsp; 🕒 {datetime.now().strftime("%d-%m-%Y %H:%M:%S")}</small></div>',unsafe_allow_html=True)
caption_col, maintenance_col = st.columns([8, 2], vertical_alignment="center")
with caption_col:
    st.caption("Live simulated demo · readings update automatically · not connected to real equipment")
with maintenance_col:
    if st.button(
        "🛠 Perform Maintenance",
        type="primary",
        width="stretch",
        help="Starts a 30-second simulated maintenance interval visible to all visitors. No real equipment is controlled.",
    ):
        perform_maintenance()
        st.rerun()

for col,text,cls in zip(st.columns(5),["🟢  Connected",robot_state,factory_state,"⚡  Power Stable","🟢  Database OK"],["","blue","warn" if latest["Machine_Status"] == "Maintenance" else "","",""]):
    col.markdown(f'<div class="pill {cls}" style="text-align:left;padding-left:.8rem">{text}</div>',unsafe_allow_html=True)
st.write("")

overview_tab, floor_tab, analytics_tab, maintenance_tab, logs_tab = st.tabs([
    "📊 Overview", "🏭 Factory & Equipment", "📈 Analytics", "🤖 AI Maintenance", "🧾 Data Logs"
])

with overview_tab:
    top_left,top_right=st.columns([1.02,1])
    with top_left:
        st.markdown(f'''<div class="panel"><div class="panel-title">🧠 &nbsp; AI Predictive Maintenance</div>
        <div style="display:flex;gap:.6rem;align-items:center"><div class="mini-kpi" style="flex:1"><div class="mini-label">Estimated Failure Risk</div><div class="mini-value">{risk:.1f}%</div></div>
        <div style="flex:1;border:1px solid {risk_border};background:{risk_background};color:#174b39;border-radius:9px;padding:.65rem;font-size:.82rem">{risk_message}</div></div>
        <div class="riskbar"><div class="riskfill" style="width:{max(4,100-risk)}%"></div></div><small>Prototype prediction based on synthetic training data. This estimate is not validated for real industrial equipment.</small></div>''',unsafe_allow_html=True)
        for col,args in zip(st.columns(4),[("📦","Products Produced",f"{production:,}"),("🩺","Machine Health",f"{health:.1f}%"),("⚡","Power",f"{power:.1f} kW"),("🌡️","Temperature",f"{temp:.1f} °C")]):
            col.markdown(f'<div class="mini-kpi"><div class="mini-label">{args[0]} {args[1]}</div><div class="mini-value">{args[2]}</div></div>',unsafe_allow_html=True)
    with top_right:
        st.markdown('<div class="panel"><div class="panel-title">📊 &nbsp; Overall Equipment Effectiveness (OEE)</div>',unsafe_allow_html=True)
        for col,(label,value,icon) in zip(st.columns(4),[("Availability",availability,"🟢"),("Performance",performance,"⚙️"),("Quality",quality,"✅"),("OEE",oee,"🏆")]):
            col.markdown(f'<div class="mini-kpi" style="min-height:64px"><div class="mini-label">{icon} {label}</div><div class="mini-value">{value:.2f}%</div></div>',unsafe_allow_html=True)
        st.markdown(f'<div class="signal">🟡 &nbsp; {"Production Performance Needs Improvement" if oee < 85 else "Production Performance On Target"}</div></div>',unsafe_allow_html=True)
        alarms=st.columns(4)
        for col,text,cls in zip(alarms,["🟢 No Critical Alarm","⚠️ Inspection Delay","🌡 Temp Normal","🤖 Robot OK"],["","warn","",""]): col.markdown(f'<div class="pill {cls}" style="font-size:.75rem;padding:.4rem">{text}</div>',unsafe_allow_html=True)

    st.write("")
    chart_data=df.tail(80)
    chart_specs=[("📊 Production Trend","Production_Count","Production Count","#05a8ff"),("🌡️ Temperature","Temperature","Temperature (°C)","#04bff0"),("⚡ Power (kW)","Power_kW","Power (kW)","#069ce7")]
    for col,(title,field,ytitle,color) in zip(st.columns(3),chart_specs):
        with col:
            st.markdown(f'<div class="panel"><div class="panel-title">{title}</div>',unsafe_allow_html=True)
            fig=go.Figure(go.Scatter(x=chart_data["Time"],y=chart_data[field],mode="lines",line=dict(color=color,width=2.5),fill="tozeroy",fillcolor="rgba(0,170,255,.08)"))
            fig.update_layout(height=190,margin=dict(l=35,r=8,t=4,b=24),paper_bgcolor="rgba(0,0,0,0)",plot_bgcolor="rgba(0,0,0,0)",font_color="#17324a",showlegend=False,xaxis=dict(showgrid=False,showline=True,linecolor="#8aa4b5",tickfont=dict(size=9,color="#38566d")),yaxis=dict(title=dict(text=ytitle,font=dict(size=9,color="#38566d")),showgrid=True,gridcolor="#cfdee7",tickfont=dict(size=9,color="#38566d")))
            st.plotly_chart(fig,width="stretch",config={"displayModeBar":False})
            st.markdown('</div>',unsafe_allow_html=True)


with floor_tab:
    equipment_col,view_col,status_col=st.columns([.75,1.45,1.35])
    with equipment_col:
        st.markdown('<div class="panel"><div class="panel-title">🦾 &nbsp; Equipment Information</div><div class="signal">🟢 &nbsp; Assembly Station</div>',unsafe_allow_html=True)
        for label,value in [("Machine Status",latest["Machine_Status"]),("Machine Health",f"{health:.1f}%"),("Temperature",f"{temp:.1f} °C"),("Cycle Time",f"{cycle:.2f} sec")]:
            st.markdown(f'<div class="mini-kpi" style="margin:.4rem 0"><div class="mini-label">{label}</div><div class="mini-value">{value}</div></div>',unsafe_allow_html=True)
        st.markdown('</div>',unsafe_allow_html=True)
    with view_col:
        st.markdown('<div class="panel"><div class="panel-title">📦 &nbsp; Interactive Assembly Digital Twin</div><small>Factory floor overview · live equipment readings update automatically</small>',unsafe_allow_html=True)
        cad_path = ROOT / "images" / "Assembly Digital Twin Final.obj"
        if cad_path.exists():
            cad = build_cad_figure(str(cad_path))
            if cad is not None:
                st.plotly_chart(cad, width="stretch", config={"displayModeBar": True, "scrollZoom": True})
                st.caption("Drag to rotate · scroll to zoom · use the toolbar to reset the view")
            else:
                st.warning("The CAD file was found but did not contain renderable geometry.")
        else:
            st.warning("Assembly Digital Twin Final.obj was not found in the images folder.")
        st.markdown('</div>',unsafe_allow_html=True)
    with status_col:
        st.markdown('<div class="panel"><div class="panel-title">🟢 &nbsp; Live Factory Status</div>',unsafe_allow_html=True)
        for label,state in [("Conveyor Belt",latest["Machine_Status"]),("Assembly Station",latest["Machine_Status"]),("Robot Arm",latest["Robot_Status"]),("Inspection Station",latest["Inspection"]),("Packing Station",latest["Packing_Status"])]: st.markdown(f'<div class="signal">🟢 &nbsp; {label}: {state}</div>',unsafe_allow_html=True)
        st.markdown('</div><div class="panel"><div class="panel-title">📋 &nbsp; Equipment Health Details</div>',unsafe_allow_html=True)
        for label,val in [("Assembly",health),("Robot",health-2),("Conveyor",health-4),("Inspection",health-3),("Packing",health-1)]: st.markdown(f'<div class="health-line"><span>{label}</span><div class="health-track"><div class="health-fill" style="width:{max(0,min(100,val))}%"></div></div><b>{val:.1f}%</b></div>',unsafe_allow_html=True)
        st.markdown('</div>',unsafe_allow_html=True)

    with st.expander("Recent factory events",expanded=False):
        st.dataframe(df.tail(5).iloc[::-1],width="stretch",hide_index=True)


    st.subheader("Current equipment readings")
    st.dataframe(pd.DataFrame({
        "Metric": ["Production count", "Temperature", "Power", "Conveyor speed", "Cycle time"],
        "Value": [f"{production:,}", f"{temp:.1f} °C", f"{power:.2f} kW", f"{speed:.2f} m/s", f"{cycle:.2f} s"],
        "Status": ["Running" if latest["Machine_Status"] == "Running" else "Review"] * 5,
    }), width="stretch", hide_index=True)

with analytics_tab:
    st.subheader("Production and quality analytics")
    chart_left, chart_right = st.columns(2)
    with chart_left:
        st.plotly_chart(px.line(df.tail(250), x="Time", y="Production_Count", title="Production count", markers=True), width="stretch")
        st.plotly_chart(px.line(df.tail(250), x="Time", y="Machine_Health", title="Machine health (%)", color_discrete_sequence=["#18d88c"]), width="stretch")
    with chart_right:
        st.plotly_chart(px.line(df.tail(250), x="Time", y="Temperature", title="Temperature (°C)", color_discrete_sequence=["#ff9418"]), width="stretch")
        st.plotly_chart(px.line(df.tail(250), x="Time", y="Power_kW", title="Power consumption (kW)", color_discrete_sequence=["#a77bff"]), width="stretch")
    dist_left, dist_right = st.columns(2)
    with dist_left:
        st.plotly_chart(px.histogram(df, x="Machine_Status", color="Machine_Status", title="Machine status distribution"), width="stretch")
    with dist_right:
        st.plotly_chart(px.scatter(df.tail(250), x="Temperature", y="Power_kW", color="Machine_Status", title="Temperature vs power"), width="stretch")

with maintenance_tab:
    st.subheader("AI predictive maintenance")
    risk = max(0.0, 100.0 - health)
    risk_a, risk_b, risk_c = st.columns(3)
    risk_a.metric("Estimated failure risk", f"{risk:.1f}%")
    risk_b.metric("Machine health", f"{health:.1f}%")
    risk_c.metric("Inspection quality", f"{quality:.1f}%")
    st.progress(min(1.0, risk / 100.0))
    st.info("Use this view to review the latest signals before scheduling an intervention.")
    st.dataframe(pd.DataFrame({
        "Signal": ["Temperature", "Power", "Cycle time", "Inspection", "Robot status"],
        "Latest value": [f"{temp:.1f} °C", f"{power:.2f} kW", f"{cycle:.2f} s", latest["Inspection"], latest["Robot_Status"]],
        "Assessment": ["Normal" if temp < 45 else "Review", "Normal" if power < 6 else "Review", "Normal" if cycle < 3 else "Review", "Pass" if latest["Inspection"] in ["OK", "Pass"] else "Review", "Ready" if latest["Robot_Status"] in ["Active", "Running"] else "Review"],
    }), width="stretch", hide_index=True)

with logs_tab:
    st.subheader("Production data logs")
    st.caption("Recent production records. Turn on all columns to inspect the complete set of machine readings.")
    show_all_log_columns = st.toggle("Show all columns", value=False, key="show_all_factory_log_columns")
    log_view = df.tail(500).iloc[::-1]
    if not show_all_log_columns:
        log_view = log_view[["Time", "Production_Count", "Machine_Status", "Machine_Health"]]
    log_columns = {
        "Time": st.column_config.TextColumn("Time", width="small"),
        "Production_Count": st.column_config.NumberColumn("Products", width="small", format="%d"),
        "Machine_Status": st.column_config.TextColumn("Status", width="small"),
        "Machine_Health": st.column_config.NumberColumn("Health %", width="small", format="%.1f"),
    }
    st.dataframe(log_view, width="stretch", hide_index=True, column_config=log_columns)
    st.download_button("⬇ Download factory logs", df.to_csv(index=False), "factory_logs.csv", "text/csv")
