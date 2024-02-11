
echo "BUILD START"

python3.9 -m venv venv
    source venv/bin/activate

pip install -r requirements.txt

echo "BUILD END"

echo "Collecting static files..."
python manage.py collectstatic --noinput --settings=skillupkids.settings.prod 

# echo "Create cache_table..."
# python manage.py createcachetable --settings=skillupkids.settings.prod

# echo "Migrating..."
# python manage.py makemigrations --settings=skillupkids.settings.prod
# python manage.py migrate --settings=skillupkids.settings.prod

# echo "Create Superuser..."
# python manage.py customsuperuser --settings=skillupkids.settings.prod

# du -h -d 1 skillupkids_v1 | sort -h
# echo "Permission..."