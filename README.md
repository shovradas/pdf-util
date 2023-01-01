# PDFUtil

A desktop app for converting image(s) to PDF(s) and merging PDF files

![PDFUtil in Action][pdf_merger]

[pdf_merger]: https://raw.githubusercontent.com/shovradas/pdf-merger/main/docs/pdfutil.png "PDFUtil in Action"

# How to run
```
pip install pdfutil-0.1.0-py3-none-any.whl
pdfutil.exe
```

## Development
```
python -m pip install poetry
poetry install
poetry run pdfutil
poetry build
```
## Useful commands
```
poetry export -f requirements.txt --without-hashes --output requirements.txt
poetry export -f requirements.txt --without-hashes --with dev --output requirements-dev.txt
```
