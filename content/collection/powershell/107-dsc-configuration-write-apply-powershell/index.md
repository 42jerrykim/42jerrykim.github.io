---
draft: true
collection_order: 107
slug: dsc-configuration-write-apply-powershell
title: "[PowerShell] 107. DSC 구성(Configuration) 작성과 적용"
date: 2026-08-29
lastmod: 2026-08-29
description: "DSC Configuration 블록에서 Node/DependsOn으로 리소스 순서를 정의하는 법과 컴파일해 MOF 파일을 만드는 과정, Start-DscConfiguration으로 실제 노드에 적용하고 Test-DscConfiguration으로 상태를 검증하는 흐름을 정리한 챕터다."
categories:
- PowerShell
tags:
- PowerShell
- Cmdlet
- Object-Pipeline
- Windows(윈도우)
- Shell(셸)
- .NET
- DSC
- Guide(가이드)
- Education(교육)
- Beginner
- Documentation(문서화)
- Quick-Reference
- Best-Practices
- Comparison(비교)
- Reference(참고)
- How-To
- Tips
- Automation(자동화)
- DevOps
- Start-DscConfiguration
- DependsOn
- Node-Block
- Test-DscConfiguration
- Configuration-Job
- Push-Deployment
image: "wordcloud.png"
---

## 개요

106장에서 DSC의 전체 그림을 그렸다면, 이 장은 실제로 `Configuration` 블록을 작성하고 그것을 노드에 적용하는 전체 파이프라인을 다룬다. 이 흐름은 "작성 → 컴파일(MOF 생성) → 적용 → 검증"이라는 네 단계로 이뤄지며, 각 단계가 서로 다른 명령으로 분리돼 있다는 점이 92장에서 배운 예약 작업의 "정의(New-ScheduledTaskAction) → 등록(Register-ScheduledTask)" 흐름과 유사한 패턴이다.

정신 모델은 "Configuration은 설계도를 그리는 것, MOF 컴파일은 그 설계도를 표준 규격 문서로 인쇄하는 것, `Start-DscConfiguration`은 그 문서를 시공팀에 전달해 실제로 짓게 하는 것"이라는 것이다.

## 사용법

```powershell
Configuration <이름> { Node <노드목록> { <리소스블록들> } }
<이름> -OutputPath <MOF저장경로>
Start-DscConfiguration -Path <MOF저장경로> -Wait -Verbose
```

## 종류

| 단계 | 명령/구문 | 결과 |
|---|---|---|
| 작성 | `Configuration` 키워드 | PowerShell 함수처럼 동작하는 구성 정의 |
| 노드 지정 | `Node` 블록 | 하나의 Configuration으로 여러 대상 노드를 동시에 기술 가능 |
| 순서 지정 | `DependsOn` | 리소스 간 적용 순서를 명시(기본은 순서 보장 안 됨) |
| 컴파일 | `<이름> -OutputPath <경로>` | `<노드이름>.mof` 파일 생성 |
| 적용 | `Start-DscConfiguration` | MOF를 실제로 실행(`-Wait` 없으면 백그라운드 Job으로 즉시 반환) |
| 검증 | `Test-DscConfiguration` | 현재 상태가 구성과 일치하는지 확인(적용은 안 함) |
| 조회 | `Get-DscConfiguration` | 현재 노드에 마지막으로 적용된 구성 상태 조회 |

## 예시

```powershell
Configuration WebServerConfig {
    Node "localhost" {
        WindowsFeature IIS {
            Ensure = "Present"
            Name   = "Web-Server"
        }
        Service W3SVC {
            Name      = "W3SVC"
            State     = "Running"
            DependsOn = "[WindowsFeature]IIS"    # IIS 설치가 끝난 뒤에야 서비스 시작 시도
        }
    }
}

WebServerConfig -OutputPath "C:\DSC\Configurations"     # MOF 컴파일

Start-DscConfiguration -Path "C:\DSC\Configurations" -Wait -Verbose   # 즉시 적용, 진행 상황 출력
Start-DscConfiguration -Path "C:\DSC\Configurations"                    # 백그라운드 Job으로 적용(78장 개념 재사용)

Test-DscConfiguration                                                     # 현재 상태가 구성과 일치하는지만 확인(변경 없음)
Get-DscConfiguration                                                        # 마지막 적용 결과 조회

$Session = New-CimSession -ComputerName "Server01" -Credential (Get-Credential)   # 84장 방식으로 원격 세션
Start-DscConfiguration -Path "C:\DSC\Configurations" -CimSession $Session            # 원격 노드에 적용
```

## 주의사항·함정

**`DependsOn`을 명시하지 않으면 리소스 적용 순서가 보장되지 않는다**: 같은 `Node` 블록 안의 리소스들이 코드에 작성된 순서대로 항상 적용될 것이라고 가정하면 안 된다. "IIS 설치 후 웹 파일 복사"처럼 순서가 중요한 관계라면 `DependsOn`으로 명시적으로 지정해야 하며, 이를 빠뜨리면 웹 파일 복사가 IIS 설치보다 먼저 시도돼 실패할 수 있다.

**MOF 파일 이름은 노드 이름과 정확히 일치해야 한다**: `Start-DscConfiguration -Path`는 지정한 폴더에서 `<NetBIOS 이름>.mof` 형식의 파일을 찾는다. Configuration 블록의 `Node` 이름을 실제 대상 컴퓨터 이름과 다르게 쓰면, MOF 파일 이름이 어긋나 `Start-DscConfiguration`이 그 노드용 구성을 찾지 못한다.

**`Start-DscConfiguration`은 기본적으로 즉시 백그라운드 Job으로 반환된다**: `-Wait`를 빠뜨리면 명령이 곧바로 프롬프트로 돌아오고, 실제 적용은 78장에서 배운 것과 같은 백그라운드 작업으로 진행된다. 대화형으로 결과를 바로 확인하고 싶다면 `-Wait -Verbose`를 함께 써야 하며, 여러 노드에 병렬로 적용해야 한다면 오히려 기본 동작(Job)이 유리하다.

**`-Force` 없이 이미 진행 중인 구성 작업이 있으면 새 적용 요청이 거부된다**: 이전 `Start-DscConfiguration` 작업이 아직 끝나지 않은 상태에서 다시 호출하면 충돌 오류가 난다. `-Force`를 쓰면 진행 중이던 작업을 중단하고 새 작업을 시작하지만, 이는 108장에서 다룰 LCM의 `RefreshMode`를 `Pull`에서 `Push`로 강제 전환하는 부수 효과도 있다는 점을 감안해야 한다.

**이식성**: Terraform의 `terraform plan`(변경 사항 미리보기, `Test-DscConfiguration`과 유사)과 `terraform apply`(`Start-DscConfiguration`과 유사)가 "계획과 적용을 분리한다"는 점에서 DSC의 워크플로와 개념적으로 유사하다. Ansible의 플레이북 실행이 `ansible-playbook` 명령 하나로 즉시 적용되는 것과 달리, DSC는 컴파일(MOF 생성)이라는 중간 단계를 명시적으로 거친다는 점이 특징이다.

## Reference

- [Start-DscConfiguration (PSDesiredStateConfiguration) - PowerShell | Microsoft Learn](https://learn.microsoft.com/en-us/powershell/module/psdesiredstateconfiguration/start-dscconfiguration)
