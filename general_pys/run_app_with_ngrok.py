import os
from pyngrok import ngrok
import subprocess
import time

# Η θύρα που τρέχει Streamlit
port = 8501

# Δημιουργεί ngrok tunnel
public_url = ngrok.connect(port)
print(f"🔗 Το app σου είναι live στο: {public_url}")

# Τρέχει το Streamlit app σου
# Αν το αρχείο σου λέγεται app.py
subprocess.run(["streamlit", "run", "mod_17_streamlit3.py"])
