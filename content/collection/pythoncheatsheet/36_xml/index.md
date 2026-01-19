---
draft: true
title: "[Python Cheatsheet] 36. XML - ElementTree로 XML 파싱/생성"
slug: "xml-elementtree-etree-parsing-xpath-element-attribute-namespace-find"
description: "파이썬 xml.etree.ElementTree를 빠르게 사용하기 위한 치트시트입니다. XML 파싱, XPath 검색, 요소 생성/수정, 네임스페이스 처리, 보안 주의점을 최소 예제로 정리합니다."
lastmod: 2026-01-18
collection_order: 36
tags:
  - python
  - Python
  - python3
  - 파이썬
  - cheatsheet
  - 치트시트
  - quick-reference
  - 빠른참조
  - xml
  - XML
  - ElementTree
  - etree
  - parsing
  - 파싱
  - xpath
  - element
  - 요소
  - attribute
  - 속성
  - namespace
  - 네임스페이스
  - xml-generation
  - XML생성
  - xml-modification
  - XML수정
  - fromstring
  - tostring
  - iterparse
  - find
  - findall
  - security
  - 보안
  - xxe
  - defusedxml
  - data-interchange
  - 데이터교환
  - config
  - 설정파일
  - standard-library
  - 표준라이브러리
  - patterns
  - 패턴
  - best-practices
  - 베스트프랙티스
---
`xml.etree.ElementTree`는 XML을 **파싱하고 생성**하는 표준 라이브러리입니다. 레거시 시스템 연동, 설정 파일 처리 등에 여전히 많이 사용됩니다.

## 언제 이 치트시트를 보나?

- **XML 파일을 읽고 파싱**해야 할 때
- **XML 응답을 처리**해야 할 때
- **XML 형식의 설정 파일**을 다룰 때

## 핵심 함수

```python
import xml.etree.ElementTree as ET

# 파싱
tree = ET.parse('file.xml')        # 파일에서
root = ET.fromstring(xml_string)   # 문자열에서

# 검색
root.find('tag')           # 첫 번째 매칭 요소
root.findall('tag')        # 모든 매칭 요소
root.iter('tag')           # 재귀적 순회

# 생성
ET.Element('tag')          # 요소 생성
ET.SubElement(parent, 'tag')  # 자식 요소 추가
ET.tostring(element)       # 문자열로 변환
```

## 최소 예제

### 1. XML 파싱 기본

```python
import xml.etree.ElementTree as ET

xml_string = """
<bookstore>
    <book category="fiction">
        <title>Harry Potter</title>
        <author>J.K. Rowling</author>
        <price>29.99</price>
    </book>
    <book category="tech">
        <title>Python Cookbook</title>
        <author>David Beazley</author>
        <price>49.99</price>
    </book>
</bookstore>
"""

root = ET.fromstring(xml_string)

# 루트 태그
print(root.tag)  # bookstore

# 모든 book 요소
for book in root.findall('book'):
    title = book.find('title').text
    category = book.get('category')
    print(f"{title} ({category})")
# Harry Potter (fiction)
# Python Cookbook (tech)
```

### 2. 파일에서 파싱

```python
import xml.etree.ElementTree as ET

# 파일 파싱
tree = ET.parse('books.xml')
root = tree.getroot()

# 또는 with 문
# with open('books.xml', 'r', encoding='utf-8') as f:
#     tree = ET.parse(f)
```

### 3. 속성과 텍스트 접근

```python
import xml.etree.ElementTree as ET

xml = '<item id="123" status="active">Item Text</item>'
element = ET.fromstring(xml)

# 태그명
print(element.tag)         # item

# 속성
print(element.get('id'))   # 123
print(element.attrib)      # {'id': '123', 'status': 'active'}

# 텍스트
print(element.text)        # Item Text
```

### 4. XPath 검색

```python
import xml.etree.ElementTree as ET

xml_string = """
<root>
    <users>
        <user id="1"><name>Alice</name></user>
        <user id="2"><name>Bob</name></user>
    </users>
</root>
"""

root = ET.fromstring(xml_string)

# 직접 자식에서 찾기
root.find('users')

# 모든 하위에서 찾기
root.find('.//user')           # 첫 번째 user
root.findall('.//user')        # 모든 user

# 속성으로 필터링
root.find(".//user[@id='2']")  # id="2"인 user

# 자식 요소가 있는 것
root.find(".//user[name]")     # name 자식이 있는 user
```

### 5. 순회 (iter)

```python
import xml.etree.ElementTree as ET

xml_string = """
<root>
    <a><b><c>text</c></b></a>
    <a><b>other</b></a>
</root>
"""

root = ET.fromstring(xml_string)

# 모든 하위 요소 순회
for elem in root.iter():
    print(elem.tag)
# root, a, b, c, a, b

# 특정 태그만
for b in root.iter('b'):
    print(b.text)
```

### 6. XML 생성

```python
import xml.etree.ElementTree as ET

# 루트 요소 생성
root = ET.Element('bookstore')

# 자식 요소 추가
book = ET.SubElement(root, 'book', category='fiction')
title = ET.SubElement(book, 'title')
title.text = 'Harry Potter'
author = ET.SubElement(book, 'author')
author.text = 'J.K. Rowling'

# 문자열로 변환
xml_str = ET.tostring(root, encoding='unicode')
print(xml_str)
# <bookstore><book category="fiction"><title>Harry Potter</title><author>J.K. Rowling</author></book></bookstore>
```

### 7. 예쁘게 출력 (Python 3.9+)

```python
import xml.etree.ElementTree as ET

root = ET.Element('root')
child = ET.SubElement(root, 'child')
child.text = 'text'

# indent 함수 (Python 3.9+)
ET.indent(root)
print(ET.tostring(root, encoding='unicode'))
# <root>
#   <child>text</child>
# </root>
```

### 8. 파일에 저장

```python
import xml.etree.ElementTree as ET

root = ET.Element('data')
ET.SubElement(root, 'item').text = 'value'

tree = ET.ElementTree(root)

# XML 선언 포함하여 저장
tree.write('output.xml', encoding='utf-8', xml_declaration=True)
```

### 9. 요소 수정/삭제

```python
import xml.etree.ElementTree as ET

xml = '<root><item>old</item></root>'
root = ET.fromstring(xml)

# 텍스트 수정
item = root.find('item')
item.text = 'new'

# 속성 추가/수정
item.set('id', '123')

# 요소 삭제
root.remove(item)

# 새 요소 삽입
new_item = ET.Element('new_item')
root.insert(0, new_item)
```

### 10. 네임스페이스 처리

```python
import xml.etree.ElementTree as ET

xml_string = """
<root xmlns="http://example.com/ns" xmlns:custom="http://example.com/custom">
    <item>Default NS</item>
    <custom:item>Custom NS</custom:item>
</root>
"""

root = ET.fromstring(xml_string)

# 네임스페이스 매핑
ns = {
    'default': 'http://example.com/ns',
    'custom': 'http://example.com/custom'
}

# 네임스페이스 포함하여 검색
root.find('default:item', ns)
root.find('custom:item', ns)

# 또는 전체 URI 사용
root.find('{http://example.com/ns}item')
```

### 11. 대용량 파일 - iterparse

```python
import xml.etree.ElementTree as ET

# 메모리 효율적인 파싱
for event, elem in ET.iterparse('large.xml', events=('end',)):
    if elem.tag == 'item':
        process(elem)
        elem.clear()  # 메모리 해제
```

## 보안 주의 (XXE 공격)

```python
# 위험: 외부 엔터티 확장 (XXE) 공격에 취약
import xml.etree.ElementTree as ET
# ET.fromstring(untrusted_xml)  # 위험할 수 있음

# 안전: defusedxml 사용
# pip install defusedxml
import defusedxml.ElementTree as SafeET
root = SafeET.fromstring(untrusted_xml)
```

## 자주 하는 실수

### 1. 빈 텍스트 접근

```python
import xml.etree.ElementTree as ET

xml = '<root><item></item></root>'
root = ET.fromstring(xml)

item = root.find('item')
print(item.text)  # None (빈 문자열 아님!)

# 안전하게 접근
text = item.text or ''
```

### 2. 네임스페이스 무시

```python
# 네임스페이스가 있으면 find가 실패함
xml = '<root xmlns="http://example.com"><item/></root>'
root = ET.fromstring(xml)

root.find('item')  # None!
root.find('{http://example.com}item')  # OK
```

## 한눈에 정리

| 작업 | 함수/메서드 |
|------|------------|
| 파일 파싱 | `ET.parse(file)` |
| 문자열 파싱 | `ET.fromstring(str)` |
| 요소 찾기 | `find()`, `findall()`, `iter()` |
| 요소 생성 | `ET.Element()`, `ET.SubElement()` |
| 문자열 변환 | `ET.tostring()` |
| 파일 저장 | `tree.write()` |

## 참고

- [xml.etree.ElementTree - Python Docs](https://docs.python.org/3/library/xml.etree.elementtree.html)
- [defusedxml - Safe XML parsing](https://github.com/tiran/defusedxml)
