
import ast
import os
from pathlib import Path
import pkg_resources
import subprocess
import sys

def find_imports_in_file(filepath):
    """Βρίσκει όλα τα imports σε ένα Python αρχείο"""
    with open(filepath, 'r', encoding='utf-8') as file:
        try:
            tree = ast.parse(file.read())
        except SyntaxError:
            return []  # Παράβλεψη αρχείων με συντακτικά λάθη
    
    imports = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                imports.add(alias.name.split('.')[0])
        elif isinstance(node, ast.ImportFrom):
            if node.module:
                imports.add(node.module.split('.')[0])
    
    return imports

def find_all_python_files():
    """Βρίσκει όλα τα .py αρχεία στο project"""
    python_files = []
    for root, dirs, files in os.walk('.'):
        # Παράβλεψη φακέλων που δεν μας ενδιαφέρουν
        if any(skip in root for skip in ['venv', 'env', '.venv', '__pycache__', '.git', 'dist', 'build']):
            continue
        for file in files:
            if file.endswith('.py'):
                python_files.append(os.path.join(root, file))
    return python_files

def check_installed_packages():
    """Ελέγχει ποια πακέτα είναι εγκατεστημένα στο current environment"""
    installed = {pkg.key for pkg in pkg_resources.working_set}
    return installed

def main():
    print("=" * 60)
    print("🔍 ΑΝΑΖΗΤΗΣΗ IMPORTS ΣΤΟ PROJECT")
    print("=" * 60)
    
    # Βρες όλα τα Python αρχεία
    python_files = find_all_python_files()
    print(f"\n📁 Βρέθηκαν {len(python_files)} Python αρχεία προς ανάλυση\n")
    
    # Συλλογή όλων των imports
    all_imports = set()
    file_imports = {}
    
    for py_file in python_files:
        imports = find_imports_in_file(py_file)
        if imports:
            file_imports[py_file] = imports
            all_imports.update(imports)
    
    # Εμφάνιση αποτελεσμάτων ανά αρχείο
    print("-" * 60)
    print("📄 IMPORTS ΑΝΑ ΑΡΧΕΙΟ:")
    print("-" * 60)
    
    for py_file, imports in sorted(file_imports.items()):
        print(f"\n📌 {py_file}")
        for imp in sorted(imports):
            print(f"   └─ {imp}")
    
    # Συνολική λίστα imports
    print("\n" + "=" * 60)
    print(f"📦 ΣΥΝΟΛΙΚΑ UNIQUE IMPORTS: {len(all_imports)}")
    print("=" * 60)
    
    # Ταξινόμηση και εμφάνιση
    standard_libs = {'os', 'sys', 're', 'json', 'datetime', 'math', 'random', 
                    'time', 'collections', 'functools', 'itertools', 'pathlib',
                    'sqlite3', 'csv', 'hashlib', 'argparse', 'logging'}
    
    third_party = []
    for imp in sorted(all_imports):
        if imp not in standard_libs and imp != '__future__':
            third_party.append(imp)
            print(f"   • {imp}")
    
    print("\n" + "=" * 60)
    print("📝 ΠΡΟΤΕΙΝΟΜΕΝΟ requirements.txt:")
    print("=" * 60)
    
    # Έλεγχος αν υπάρχει ήδη requirements.txt
    if os.path.exists('requirements.txt'):
        with open('requirements.txt', 'r') as f:
            existing = [line.strip().split('==')[0].split('>')[0].split('<')[0] 
                       for line in f if line.strip() and not line.startswith('#')]
        print("\n⚠️  Υπάρχον requirements.txt περιέχει:")
        for pkg in sorted(existing):
            print(f"   • {pkg}")
        print("\n➕ Νέες βιβλιοθήκες που βρέθηκαν αλλά δεν είναι στο requirements.txt:")
        new_pkgs = [p for p in third_party if p not in existing]
        for pkg in sorted(new_pkgs):
            print(f"   • {pkg}")
    else:
        print("\n".join(sorted(third_party)))
    
    print("\n" + "=" * 60)
    
    # Προαιρετικός έλεγχος εκδόσεων
    response = input("\n🤔 Θέλεις να ελέγξω ποιες εκδόσεις έχεις εγκατεστημένες; (y/n): ")
    if response.lower() == 'y':
        try:
            installed = check_installed_packages()
            print("\n📦 ΕΓΚΑΤΕΣΤΗΜΕΝΕΣ ΕΚΔΟΣΕΙΣ:")
            for pkg in sorted(third_party):
                if pkg in installed:
                    # Προσπάθεια να βρεις την ακριβή έκδοση
                    try:
                        version = subprocess.check_output([sys.executable, '-m', 'pip', 'show', pkg]).decode()
                        for line in version.split('\n'):
                            if line.startswith('Version:'):
                                print(f"   • {pkg}=={line.split(':')[1].strip()}")
                                break
                    except:
                        print(f"   • {pkg}")
                else:
                    print(f"   • {pkg} (⚠️  ΔΕΝ ΕΙΝΑΙ ΕΓΚΑΤΕΣΤΗΜΕΝΟ)")
        except:
            print("   Δεν ήταν δυνατός ο έλεγχος εκδόσεων")

if __name__ == "__main__":
    main()