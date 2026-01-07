serve:
  python3.11 -m http.server 9000

bundle:
  tar zcf dist/connect-extension-bulk-delete.tar.gz ./manifest.json ./requirements.txt ./app.py ./connect-extension.toml 