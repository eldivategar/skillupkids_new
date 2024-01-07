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


chown -R nobody:nogroup /var/task
chown -R nobody:nogroup media

ls -l
pwd