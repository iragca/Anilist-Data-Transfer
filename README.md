<h1 align="center">Anilist Data Transfer</h1>
<h3 align="center">Part of <a href="https://github.com/iragca/keikakku-dashboards">Keikakku Dashboards</a></h3>

This repository is for transfering data from the node based [AniList GraphQL database](https://docs.anilist.co/) to
a local DuckDB relational database. The anime entries retrieved are roughly ~13,000 rows as of 2025 January 10.

> AniList database -> GraphQL API -> DuckDB

8 tables currently exist in the database:

- **Anime:** Stores detailed information about the anime shows.
- **Review:** Stores reviews of anime.
- **Status:** Stores statistics about anime user statuses.
- **User:** Stores user information.
- **WebAsset:** Stores web assets related to anime.
- **Studio:** Stores information about studios associated with anime.
- **Tag:** Stores tags associated with anime.
- **Genre:** Stores genres associated with anime.

<br>
 
<div style="border: 1px solid #007BFF; background-color: #E9F7FE; padding: 10px; border-radius: 5px; color: #0056b3;">
<strong>ℹ️ Info:</strong> Primary keys are for enforcing uniqueness. Foreign keys are not recommended as GraphQL is inherently node based and not relational.
</div>


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

## <a id="EDA"></a>Exploratory Data Analysis

Basic reports are made for each table and are available on [src/eda.](https://github.com/iragca/anilist-data-transfer/tree/main/src)


