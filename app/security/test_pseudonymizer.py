from app.security.pseudonymizer import Pseudonymizer


text = """
Nom et prénom : IDRISSI ZINEB
CIN : CIN_001
N° compte : 1234567891234567
Montant : 740 000,00 DHs
"""


pseudonymizer = Pseudonymizer()

# ----------------------------------------------------------
# Pseudonymization
# ----------------------------------------------------------

pseudonymized_text, mapping = pseudonymizer.pseudonymize(text)

print("\n========== ORIGINAL ==========\n")
print(text)

print("\n========== PSEUDONYMIZED ==========\n")
print(pseudonymized_text)

print("\n========== MAPPING ==========\n")
print(mapping)

# ----------------------------------------------------------
# Restoration
# ----------------------------------------------------------

restored_text = pseudonymizer.restore(
    pseudonymized_text
)

print("\n========== RESTORED ==========\n")
print(restored_text)