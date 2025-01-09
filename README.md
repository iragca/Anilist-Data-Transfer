<h1 align="center">Anilist Data Transfer</h1>
<h3 align="center">Part of <a href="https://github.com/iragca/keikakku-dashboards">Keikakku Dashboards</a></h3>

### <a id="Requirements"></a>Requirements

- Python

## <a id="Getting-Started"></a>Getting Started

<div style="font-weight: bold; margin-bottom: 5px;">Linux</div>

```bash
git clone https://github.com/iragca/anilist-data-transfer.git
cd anilist-data-transfer
bash setup.sh
source .venv/bin/activate
pip install -r requirements.txt
python src/init_db.py
python src/data_transfer.py
```

<div style="font-weight: bold; margin-bottom: 5px;">Powershell</div>

```powershell
git clone https://github.com/iragca/anilist-data-transfer.git
cd anilist-data-transfer
pip install virtualenv
virtualenv .venv
source .\.venv\Scripts\activate
pip install -r requirements.txt
python .\src\init_db.py
python .\src\data_transfer.py
```
