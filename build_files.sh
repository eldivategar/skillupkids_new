pip install virtualenv
virtualenv env
source env/Script/activate

pip install -r requirements.txt
python manage.py collectstatic --settings=skillupkids.settings.prod