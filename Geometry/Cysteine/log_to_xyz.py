import sys
import os

# Dictionary to convert Gaussian atomic numbers back to element symbols
# I've included the most common ones for biochemistry/EPR, but you can add more if needed!
PERIODIC_TABLE = {
    1: 'H', 6: 'C', 7: 'N', 8: 'O', 9: 'F', 11: 'Na', 12: 'Mg', 
    14: 'Si', 15: 'P', 16: 'S', 17: 'Cl', 19: 'K', 20: 'Ca', 26: 'Fe'
}

def extract_last_geometry(log_file, xyz_file):
    if not os.path.exists(log_file):
        print(f"Error: The file '{log_file}' was not found.")
        sys.exit(1)

    with open(log_file, 'r') as file:
        lines = file.readlines()

    # 1. Find the index of the last "Standard orientation:"
    last_orient_idx = -1
    for i, line in enumerate(lines):
        if "Standard orientation:" in line:
            last_orient_idx = i

    if last_orient_idx == -1:
        print(f"Error: Could not find 'Standard orientation' in {log_file}.")
        sys.exit(1)

    # 2. Parse the coordinates from that block
    # The actual data starts 5 lines below the header
    start_idx = last_orient_idx + 5
    atoms = []
    
    for i in range(start_idx, len(lines)):
        # The block ends when we hit the next row of dashes
        if "---------------------------------------------------------------------" in lines[i]:
            break
            
        parts = lines[i].split()
        if len(parts) == 6:
            atomic_number = int(parts[1])
            symbol = PERIODIC_TABLE.get(atomic_number, f"X{atomic_number}") # Fallback if not in dict
            
            # Extract X, Y, Z coordinates
            x, y, z = parts[3], parts[4], parts[5]
            atoms.append(f"{symbol:<4} {x:>12} {y:>12} {z:>12}")

    # 3. Write out to the .xyz format
    with open(xyz_file, 'w') as file:
        file.write(f"{len(atoms)}\n")
        file.write(f"Geometry extracted from {log_file}\n")
        for atom in atoms:
            file.write(atom + "\n")
            
    print(f"Success! Extracted {len(atoms)} atoms and saved to {xyz_file}")

if __name__ == "__main__":
    # Check if the right number of arguments are passed
    if len(sys.argv) != 3:
        print("Usage: python3 log_to_xyz.py <input_file.log> <output_file.xyz>")
        sys.exit(1)

    input_log = sys.argv[1]
    output_xyz = sys.argv[2]
    
    extract_last_geometry(input_log, output_xyz)
