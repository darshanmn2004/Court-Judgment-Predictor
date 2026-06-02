# ============================================================
# LEGAL DATASET GENERATOR V6 — 25+ IPCs + Relevant Laws + Similar Cases
# Generates: balanced_final_dataset_v6.csv
# ============================================================

import pandas as pd
import random
from faker import Faker
from itertools import cycle

fake = Faker()
random.seed(42)

# ----------------------------------------------------------------------
# IPC LIST (25+ IPC SECTIONS WITH DESCRIPTIONS)
# ----------------------------------------------------------------------
ipc_facts_mapping = {

    # High Severity
    "302": "murder",
    "304": "culpable homicide not amounting to murder",
    "304B": "dowry death",
    "307": "attempt to murder",
    "376": "rape",
    "364": "kidnapping with intent to murder",
    "392": "robbery",
    "394": "robbery causing hurt",
    "397": "robbery or attempt with deadly weapon",
    "396": "dacoity with murder",

    # Medium Severity
    "420": "cheating and fraud",
    "406": "criminal breach of trust",
    "498A": "cruelty by husband or relatives",
    "326": "grievous hurt using weapon",
    "468": "forgery",
    "471": "using forged documents",
    "354": "outraging modesty of woman",
    "354D": "stalking",
    "509": "insulting modesty of a woman",
    "380": "theft in a dwelling house",
    "411": "dishonest possession of stolen property",
    "489A": "counterfeiting currency",

    # Low Severity
    "379": "theft",
    "341": "wrongful restraint",
    "363": "kidnapping",
    "120B": "criminal conspiracy",
    "323": "voluntarily causing hurt",
    "324": "hurt by dangerous weapon",
    "335": "hurt on provocation",
    "504": "intentional insult",
    "268": "public nuisance",
    "278": "making atmosphere noxious",
    "289": "negligent act with animals"
}

ipc_list = list(ipc_facts_mapping.keys())

# ----------------------------------------------------------------------
# Fact building components
# ----------------------------------------------------------------------
context_events = [
    "a financial dispute", "a neighbourhood argument", "a business conflict",
    "a heated family situation", "a clash during a public event",
    "a long-standing rivalry", "an argument after an accident"
]

evidence_strength = [
    "strong forensic indications", "partial CCTV footage",
    "an inconsistent witness account", "multiple witness statements",
    "limited physical evidence", "digital records being reviewed",
    "no direct forensic match"
]

actions = [
    "injured", "attacked", "threatened", "forced", "followed",
    "misled", "took away", "attempted to harm", "illegally detained",
    "extorted", "harassed"
]

locations = [
    "near the market area", "outside the complainant’s residence",
    "inside a rented property", "near a bus stop",
    "in a semi-crowded locality", "within a moving vehicle",
    "inside a commercial building"
]

outcomes = [
    "minor injuries", "financial loss", "verbal confrontation",
    "temporary distress", "serious injuries", "property damage"
]

# ----------------------------------------------------------------------
# Fact Generators
# ----------------------------------------------------------------------
def generate_guilty_fact(ipc):
    return (
        f"During {random.choice(context_events)}, the accused allegedly "
        f"{random.choice(actions)} the complainant {random.choice(locations)}. "
        f"Case documents indicate {random.choice(evidence_strength)}, and the act "
        f"relates to IPC {ipc} concerning {ipc_facts_mapping[ipc]}. "
        f"The incident resulted in {random.choice(outcomes)}."
    )

def generate_not_guilty_fact(ipc):
    return (
        f"The accused was involved in {random.choice(context_events)}, but the available "
        f"materials show {random.choice(evidence_strength)}. The allegation under IPC {ipc} "
        f"({ipc_facts_mapping[ipc]}) lacks sufficient evidence. The situation caused "
        f"{random.choice(outcomes)}, but no intention is proven."
    )

# ----------------------------------------------------------------------
# Relevant Laws Generator (multi-label)
# ----------------------------------------------------------------------
def generate_relevant_laws(main_ipc):
    # Always include the main IPC, plus 1–3 extra
    num_extra = random.randint(1, 3)
    extra_laws = random.sample([ipc for ipc in ipc_list if ipc != main_ipc], num_extra)
    return [main_ipc] + extra_laws

# ----------------------------------------------------------------------
# Similar Case Generators
# ----------------------------------------------------------------------
def generate_relevant_case(ipc):
    return (
        f"In an earlier matter involving IPC {ipc}, the court observed "
        f"{random.choice(evidence_strength)} following {random.choice(context_events)}. "
        f"The judgment highlighted the importance of evidence reliability."
    )

def generate_relevant_case_ids():
    return [fake.uuid4() for _ in range(3)]

# ----------------------------------------------------------------------
# Severity + Penalty
# ----------------------------------------------------------------------
high = {
    "302", "304", "304B", "307", "376",
    "364", "392", "394", "397", "396"
}

medium = {
    "420", "406", "498A", "326", "468", "471",
    "354", "354D", "509",
    "380", "411", "489A"
}

def get_severity(ipc):
    if ipc in high:
        return "High"
    if ipc in medium:
        return "Medium"
    return "Low"

def get_penalty(ipc, verdict):
    if verdict == "Not Guilty":
        return 0
    severity = get_severity(ipc)
    if severity == "High": return random.randint(120, 300)
    if severity == "Medium": return random.randint(36, 120)
    return random.randint(6, 36)

# ----------------------------------------------------------------------
# Main Dataset Generation
# ----------------------------------------------------------------------
rows = []
count_guilty = 3500
count_not_guilty = 3500
ipc_cycle = cycle(ipc_list)

for _ in range(count_guilty):
    ipc = next(ipc_cycle)
    laws = generate_relevant_laws(ipc)
    rows.append({
        "case_id": fake.uuid4(),
        "verdict": "Guilty",
        "ipc_section": ipc,
        "relevant_laws": ",".join(laws),
        "case_fact": generate_guilty_fact(ipc),
        "penalty_months": get_penalty(ipc, "Guilty"),
        "severity": get_severity(ipc),
        "similar_case_ids": ",".join(generate_relevant_case_ids()),
        "similar_case_summaries": " || ".join(
            [generate_relevant_case(ipc) for _ in range(3)]
        )
    })

for _ in range(count_not_guilty):
    ipc = next(ipc_cycle)
    laws = generate_relevant_laws(ipc)
    rows.append({
        "case_id": fake.uuid4(),
        "verdict": "Not Guilty",
        "ipc_section": ipc,
        "relevant_laws": ",".join(laws),
        "case_fact": generate_not_guilty_fact(ipc),
        "penalty_months": get_penalty(ipc, "Not Guilty"),
        "severity": get_severity(ipc),
        "similar_case_ids": ",".join(generate_relevant_case_ids()),
        "similar_case_summaries": " || ".join(
            [generate_relevant_case(ipc) for _ in range(3)]
        )
    })

df = pd.DataFrame(rows).sample(frac=1, random_state=42).reset_index(drop=True)
df.to_csv("balanced_final_dataset_v6.csv", index=False)

print("✅ Dataset generated: balanced_final_dataset_v6.csv")
print("Rows:", len(df))
