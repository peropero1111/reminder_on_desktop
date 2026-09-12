# reminder_on_desktop

### 이 reminder_on_desktop 은 codex 의 도움이 들어갔습니다.  
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
&nbsp;&nbsp;&nbsp;&nbsp;1.1 적당한 폴더에 reminder_on_desktop 속 내용물을 다운 받아 주십시오.
</br>
</br>

&nbsp;&nbsp;&nbsp;&nbsp;1.2 reminder_on_desktop 속 reminder.py 에서 다음 명령어를 각각 입력하여 주십시오.

&nbsp;&nbsp;&nbsp;&nbsp;이때 굳이 google calendar 의 일정과 연동하고 싶지 않으신 분들은 
```powershell
python -m pip install winotify
```
&nbsp;&nbsp;&nbsp;&nbsp;만 입력하여서 설치하셔도 괜찮습니다.
</br>
</br>
&nbsp;&nbsp;&nbsp;&nbsp;단  google calendar 의 일정과 연동하고 싶으신 분들은 
```powershell
python -m install requests icalendar recurring-ical-events
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

&nbsp;&nbsp;&nbsp;&nbsp;5.1 [calendar_widget_on_desktop](https://github.com/peropero1111/calendar_widget_on_desktop) 와 마찬가지로 한주안의 일정은 붉은 색으로 표시해 줍니다.


&nbsp;&nbsp;&nbsp;&nbsp;<img src="https://github.com/peropero1111/reminder_with_google_calendar/blob/main/img/2026-09-09%20203311.png?raw=true" width="450" height="450"/> 
</br>
</br>


&nbsp;&nbsp;&nbsp;&nbsp;5.2 [calendar_widget_on_deskop](https://github.com/peropero1111/calendar_widget_on_desktop) 와 마찬가지로 민감한  할 일을 숨길 수 있습니다.


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


---

## 라이선스 및 제3자 소프트웨어

`reminder_on_desktop`에서 프로젝트 작성자가 직접 작성하고 저작권을
보유한 원본 소스 코드는 MIT License에 따라 배포됩니다.

자세한 내용은 저장소 루트의 [`LICENSE`](LICENSE) 파일을 참고해
주십시오.

이 프로젝트는 다음과 같은 제3자 Python 패키지를 사용하거나 사용할 수
있습니다.

| 패키지                     | 라이선스                   |
| ----------------------- | ---------------------- |
| `requests`              | Apache License 2.0     |
| `icalendar`             | BSD 2-Clause License   |
| `recurring-ical-events` | GNU LGPL v3.0 or later |
| `winotify`              | MIT License            |
| `x-wr-timezone`         | GNU LGPL v3.0 or later |
| `tzdata`                | Apache License 2.0     |

각 제3자 패키지에는 `reminder_on_desktop`의 MIT License와 별개의
라이선스가 적용됩니다.

제3자 소프트웨어와 관련된 자세한 내용은 다음 파일을 참고해 주십시오.

* [`THIRD_PARTY_NOTICES.md`](THIRD_PARTY_NOTICES.md)
* [`LICENSES/README.md`](LICENSES/README.md)
* [`LICENSES/`](LICENSES/)

위 제3자 라이선스는 해당 구성요소에 적용되며,
`reminder_on_desktop`의 원본 소스 코드에 적용되는 MIT License를
대체하지 않습니다.

### EXE 배포판에 대한 안내

컴파일되거나 패키징된 EXE 버전에는 Python 런타임 및 추가적인 제3자
라이브러리와 의존 패키지가 포함될 수 있습니다.

실제로 포함되는 구성요소는 Python 버전, 패키지 버전 및 빌드 환경에
따라 달라질 수 있습니다.

각 구성요소에는 자체적인 라이선스와 재배포 조건이 적용되므로 새로운
EXE 버전을 배포할 때에는 실제 빌드에 포함된 패키지와 라이선스를
별도로 확인하는 것을 권장합니다.

---

## 비공식 프로젝트 및 상표 안내

`reminder_on_desktop`는 비공식 서드파티 오픈소스 프로젝트입니다.

이 프로젝트는 Google LLC와 제휴 관계에 있지 않으며 Google LLC로부터
공식적인 승인, 후원 또는 보증을 받은 프로젝트가 아닙니다.

Google, Google Calendar 및 관련 명칭과 상표는 Google LLC의 상표 또는
자산입니다.

이 프로젝트에서 Google Calendar라는 명칭을 사용하는 것은 호환성,
지원되는 데이터 형식 및 연동 방법을 설명하기 위한 식별 목적으로만
사용됩니다.

---

## Google Calendar 비공개 iCal 주소에 대한 주의

Google Calendar와 연동하는 경우 이 프로그램은
`iCal 형식의 비공개 주소`를 사용할 수 있습니다.

이 주소를 알고 있는 사람이나 프로그램은 해당 캘린더의 일정 정보에
접근할 수 있을 수 있으므로 비밀번호와 비슷한 민감한 정보로 취급하는
것을 권장합니다.

따라서 다음 사항에 주의해 주십시오.

* 비공개 iCal 주소를 GitHub 또는 다른 공개 저장소에 올리지 마십시오.
* 비공개 iCal 주소가 보이는 스크린샷을 공개하지 마십시오.
* `reminder_widget_config.json`에 비공개 iCal 주소가 저장되어 있다면
  해당 파일을 공개 저장소에 커밋하지 마십시오.
* `reminder_widget_config.json`을 `.gitignore`에 추가하는 것을
  권장합니다.
* 비공개 iCal 주소가 외부에 노출되었다고 판단되는 경우 기존 주소를
  더 이상 사용하지 말고 Google Calendar에서 주소를 재설정한 뒤 새
  주소를 사용하십시오.

사용자는 프로그램에 입력하는 캘린더 주소와 캘린더 데이터에 필요한
접근 권한을 보유하고 있는지 확인할 책임이 있습니다.

---

## 면책조항

이 소프트웨어는 어떠한 종류의 명시적 또는 묵시적 보증 없이
**"있는 그대로(AS IS)"** 제공됩니다.

프로젝트 작성자는 다음 사항을 보장하지 않습니다.

* 모든 환경에서 프로그램이 항상 정상적으로 작동하는 것
* 모든 일정이 항상 정확하게 불러와지는 것
* 모든 반복 일정이 항상 정확하게 처리되는 것
* 모든 알림이 지정된 시간에 반드시 표시되는 것
* Google Calendar의 일정과 프로그램에 표시되는 일정이 항상 완전히
  일치하는 것

중요한 일정이나 알림의 경우 이 프로그램에만 의존하지 말고 필요에
따라 원본 캘린더에서도 직접 확인하는 것을 권장합니다.

이 프로젝트의 사용으로 발생하는 결과에 대한 책임은 저장소의
`LICENSE`에 규정된 범위 내에서 제한됩니다.

