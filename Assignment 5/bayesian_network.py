
import sys
import warnings

from matplotlib import lines

from matplotlib import lines
warnings.filterwarnings("ignore")

try:
    from pgmpy.models import DiscreteBayesianNetwork as BayesianNetwork
    from pgmpy.factors.discrete import TabularCPD
    from pgmpy.inference import VariableElimination, BeliefPropagation
except ImportError:
    print("pgmpy library is required to run this code. Please install it using:")
    print("  pip install pgmpy")
    sys.exit(1)
from typing import Dict, Optional


# BUILD THE BAYESIAN NETWORK 

def build_flu_bayesian_network() -> BayesianNetwork:
    """
    Build and return a Flu Diagnosis Bayesian Network.

    DAG edges:
        Season  → Flu
        Flu     → Fever
        Flu     → Cough
        Flu     → Fatigue

    Variable encoding:
        Season  : 0 = Winter,  1 = Other
        Flu     : 0 = Yes,     1 = No
        Fever   : 0 = Yes,     1 = No
        Cough   : 0 = Yes,     1 = No
        Fatigue : 0 = Yes,     1 = No
    """
    model = BayesianNetwork([
        ("Season", "Flu"),
        ("Flu",    "Fever"),
        ("Flu",    "Cough"),
        ("Flu",    "Fatigue"),
    ])

    # P(Season)
    # Season: 0=Winter (30% of year), 1=Other (70%)
    cpd_season = TabularCPD(
        variable="Season",
        variable_card=2,
        values=[[0.30],   # P(Season=Winter)
                [0.70]],  # P(Season=Other)
        state_names={"Season": ["Winter", "Other"]}
    )

    # P(Flu | Season)
    # In Winter, flu probability is 20%; otherwise 5%
    #           Season=Winter  Season=Other
    # Flu=Yes       0.20           0.05
    # Flu=No        0.80           0.95
    cpd_flu = TabularCPD(
        variable="Flu",
        variable_card=2,
        values=[[0.20, 0.05],
                [0.80, 0.95]],
        evidence=["Season"],
        evidence_card=[2],
        state_names={
            "Flu":    ["Yes", "No"],
            "Season": ["Winter", "Other"]
        }
    )

    # P(Fever | Flu)
    # Flu patients have 80% chance of fever; non-flu 10%

    #              Flu=Yes  Flu=No
    # Fever=Yes     0.80    0.10
    # Fever=No      0.20    0.90
    cpd_fever = TabularCPD(
        variable="Fever",
        variable_card=2,
        values=[[0.80, 0.10],
                [0.20, 0.90]],
        evidence=["Flu"],
        evidence_card=[2],
        state_names={
            "Fever": ["Yes", "No"],
            "Flu":   ["Yes", "No"]
        }
    )

    # P(Cough | Flu)
    # Flu → cough with 70% probability; non-flu 20%
    cpd_cough = TabularCPD(
        variable="Cough",
        variable_card=2,
        values=[[0.70, 0.20],
                [0.30, 0.80]],
        evidence=["Flu"],
        evidence_card=[2],
        state_names={
            "Cough": ["Yes", "No"],
            "Flu":   ["Yes", "No"]
        }
    )

    # P(Fatigue | Flu)
    # Flu → fatigue with 60% probability; non-flu 15%
    cpd_fatigue = TabularCPD(
        variable="Fatigue",
        variable_card=2,
        values=[[0.60, 0.15],
                [0.40, 0.85]],
        evidence=["Flu"],
        evidence_card=[2],
        state_names={
            "Fatigue": ["Yes", "No"],
            "Flu":     ["Yes", "No"]
        }
    )

    model.add_cpds(cpd_season, cpd_flu, cpd_fever, cpd_cough, cpd_fatigue)

    #Validate the model
    assert model.check_model(), "BN model is invalid!"

    return model


class FluDiagnosisSystem:
    """
    Medical Diagnosis System backed by the Flu Bayesian Network.

    Supports two inference algorithms:
      1. Variable Elimination (exact, algebraic)
      2. Belief Propagation   (exact on trees / polytrees)
    """

    def __init__(self):
        self.model = build_flu_bayesian_network()
        self.ve    = VariableElimination(self.model)   # exact inference

    def diagnose(self, evidence: Dict[str, str],
                 query_variable: str = "Flu") -> dict:
        """
        Compute posterior probability of query_variable given evidence.

        Args:
            evidence       : dict mapping variable name → observed state
                             e.g. {"Fever": "Yes", "Cough": "Yes"}
            query_variable : variable to query (default: "Flu")

        Returns:
            dict: {"Yes": prob, "No": prob}
        """
        result = self.ve.query(
            variables=[query_variable],
            evidence=evidence,
            show_progress=False
        )
        states = result.state_names[query_variable]
        probs  = result.values
        return dict(zip(states, probs))

    def full_inference(self, evidence: Dict[str, str]) -> dict:
        """
        Run inference for ALL unobserved variables given evidence.

        Returns:
            dict mapping variable name → {state: probability}
        """
        all_vars = list(self.model.nodes())
        results  = {}
        for var in all_vars:
            if var not in evidence:
                try:
                    result = self.ve.query(
                        variables=[var],
                        evidence=evidence,
                        show_progress=False
                    )
                    states = result.state_names[var]
                    probs  = result.values
                    results[var] = dict(zip(states, probs))
                except Exception:
                    pass  # skip if query fails
        return results

    def explain(self, evidence: Dict[str, str]) -> str:
        """
        Human-readable diagnosis report.
        """
        flu_probs = self.diagnose(evidence, "Flu")
        flu_yes   = flu_probs.get("Yes", 0)
        flu_no    = flu_probs.get("No", 1)

        lines = []
        lines.append("BAYESIAN FLU DIAGNOSIS REPORT")
        lines.append("Observed Symptoms:")
        for var, state in evidence.items():
            lines.append(f"  • {var}: {state}")
        lines.append("")
        lines.append("Posterior Probabilities:")
        lines.append(f"  P(Flu = Yes | evidence) = {flu_yes:.4f}  ({flu_yes*100:.1f}%)")
        lines.append(f"  P(Flu = No  | evidence) = {flu_no:.4f}  ({flu_no*100:.1f}%)")
        lines.append("")

        if flu_yes >= 0.70:
            verdict = "HIGH probability of Flu. Medical attention recommended."
        elif flu_yes >= 0.40:
            verdict = "MODERATE probability of Flu. Monitor symptoms closely."
        else:
            verdict = "LOW probability of Flu. Likely a non-flu illness."

        lines.append(f"Verdict: {verdict}")
        return "\n".join(lines)


#DEMO

if __name__ == "__main__":
    system = FluDiagnosisSystem()

    print("BAYESIAN NETWORK: FLU DIAGNOSIS SYSTEM")

    print("\n[Model Structure]")
    print(f"  Nodes : {list(system.model.nodes())}")
    print(f"  Edges : {list(system.model.edges())}")

    # ── Case 1: Fever + Cough + Winter ─────────────────────
    print("\n\nCASE 1: Patient has Fever, Cough, in Winter season")
    evidence1 = {"Fever": "Yes", "Cough": "Yes", "Season": "Winter"}
    print(system.explain(evidence1))

    # ── Case 2: No symptoms, summer ───────────────────────
    print("CASE 2: No symptoms, not Winter")
    evidence2 = {"Fever": "No", "Cough": "No", "Season": "Other"}
    print(system.explain(evidence2))

    # ── Case 3: Fever only ─────────────────────────────────
    print("CASE 3: Fever only (no other info)")
    evidence3 = {"Fever": "Yes"}
    print(system.explain(evidence3))

    # ── Case 4: All three symptoms ─────────────────────────
    print("CASE 4: Fever + Cough + Fatigue (worst case)")
    evidence4 = {"Fever": "Yes", "Cough": "Yes", "Fatigue": "Yes"}
    print(system.explain(evidence4))

    # ── Prior (no evidence) ────────────────────────────────
    print("CASE 5: No evidence (prior probability of Flu)")
    prior = system.diagnose({}, "Flu")
    print(f"  P(Flu=Yes) = {prior.get('Yes', 0):.4f}")
    print(f"  P(Flu=No)  = {prior.get('No',  0):.4f}")