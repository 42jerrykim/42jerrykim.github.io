---
draft: false
collection_order: 106
slug: dsc-concept-architecture-powershell
title: "[PowerShell] 106. DSC 개념과 아키텍처"
date: 2026-08-29
lastmod: 2026-08-29
description: "PowerShell DSC(Desired State Configuration)가 선언적으로 시스템 상태를 정의하는 원리와 Configuration/MOF/LCM으로 이뤄진 고전 아키텍처, 새로 등장한 크로스플랫폼 DSC v3와의 차이를 정리한 Part 15 시작 챕터다."
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
- Desired-State-Configuration
- Declarative-Configuration
- MOF-File
- Idempotent
- Configuration-Drift
- Infrastructure-As-Code
image: "wordcloud.png"
---

## 개요

<strong>DSC(Desired State Configuration)</strong>는 "이 서버가 어떤 명령을 순서대로 실행해야 하는가"가 아니라 "이 서버가 최종적으로 어떤 **상태**여야 하는가"를 선언적으로 기술하는 구성 관리 플랫폼이다. 92장에서 배운 예약 작업이 "언제 무엇을 실행할지"를 다뤘다면, DSC는 "무엇이 참이어야 하는지"를 다룬다는 점에서 근본적으로 다른 사고방식을 요구하며 Part 15를 시작한다.

정신 모델은 "명령형(imperative) 스크립트가 요리 순서를 하나하나 지시하는 레시피라면, DSC는 완성된 요리 사진만 보여주고 그 사진과 다르면 알아서 고치라고 맡기는 것"이라는 것이다. 이 선언 방식 덕분에 DSC는 <strong>멱등성(idempotent)</strong>을 갖는다 — 같은 구성을 몇 번을 적용해도 결과는 항상 같다.

## 사용법

```powershell
Configuration <이름> {
    Node <대상노드> {
        <리소스이름> <별칭> { <속성> = <값> }
    }
}
```

## 종류

| 구성 요소 | 역할 |
|---|---|
| **Configuration** 블록 | DSC 구성을 정의하는 PowerShell 함수형 스크립트 |
| **DSC 리소스** | 파일·서비스·레지스트리 값 등 특정 구성 요소를 관리하는 단위(`Get`/`Test`/`Set` 세 동작 지원) |
| **MOF 파일** | Configuration 블록을 컴파일한 결과물, 실제로 노드에 적용되는 표준화된 구성 문서 |
| **LCM(로컬 구성 관리자)** | 각 노드에서 MOF 파일을 실제로 적용·감시하는 엔진(108장에서 자세히 다룸) |
| **DSC v3**(신규) | PowerShell에 의존하지 않는 완전히 새로운 크로스플랫폼 CLI 도구, LCM 없이 `dsc` 명령으로 직접 호출 |

## 예시

```powershell
Configuration WebServerConfig {
    Node "localhost" {
        WindowsFeature IIS {
            Ensure = "Present"
            Name   = "Web-Server"
        }
        File WebContent {
            Ensure          = "Present"
            SourcePath      = "\\Server\Share\index.html"
            DestinationPath = "C:\inetpub\wwwroot\index.html"
            DependsOn       = "[WindowsFeature]IIS"     # 리소스 간 순서 지정
        }
    }
}

WebServerConfig -OutputPath "C:\DSC\Configurations"       # Configuration 블록 실행 → MOF 파일 생성
# 결과: C:\DSC\Configurations\localhost.mof

Get-DscResource                                              # 사용 가능한 DSC 리소스 목록 확인
Get-DscResource -Name WindowsFeature | Select-Object Properties -ExpandProperty Properties   # 리소스가 다루는 속성 확인
```

## 주의사항·함정

**"DSC"라는 이름이 서로 다른 두 세대의 기술을 동시에 가리켜 혼동하기 쉽다**: 이 장에서 다루는 고전 DSC(`Configuration` 키워드, MOF 파일, LCM)는 Windows PowerShell 5.0/5.1에 깊이 통합된 기술이다. Microsoft는 이후 PowerShell에 의존하지 않는 완전히 새로운 크로스플랫폼 `dsc` 명령줄 도구(DSC v3)를 별도로 내놓았는데, 이쪽은 MOF 대신 JSON/YAML 구성 문서를 쓰고 LCM 자체가 없다 — 서비스로 동작하지 않고 명령으로 즉시 실행되는 구조다. 이 시리즈 106–108장은 `Configuration`/MOF/LCM 기반의 **고전 DSC**를 다루며, 최신 크로스플랫폼 자동화가 목적이라면 DSC v3도 별도로 조사해야 한다.

**Configuration 블록은 함수처럼 보이지만 실행 결과가 즉시 시스템에 적용되지 않는다**: `WebServerConfig`를 실행하면 그 자리에서 IIS가 설치되는 것이 아니라, 그 구성을 기술한 MOF 파일이 생성될 뿐이다. 실제 적용은 107장에서 다룰 `Start-DscConfiguration`이라는 별도 단계가 필요하다 — 이 "정의"와 "적용"의 분리를 이해하지 못하면 Configuration을 실행했는데 왜 아무 변화가 없는지 혼란스러울 수 있다.

**DSC 리소스가 모든 구성 요소를 다 지원하는 것은 아니다**: 원하는 설정을 관리할 표준 DSC 리소스가 없다면, 직접 사용자 정의 리소스를 만들거나 `Script` 리소스(임의의 PowerShell 코드를 `Get`/`Test`/`Set`으로 감싸는 범용 리소스)로 우회해야 한다.

**고전 DSC는 사실상 Windows PowerShell/Windows 환경에 묶여 있다**: PowerShell 7에서도 `PSDesiredStateConfiguration` 모듈을 설치해 Configuration을 작성할 수는 있지만, LCM 기반의 실제 적용·모니터링 체계는 근본적으로 Windows PowerShell 생태계의 기능이다. 크로스플랫폼 환경(Linux/macOS)에서 선언적 구성 관리가 필요하다면 DSC v3나 Ansible 같은 별도 도구를 고려해야 한다.

**이식성**: Ansible의 플레이북, Puppet의 매니페스트, Chef의 레시피가 모두 "선언적으로 원하는 상태를 기술한다"는 같은 철학을 공유한다. DSC의 MOF 파일은 CIM(Common Information Model) 표준을 기반으로 하는데, 이는 94장에서 다룬 `Get-CimInstance`와 같은 CIM 인프라 위에 구축됐다는 뜻이다 — DSC가 단순한 스크립트 모음이 아니라 Windows 관리 인프라 전체와 통합된 기술이라는 점을 보여준다.

## Reference

- [Microsoft Desired State Configuration overview - PowerShell | Microsoft Learn](https://learn.microsoft.com/en-us/powershell/dsc/overview)
