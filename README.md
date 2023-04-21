# OAuth2.0試做 #

## [Required](https://github.com/jimlin1111/oauth2.0_test#Required) ##
> python==3.8.8
---------------
## [Before active](https://github.com/jimlin1111/oauth2.0_test#before-active) ##
若使用mysql可將[oauth20/sensitive-sample.py](https://github.com/jimlin1111/oauth2.0_test/blob/master/oauth20/sensitive-sample.py)
複製成**oauth20/sensitive.py**並填入必要資訊  

若不是則需至**oauth20/settings.py**中將最下面的`from oauth20.sensitive.py import *`註解  
並將約中段的`DATABASES`參數取消註解

<font color=#FF0000>*註解後啟動專案時會在根目錄多一個 **db.sqlite3** 檔案</font>

----------
## sensitive-sample.py參數說明 ##
**DATABASE**為資料庫資訊(範例為使用mysql，可自行調整自己慣用的)  
**CHANNEL_ABOUT** 為line login與line notify的channel_id與secret
**BASE_URL** 為此網站的domain，像是https://example.com.tw (最後不用加入/)
----------
## [How to active](https://github.com/jimlin1111/oauth2.0_test#how-to-active) ##
開好python虛擬環境後在根目錄下打下面指令  

mac、Linux :
```bash
pip3 install -r ./requirements.txt
```

Windows :
```bash
pip3 install -r .\requirements.txt
```

第一次啟動前需使用
```bash
python3 manage.py makemigrations
```
```bash
python3 manage.py migrate
```

啟動專案 :

```bash
python3 manage.py runserver
```