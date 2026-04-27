# Usage

1. Create a `.env` file for secret variables following the format in `.env.example`
```env
DB_USER=
DB_PASS=
DB_DSN=
LIB_DIR=
```
2. Run `dataload.py` to populate the Oracle FreeSQL database
```shell
python3 dataload.py
```
3. Run `app.py` to enter the terminal UI
```shell
python3 app.py
```