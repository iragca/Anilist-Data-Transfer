<h1 align="center">Anilist Data Transfer</h1>
<h3 align="center">Part of <a href="https://github.com/iragca/keikakku-dashboards">Keikakku Dashboards</a></h3>

<h3>Quicklinks</h3>

- [Getting Started](#Getting-Started)
- [Exploratory Data Analysis](#EDA)

  <h2></h2>

This repository is for transferring data from the node based [AniList GraphQL database](https://docs.anilist.co/) to
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

> [!NOTE]
> Primary keys are for enforcing uniqueness. Foreign keys are not recommended as GraphQL is inherently node based and not relational.

#### Relevant / Similar Repositories

- https://github.com/manami-project/anime-offline-database

## <a id="Getting-Started"></a>Getting Started


https://github.com/user-attachments/assets/7a25466b-d1a9-4c4f-8259-7d8bf6b89396


Requirements:

- Python


<div style="font-weight: bold; margin-bottom: 5px;">Linux</div>

```bash
git clone https://github.com/iragca/anilist-data-transfer.git
cd anilist-data-transfer
bash setup.sh
source .venv/bin/activate
pip install -r requirements.txt
python src/init_db.py
python src/data_transfer.py 1940 2025 10 # <inclusive: start year> <exclusive: end year> <optional: cooldown; default: 10>
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
python .\src\data_transfer.py 1940 2025 10 # <inclusive: start year> <exclusive: end year> <optional: cooldown; default: 10>
```

## <a id="EDA"></a>Exploratory Data Analysis

Basic reports are made for each table and are available on project folder [root/eda](https://github.com/iragca/Anilist-Data-Transfer/tree/main/eda)


