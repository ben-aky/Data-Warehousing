# generate_datasets.py
# ------------------------------------------------------------
# Creates three CSV files in ./data:
#   - patients.csv
#   - doctors.csv
#   - appointments.csv
#
# IDs are simple unique strings you generate here, and
# appointments re-use those IDs to link the collections.
# ------------------------------------------------------------

from faker import Faker
import pandas as pd
import random
import uuid
from pathlib import Path

# ----------------- settings (adjust if needed) -----------------
N_PATIENTS = 30000
N_DOCTORS  = 10000
N_APPTS    = 50000

# If you want reproducible results while testing, set a seed:
SEED = None  # for example,  42
# ---------------------------------------------------------------

if SEED is not None:
    random.seed(SEED)

fake = Faker()

# Specialties and statuses used in the assignment
SPECIALTIES = [
    "Cardiology", "Dermatology", "Neurology", "Oncology",
    "Pediatrics", "Orthopedics", "General Medicine"
]
STATUSES = ["Scheduled", "Completed", "Cancelled", "Pending"]

# Helper: sometimes return None (so CSV cells are empty)
def maybe(value, p_missing=0.2):
    """Return value or None with probability p_missing."""
    return value if random.random() > p_missing else None

# Ensure output folder exists
out_dir = Path("data")
out_dir.mkdir(parents=True, exist_ok=True)

# --------------------------- Patients --------------------------
patients = []
for _ in range(N_PATIENTS):
    patients.append({
        "patient_id": str(uuid.uuid4()),             # unique string ID (your domain ID)
        "name": fake.name(),
        "age": random.randint(1, 90),
        "gender": random.choice(["Male", "Female"]),
        "phone_number": maybe(fake.phone_number(), p_missing=0.2),  # ~20% missing
        "medical_history": maybe(fake.sentence(), p_missing=0.3)    # ~30% missing
    })

df_patients = pd.DataFrame(patients)
df_patients.to_csv(out_dir / "patients.csv", index=False)

# ---------------------------- Doctors --------------------------
doctors = []
for _ in range(N_DOCTORS):
    doctors.append({
        "doctor_id": str(uuid.uuid4()),              # unique string ID (your domain ID)
        "name": fake.name(),
        "specialty": random.choice(SPECIALTIES),
        "experience_years": random.randint(1, 40)    # 1–40 inclusive
    })

df_doctors = pd.DataFrame(doctors)
df_doctors.to_csv(out_dir / "doctors.csv", index=False)

# -------------------------- Appointments -----------------------
# Link appointments to actual patients and doctors
patient_ids = [p["patient_id"] for p in patients]
doctor_ids  = [d["doctor_id"]  for d in doctors]

appointments = []
for _ in range(N_APPTS):
    appointments.append({
        "appointment_id": str(uuid.uuid4()),         # unique string ID (your domain ID)
        "patient_id": random.choice(patient_ids),    # must match a patients.csv patient_id
        "doctor_id": random.choice(doctor_ids),      # must match a doctors.csv doctor_id
        "status": random.choice(STATUSES)
    })

df_appts = pd.DataFrame(appointments)
df_appts.to_csv(out_dir / "appointments.csv", index=False)

# -------------------------- Summary ----------------------------
print("Generated CSV files in ./data")
print(f" patients.csv rows: {len(df_patients)}")
print(f" doctors.csv rows: {len(df_doctors)}")
print(f" appointments.csv rows: {len(df_appts)}")

#uncomment the following lines if you want to preview in the console

# print("\nPatients (head):")
# print(df_patients.head(3))
# print("\nDoctors (head):")
# print(df_doctors.head(3))
# print("\nAppointments (head):")
# print(df_appts.head(3))