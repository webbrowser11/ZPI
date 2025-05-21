from mpmath import mp
import os

mp.dps = 1_000_010
pi_str = str(mp.pi)

output_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "pi.txt")
with open(output_path, "w") as f:
    f.write(pi_str)

print(f"✅ Pi written to {output_path}")