import os
import sys

directory = r"d:\Profolio\Language-as-being\Thesis"

renames = {
    "datalab-output-1-s2.0-S1075293524001028-main.pdf.md": "A meta-analysis of relationships between syntactic features and writing performance.md",
    "datalab-output-applsci-12-07518-v2.pdf.md": "Post-Authorship Attribution Using Regularized Deep Neural Network.md",
    "datalab-output-A_Survey_on_Stylometric_Text_Features.pdf.md": "A Survey on Stylometric Text Features.md",
    "datalab-output-jss_2021120615293486.pdf.md": "A Stylometric Investigation of Linguistic Styles Based on a Vietnamese Corpus.md",
    "lind-et-al-2024-narrative-identity-traits-and-trajectories-of-depression-and-well-being-a-9-year-longitudinal-study.pdf.md": "Narrative Identity, Traits, and Trajectories of Depression and Well-Being A 9-Year Longitudinal Study.md",
    "PersSocPsycholRev2016Adler.pdf.md": "The Incremental Validity of Narrative Identity in Predicting Well-Being.md",
    "Psychobiography-AP.pdf.md": "Psychobiography Theory and Method.md",
    "the-empirical-structure-of-narrative-identity-the-initial.md": "The Empirical Structure of Narrative Identity The Initial Big Three.md"
}

# The following are already correct or similar, checking logic:
# "The contemporary theory of metaphor.md" -> "The contemporary theory of metaphor — now new and improved!.md"
# I'll stick to the simpler current name for metaphor if it exists, or rename if requested to match title strictly.
# The user said "change title to paper title".
renames["The contemporary theory of metaphor.md"] = "The contemporary theory of metaphor — now new and improved!.md"
# Distinguishing... is already correct.

log_path = r"d:\Profolio\Language-as-being\rename_execution.log"

def log(msg):
    with open(log_path, "a", encoding="utf-8") as f:
        f.write(msg + "\n")

with open(log_path, "w", encoding="utf-8") as f:
    f.write("Starting Rename...\n")

for old_name, new_name in renames.items():
    old_path = os.path.join(directory, old_name)
    new_path = os.path.join(directory, new_name)
    
    if os.path.exists(old_path):
        try:
            os.rename(old_path, new_path)
            log(f"SUCCESS: {old_name} -> {new_name}")
        except Exception as e:
            log(f"ERROR: Could not rename {old_name}: {e}")
    else:
        log(f"SKIP: {old_name} not found")

log("Done.")
