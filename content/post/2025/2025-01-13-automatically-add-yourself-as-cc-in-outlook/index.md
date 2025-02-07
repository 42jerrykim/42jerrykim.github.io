---
title: "[Outlook] 아웃룩에서 메일 보낼 때 자동으로 본인을 참조(CC) 추가하는 방법"
categories:
- Outlook
- OutlookAutomation
- MicrosoftOffice
tags:
- Outlook
- 아웃룩
- MicrosoftOutlook
- Office365
- EmailAutomation
- 자동CC
- 규칙설정
- VBA매크로
- 업무팁
- 생산성향상
- IT꿀팁
- 자동화
- 메일관리
- 이메일관리
- 이메일참조
- 아웃룩설정
- OfficeTips
- 아웃룩규칙
- 회사업무
- 직장인꿀팁
- 업무효율
- 효율적업무
- 보안정책
- 참조자동
- 자동메일
- 메일발송
- MicrosoftOffice
- 메일효율
- 설정가이드
- OutlookTips
- IT기초
- 회사메일
- 자동회신
- 생산성도구
- 메일팁
- 디지털워크
- 이메일효율
- 협업도구
- 직장생활
- 사내교육
- 아웃룩가이드
- Office자동화
- 초보가이드
- 업무매뉴얼
- OutlookVBA
- 규칙마법사
- 메일작성
- Windows
- EmailManagement
- EmailWorkflow
- EmailTools
- EmailSettings
- EmailConfiguration
- EmailAutomation
- EmailProductivity
- EmailEfficiency
- EmailBestPractices
- EmailOrganization
- EmailSolutions
- EmailTechnology
- EmailCommunication
- EmailSoftware
- EmailFeatures
- EmailCustomization
- EmailProcesses
- EmailWorkspace
- EmailInbox
- EmailSystem
- EmailSetup
- EmailTutorial
- EmailGuide
- EmailHowTo
- EmailTips
- EmailHacks
- EmailSecurity
- EmailPrivacy
- EmailProtocols
- EmailIntegration
- EmailServices
- EmailClient
- EmailPlatform
- EmailInterface
- EmailFunctionality
- EmailCapabilities
- EmailOptions
- EmailPreferences
- EmailControls
- EmailRules
- EmailFilters
- EmailNotifications
- EmailForwarding
- EmailCopy
- EmailDistribution
- EmailDelivery
- EmailTracking
- EmailMonitoring
- EmailSupport
- EmailTroubleshooting
- EmailMaintenance
- EmailOptimization
image: "index.png"
date: 2025-01-13
updated: 2025-02-06
---

Outlook에서 email을 보낼 때 자동으로 본인을 CC에 추가하는 것은 매우 편리한 기능이다. 보낸 메일을 "보낸 편지함"에서 일일이 찾아보지 않아도 "받은 편지함"에서 바로 확인할 수 있기 때문이다. 또한 업무 특성상 본인이 CC에 포함되어야 하는 경우가 많다면, 매번 수동으로 CC를 추가하는 번거로움을 자동화 설정으로 해결할 수 있다. 이러한 자동 CC 설정을 위한 두 가지 방법을 소개하고자 한다.


## 1. 아웃룩 규칙을 이용한 자동 CC 설정 방법.

1. **아웃룩 실행** 후, 상단 메뉴의 **파일**을 클릭한 뒤 **정보** → **규칙 및 알림 관리** 메뉴로 이동한다.  
2. **규칙 및 알림** 창에서 **새 규칙**을 클릭하고, **규칙 마법사**를 연다.  
3. "보낸 메시지에 적용" 또는 비슷한 템플릿을 선택한 뒤 **다음**을 클릭한다.  
4. 조건 설정 화면에서 모든 조건을 체크 해제하고, 경고 창이 뜨면 **예**를 선택합니다.  
   - 이렇게 하면 내가 보낸 모든 메일에 규칙이 적용됩니다.  
5. **조치 지정** 화면에서 "**메시지를 지정된 사람/배분 목록에게 보낸 사람에게 CC로 보낸다**" 옵션을 선택한다.  
6. 규칙 설명 하단에서 "**지정된 사람/배분 목록**"을 클릭하여 **본인의 이메일 주소**를 입력한다.  
7. 다음 단계를 클릭해 예외 설정이 필요하면 추가하고, 필요 없다면 넘어간다.  
8. 마지막으로 규칙의 이름을 정하고(예: "내 메일 자동 CC"), 규칙 사용에 체크한 뒤 **마침**을 누른다.  

이 과정을 마치면, **아웃룩에서 메일을 보낼 때마다 본인이 자동으로 참조(CC)에 포함**됩니다.

## 2. VBA 매크로를 이용한 자동 CC 설정 방법.

규칙 방식 이외에, VBA 스크립트를 활용해 메일을 보낼 때마다 본인을 자동 참조(CC)로 추가할 수도 있다. 다만, 회사나 기관의 보안 정책에 따라 매크로 사용이 제한될 수 있으므로 사전에 확인해야 한다.

1. **아웃룩**에서 **Alt + F11** 키를 눌러 VBA 편집기를 연다.  
2. 왼쪽 프로젝트 창에서 `ThisOutlookSession`을 더블 클릭한다.  
3. 아래와 같은 코드를 붙여넣는다. (이메일 주소를 본인 것으로 바꿔야 한다.)
   ```vb
   Private Sub Application_ItemSend(ByVal Item As Object, Cancel As Boolean)
       Dim mail As Outlook.MailItem
       
       If TypeName(Item) = "MailItem" Then
           Set mail = Item
           mail.Recipients.Add "myemail@domain.com"
           mail.Recipients(mail.Recipients.Count).Type = olCC
           Set mail = Nothing
       End If
   End Sub
   ```
4. 작성이 끝나면 저장 후 VBA 편집기를 닫고, **아웃룩**을 재시작한다.  
5. 이제 메일을 보낼 때마다, 자동으로 설정된 스크립트가 본인 이메일 주소를 참조(CC)에 추가한다.

## 3. 유의 사항.

- **회사/기관**에서 사용하는 아웃룩은 보안 정책으로 인해 규칙 생성이나 VBA 매크로 사용이 제한될 수 있다. 반드시 관리자나 IT 부서에 문의하는 것이 좋다.  
- 자동 CC 설정을 하면 수신되는 메일이 중복될 수 있으므로, 메일 박스 용량에 유의해야 한다. 또한, 일정 기간 뒤에는 **정기적으로 보관 처리**나 **정리 작업**을 수행하는 것이 좋다.  
- 업무에 따라 **예외 처리**가 필요한 경우가 있다면, 규칙 마법사에서 예외 조건을 등록하는 편이 편리하다.  

이상으로 아웃룩에서 메일을 보낼 때 자동으로 본인을 참조(CC)에 추가하는 두 가지 방법을 알아보았습니다. 업무 효율성을 높이고 중요한 메일을 놓치지 않으려면, 간단한 규칙 설정이나 VBA 매크로를 사용해 보는 것을 추천합니다. 편리함과 생산성 향상에 도움이 되길 바랍니다. 모두 즐거운 업무 생활을 누리시길 바랍니다. 끝이다.