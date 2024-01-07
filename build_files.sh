pip install virtualenv
virtualenv env
source env/bin/activate

pip install -r requirements.txt
python manage.py collectstatic --settings=skillupkids.settings.prod