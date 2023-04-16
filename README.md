use python==3.8.8

開好虛擬環境在根目錄下打下面指令

mac、Linux :
```bash
pip install -r ./requirements.txt
```

Windows :
```batch
pip install -r .\requirements.txt
```

第一次啟動前需使用
```bash
python manage.py makemigrations
```
```bash
python manage.py migrate
```

啟動專案 :

```bash
python manage.py runserver
```