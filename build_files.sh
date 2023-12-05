python3.9 -m venv env
source env/bin/activate
pip install -r requirements.txt
python3.9 manage.py collectstatic --settings=skillupkids.settings.prod