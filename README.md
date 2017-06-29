# CHOCCO
CHOCCO


# Разворачиваем проект

git clone https://github.com/AlimovTILLO/CHOCCO.git

virtualenv -p python3 venv

source venv/bin/activate

устанавливаем зависимости pip install -r requirements.txt

cd core/

python manage.py makemigrations

python manage.py migrate

python manage.py createsuperuser

python manage.py runserver