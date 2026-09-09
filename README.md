# reminder_with_google_calendar

### 이 reminder_with_google_calendar 은 codex 의 도움이 들어갔습니다.  
</br>



[exe 파일링크](https://drive.google.com/drive/folders/1gWtG7FFEK5YoUlfUZFnBOCYaJI3ADCnP?usp=sharing) 로 실행할때의 사용법은 글 하단에 있습니다.
</br>
</br>
사용하시기전에 다음 절차를 따라 주십시오.
</br>

### 목차
[1. 설치](#1-설치)  
[2. Google Calendar 연결 (선택)](#2-google-calendar-연결-선택)  
[3. 작업스케쥴러 등록 (선택사항) (py 버젼)](#3-작업스케쥴러-등록-선택사항-py-버젼)  
[4. 작업스케쥴러 등록 (선택사항) (exe 버젼)](#4-작업스케쥴러-등록-선택사항-exe-버젼)  
[5. 기능 소개](#5-기능-소개)

## 1. 설치
&nbsp;&nbsp;&nbsp;&nbsp;1.1 적당한 폴더에 reminder_with_google_calendar 속 내용물을 다운 받아 주십시오.
</br>
</br>

&nbsp;&nbsp;&nbsp;&nbsp;1.2 reminder_with_google_calendar 속 reminder.py 에서 다음 명령어를 각각 입력하여 주십시오.

&nbsp;&nbsp;&nbsp;&nbsp;이때 굳이 google calendar 의 일정과 연동하고 싶지 않으신 분들은 
```powershell
python -m pip install winotify
```
&nbsp;&nbsp;&nbsp;&nbsp;만 입력하여서 설치하셔도 괜찮습니다.
</br>
</br>
&nbsp;&nbsp;&nbsp;&nbsp;단  google calendar 의 일정과 연동하고 싶으신 분들은 
```powershell
pip -m install requests icalendar recurring-ical-events
```
&nbsp;&nbsp;&nbsp;&nbsp;까지 입력해 주셔야 합니다.
</br>

## 2. Google Calendar 연결 (선택)

&nbsp;&nbsp;&nbsp;&nbsp;2.1. 브라우저에서 Google Calendar를 엽니다.  
&nbsp;&nbsp;&nbsp;&nbsp;2.2. 오른쪽 위 톱니바퀴 아이콘에서 `설정`으로 들어갑니다.  
&nbsp;&nbsp;&nbsp;&nbsp;2.3. 왼쪽에서 `내 캘린더의 설정`을 선택한 후 선택할 계정을 고릅니다.  
&nbsp;&nbsp;&nbsp;&nbsp;2.4. `캘린더 통합` 을 선택한 후 암호화 형식인 `iCal 형식의 비공개 주소`를 복사합니다.  
&nbsp;&nbsp;&nbsp;&nbsp;2.5. calendar.py를 처음 실행하면 생기는 `reminder_widget_config.json` 파일을 열고 `input_ical_urls`에 붙여 넣습니다.

</br>

## 3. 작업스케쥴러 등록 (선택사항) (py 버젼) 
&nbsp;&nbsp;&nbsp;&nbsp;3.1 작업스케줄러를 실행시킨후 작업만들기를 클릭하여 주십시오.

&nbsp;&nbsp;&nbsp;&nbsp;<img src="https://github.com/peropero1111/reminder_with_google_calendar/blob/main/img/2026-09-09%20185153.png" width="450" height="450"/>  
</br>

&nbsp;&nbsp;&nbsp;&nbsp;3.2 처음뜨는 창 (일반 메뉴) 에서 이름을 정해 주시고 `사용자가 로그온 할때만 실행` 으로 설정해 주십시오.

&nbsp;&nbsp;&nbsp;&nbsp;<img src="https://github.com/peropero1111/reminder_with_google_calendar/blob/main/img/2026-09-09%20185316.png?raw=true" width="450" height="450"/> 
</br>
</br>

&nbsp;&nbsp;&nbsp;&nbsp;3.3 트리거 메뉴로 넘어가서 새로만들기를 눌러주십시오.

&nbsp;&nbsp;&nbsp;&nbsp;<img src="https://github.com/peropero1111/reminder_with_google_calendar/blob/main/img/2026-09-09%20185402.png?raw=true" width="450" height="450"/> 
</br>
</br>

&nbsp;&nbsp;&nbsp;&nbsp;3.4 작업시작을 `로그온 할떄`, 지연시간에 체크해 주시고 30초 로 체크해 주십시오.

&nbsp;&nbsp;&nbsp;&nbsp;<img src="https://github.com/peropero1111/reminder_with_google_calendar/blob/main/img/2026-09-09%20185452.png?raw=true" width="450" height="450"/> 
</br>
</br>

&nbsp;&nbsp;&nbsp;&nbsp;3.5 cmd 혹은 powershell 을 관리자 권한으로 실행시켜서 ```  where pythonw  ``` 라고 검색 해 주십시오.
</br>&nbsp;&nbsp;&nbsp;&nbsp;( 저는 python 을 기존에 다운 하여서 두번째 경로가 있는데 대부분의 사람들은 첫번째 경로 밖에 없을 것입니다. 무엇으로 하여도 결과에 큰 지장은 없습니다. )

&nbsp;&nbsp;&nbsp;&nbsp;<img src="https://github.com/peropero1111/google_calendar_on_desktop/blob/main/img/2026-06-30%20215110.png" width="450" height="450"/> 
<br>
</br>

&nbsp;&nbsp;&nbsp;&nbsp;3.6 나온 경로를 기억하고 있다가 동작 메뉴로 넘어가서 새로만들기를 눌러 주십시오.

&nbsp;&nbsp;&nbsp;&nbsp;<img src="https://github.com/peropero1111/reminder_with_google_calendar/blob/main/img/2026-09-09%20185631.png?raw=true" width="450" height="450"/> 
<br>
</br>

&nbsp;&nbsp;&nbsp;&nbsp;3.7 `프로그램`에 나온 경로를 입력하여 주십시오. 
</br>&nbsp;&nbsp;&nbsp;&nbsp;3.8 `인수 추가` 에 다음과 같이 입력하여 주십시오 `"C:\Users\~ run_widget.py 를 놓은 폴더 경로 주소 ~ \run_widget.py"`
</br>&nbsp;&nbsp;&nbsp;&nbsp;3.9 `시작 위치` 에 다음과 같이 입력하여 주십시오  `C:\Users\~ run_widget.py 를 놓은 폴더 경로 주소 ~`

&nbsp;&nbsp;&nbsp;&nbsp;<img src="https://github.com/peropero1111/reminder_with_google_calendar/blob/main/img/2026-09-09%20185951.png?raw=true" width="450" height="450"/> 
<br>
</br>

## 4. 작업스케쥴러 등록 (선택사항) (exe 버젼) 

&nbsp;&nbsp;&nbsp;&nbsp;4.1 작업스케줄러를 실행시킨후 작업만들기를 클릭하여 주십시오.

&nbsp;&nbsp;&nbsp;&nbsp;<img src="https://github.com/peropero1111/google_calendar_on_desktop/blob/main/img/2026-06-30%20212029.png" width="450" height="450"/>  
</br>

&nbsp;&nbsp;&nbsp;&nbsp;4.2 처음뜨는 창 (일반 메뉴) 에서 이름을 정해 주시고 `사용자가 로그온 할때만 실행` 으로 설정해 주십시오.

&nbsp;&nbsp;&nbsp;&nbsp;<img src="https://github.com/peropero1111/reminder_with_google_calendar/blob/main/img/2026-09-09%20185316.png?raw=true" width="450" height="450"/> 
</br>
</br>

&nbsp;&nbsp;&nbsp;&nbsp;4.3 트리거 메뉴로 넘어가서 새로만들기를 눌러주십시오.

&nbsp;&nbsp;&nbsp;&nbsp;<img src="https://github.com/peropero1111/google_calendar_on_desktop/blob/main/img/2026-06-30 212201.png" width="450" height="450"/> 
</br>
</br>

&nbsp;&nbsp;&nbsp;&nbsp;4.4 작업시작을 `로그온 할떄`, 지연시간에 체크해 주시고 30초 로 체크해 주십시오

&nbsp;&nbsp;&nbsp;&nbsp;<img src="https://github.com/peropero1111/google_calendar_on_desktop/blob/main/img/2026-06-30%20212231.png" width="450" height="450"/> 
</br>
</br>

&nbsp;&nbsp;&nbsp;&nbsp;4.6 동작 메뉴로 넘어가서 새로만들기를 눌러 주십시오.

&nbsp;&nbsp;&nbsp;&nbsp;<img src="https://github.com/peropero1111/google_calendar_on_desktop/blob/main/img/2026-06-30%20212311.png" width="450" height="450"/> 
<br>
</br>


&nbsp;&nbsp;&nbsp;&nbsp;4.7 `프로그램`에 exe 파일의 경로를 입력하여 주십시오. 
</br>&nbsp;&nbsp;&nbsp;&nbsp;4.8 `인수 추가` 에 다음과 같이 입력하여 주십시오 `"C:\Users\~ reminder.exe 를 놓은 폴더 경로 주소 ~ \reminder.exe"`
</br>&nbsp;&nbsp;&nbsp;&nbsp;4.9 `시작 위치` 에 다음과 같이 입력하여 주십시오  `C:\Users\~ reminder.exe 를 놓은 폴더 경로 주소 ~`

&nbsp;&nbsp;&nbsp;&nbsp;<img src="https://github.com/peropero1111/reminder_with_google_calendar/blob/main/img/2026-09-09%20201142.png?raw=true" width="450" height="450"/> 
<br>
</br>


## 5. 기능 소개 

&nbsp;&nbsp;&nbsp;&nbsp;5.1 google_calendar_on_desktop 와 마찬가지로 한주안의 일정은 붉은 색으로 표시해 줍니다.


&nbsp;&nbsp;&nbsp;&nbsp;<img src="https://github.com/peropero1111/reminder_with_google_calendar/blob/main/img/2026-09-09%20203311.png?raw=true" width="450" height="450"/> 
</br>
</br>


&nbsp;&nbsp;&nbsp;&nbsp;5.2 google_calendar_on_desktop 와 마찬가지로 민감한  할 일을 숨길 수 있습니다.


&nbsp;&nbsp;&nbsp;&nbsp;<img src="https://github.com/peropero1111/reminder_with_google_calendar/blob/main/img/2026-09-09%20203529.png?raw=true" width="450" height="450"/> 
</br>
</br>


&nbsp;&nbsp;&nbsp;&nbsp;5.3 리마인더이니 만큼 일정을 등록할 수 있습니다.


&nbsp;&nbsp;&nbsp;&nbsp;<img src="https://github.com/peropero1111/reminder_with_google_calendar/blob/main/img/2026-09-09%20203209.png?raw=true" width="450" height="450"/> 
</br>
</br>



&nbsp;&nbsp;&nbsp;&nbsp;5.4 리마인더이니 만큼 <code>직접등록 한</code> 일정은 지울수 있습니다. ( google calendar 에 등록되어 있는 일정은 지울 수 없습니다. )


&nbsp;&nbsp;&nbsp;&nbsp;<img src="https://github.com/peropero1111/reminder_with_google_calendar/blob/main/img/2026-09-09%20203529.png?raw=true" width="450" height="450"/> 
</br>
</br>

