echo "BUILD START"

python3.9 -m venv venv
    source venv/bin/activate

pip install -r requirements.txt

echo "BUILD END"

echo "Collecting static files..."
python manage.py collectstatic --settings=skillupkids.settings.prod

echo "Migrating..."
python manage.py makemigrations --settings=skillupkids.settings.prod
python manage.py migrate --settings=skillupkids.settings.prod

echo "Create Superuser..."
python manage.py customsuperuser --settings=skillupkids.settings.prod

echo "Permission..."
chmod -R 777 media
chmod -R 777 staticfiles_build

mkdir /var/task/media
chmod -R 777 /var/task/media
