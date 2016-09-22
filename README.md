# Cookit
Nuance NLU online project
***
Cookit is a web platform for Nuance NLU data management, online word segmentation and model validation. 


## Environment
python2.7 **x86**+django+mysql

## Db Init
Create schema ‘cookit’ in mysql, then
```
python manage.py makemigrations
python manage.py migrate
```
Your data models under `NLU/models.py` will be sync into db. 
	
## Add a User Account
Cookit requires user login to access NLU online part，so we need to create an account in backend.
```
python manage.py adduser
```

## Data Management

### Data Type
Cookit supports three kinds of NLU data:
1. corpus
2. hrl
3. pattern

**1. Corpus data template**
```
// no header
Ent.Pause	停止 播放
Ent.Continue	恢复 听 歌
```

**2. Hrl data template**
```
// with header
#head;hrl;2.0;utf-8
#ref#speechfile#speaker#gender#reference word sequence#topic#;slot names#;slot values
head
ref#Blu/009s003.pcm#Blu#male#请打开收音机界面#INTENT_Radio_ShowRadio##
ref#Blu/009s034.pcm#Blu#male#有收音机界面吗#INTENT_Radio_ShowRadio##
```
**3. Pattern data template**
```
Apps.CloseApp	APP_NM 不想 听 了
Apps.ShowMenu	APP_MENU_NM 打开
```

### Add New Data
Put your all data files under  `\Cookit\static\data`

The data file should be categorized by its suffix:
1. Corpus: **\*.cop**
2. Hrl: **\*.hrl**
3. Pattern: **\*.pat**

Then run `python manage.py syncdata`, all the data will be sync to the db automatically.


## Cookit Website

Cookit web part provides ...


waiting...