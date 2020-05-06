# This script:
#   - sets up the catalog_search_path directory for databroker to find catalogs
#   - copies a simple catalog.yml file to configure our catalog sources
#   - copies msgpack catalogs next to the catalog.yml

import shutil
from pathlib import Path
from databroker import catalog_search_path

catalog_path = catalog_search_path()[0]
print(f"Using the following catalog search path: {catalog_path}...")

print(f"Creating the directory {catalog_path} (if it does not already exist)...")
Path(catalog_path).mkdir(parents=True, exist_ok=True)

print(f"Copying catalog.yml to {catalog_path}...")
shutil.copy("catalog.yml", catalog_path)

print(f"Copying msgpack files to {catalog_path}...")
# catalog.yml uses the {{ CATALOG_DIR }}/*.msgpack
# this means catalogs will be search for in the directory that catalog.yml was copied to.
msgpack_file_gen = Path.cwd().glob("*.msgpack")
for f in msgpack_file_gen:
    print(f"\tcopying {f.name}...")
    shutil.copy(f, catalog_path)

print("Done.")
