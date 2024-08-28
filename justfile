serve:
  python3.11 -m http.server 9000

bundle:
  tar zcf connect-extension-bulk-delete.tar.gz ./manifest.json ./requirements.txt ./app.py ./extension.toml ./labs.toml