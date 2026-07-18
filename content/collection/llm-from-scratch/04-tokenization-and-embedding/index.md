---
collection_order: 4
date: 2026-07-17
lastmod: 2026-07-17
draft: false
title: "[LLM] 04. 토크나이징과 임베딩 — 텍스트를 벡터로"
slug: tokenization-and-embedding
description: "텍스트를 토큰 ID로 바꾸는 토크나이징, 토큰을 벡터로 바꾸는 임베딩, 그리고 절대·상대 위치 인코딩과 RoPE까지 GPT 입력 표현을 다룹니다. PyTorch Dataset/DataLoader 구현 예제를 포함합니다."
tags:
  - LLM(Large Language Model)
  - Transformer
  - Tokenization(토크나이징)
  - Embedding(임베딩)
  - GPT(Generative Pre-trained Transformer)
  - Attention(어텐션)
  - Neural-Network
  - Deep-Learning(딥러닝)
  - Machine-Learning(머신러닝)
  - NLP(Natural Language Processing)
  - AI(인공지능)
  - PyTorch
  - Hugging-Face
  - Data-Science(데이터사이언스)
  - Curriculum
  - 커리큘럼
  - Tutorial(튜토리얼)
  - Guide(가이드)
  - Deep-Dive
  - Education(교육)
  - Beginner
  - Advanced
  - Reference(참고)
  - Implementation(구현)
  - Best-Practices
  - Prompt-Engineering(프롬프트엔지니어링)
  - ChatGPT

---

Transformer는 03장에서 본 것처럼 문장 전체를 한 번에 병렬로 입력받습니다. 하지만 신경망은 숫자 연산만 할 수 있고, 병렬로 넣는 순간 "몇 번째 단어인가"라는 순서 정보는 저절로 사라집니다. 이 장은 문장을 모델이 받아들일 수 있는 숫자로 바꾸는 과정 — 토크나이징과 임베딩 — 과, 사라진 순서 정보를 되살리는 위치 인코딩을 다룹니다.

## 토크나이징 — 문장을 토큰 ID로

**토크나이징(Tokenizing)**은 문장을 의미 단위로 잘라 정수 ID의 나열로 바꾸는 과정입니다. 이 나열이 모델의 실제 입력이 됩니다. 가장 단순한 방법은 공백 단위로 자르는 것이지만, 이렇게 하면 사전에 없는 단어(신조어, 오타, 외국어)를 처리할 수 없다는 문제가 생깁니다. 이를 해결한 것이 **BPE(Byte Pair Encoding)** 같은 서브워드 토크나이징으로, 자주 등장하는 문자열은 하나의 토큰으로 길게 묶고 드문 문자열은 더 잘게 쪼갭니다. 이 방식은 사전에 없는 단어도 알파벳 단위까지 쪼개서 표현할 수 있어 어휘 밖 단어(out-of-vocabulary) 문제가 사실상 사라집니다.

```python
import tiktoken

tokenizer = tiktoken.get_encoding("gpt2")
text = "LLM 밑바닥부터 이해하기"
token_ids = tokenizer.encode(text)

print(token_ids)                       # 정수 ID의 나열
print(tokenizer.decode(token_ids))     # 다시 원문으로 복원 가능
```

`tiktoken`은 OpenAI가 공개한 BPE 토크나이저 구현으로, GPT-2/GPT-3 계열 모델이 실제로 사용하는 어휘 사전을 그대로 씁니다. `encode`와 `decode`가 서로의 역연산이라는 점(토큰화해도 정보 손실 없이 원문을 복원할 수 있다는 점)이 토크나이저 설계의 핵심 제약입니다.

## 토큰 임베딩 — ID를 의미 벡터로

토큰 ID 자체는 단순한 순번이라 "5번 토큰이 3번 토큰보다 의미가 크다"는 식의 관계가 없습니다. **토큰 임베딩(Token Embedding)**은 각 토큰 ID를 학습 가능한 N차원 벡터로 대응시키는 조회 테이블(lookup table)입니다. "임베딩"이라는 말 자체가 어떤 대상을 N차원 벡터 공간의 한 점으로 표현한다는 뜻이며, 01장에서 다룬 코사인 유사도로 두 토큰(또는 문장)의 의미적 유사도를 잴 수 있는 것도 이 임베딩 덕분입니다.

```python
import torch.nn as nn

vocab_size = 50257     # GPT-2 어휘 사전 크기
emb_dim = 768           # 임베딩 차원

token_embedding = nn.Embedding(vocab_size, emb_dim)
# token_embedding.weight의 shape: (50257, 768)
# 토큰 ID를 인덱스로 찍으면 해당하는 768차원 벡터를 반환한다
```

`nn.Embedding`은 내부적으로 `(vocab_size, emb_dim)` 크기의 행렬을 갖고 있을 뿐이며, 학습 초기에는 무작위 값으로 채워져 있다가 학습이 진행되면서 의미가 비슷한 토큰끼리 가까운 벡터를 갖도록 조정됩니다.

## 위치 인코딩 — 사라진 순서 정보를 되살리기

`Tom ate the dog`과 `The dog ate Tom`은 같은 토큰들로 이루어졌지만 완전히 다른 의미입니다. 하지만 Transformer는 모든 토큰을 동시에 입력받기 때문에, 토큰 임베딩만으로는 이 둘을 구분할 수 없습니다. 그래서 토큰 임베딩과 같은 차원의 **위치 임베딩(Positional Embedding)**을 별도로 만들어 더해줍니다.

$$\text{입력 임베딩} = \text{토큰 임베딩} + \text{위치 임베딩}$$

위치 정보를 인코딩하는 방식은 세 갈래로 발전했습니다.

| 방식 | 인코딩 대상 | 장점 | 단점 |
|---|---|---|---|
| 절대 위치 인코딩 | 1, 2, 3, ... 같은 절대 순번을 sin·cos 함수로 변환 | 구현이 단순 | 토큰 간 상대적 거리 정보를 직접 담지 못함 |
| 상대 위치 인코딩 | 두 토큰 사이의 거리 | 상대적 거리가 중요한 언어 구조에 안정적 | 계산이 느리고 KV 캐싱(12장)과 상성이 나쁨 |
| RoPE(Rotary Position Embedding) | 위치에 따라 벡터를 회전 | 절대·상대 위치 정보를 모두 담으면서 계산 효율 유지 | 구현이 앞의 두 방식보다 복잡 |

절대 위치 인코딩은 짝수 차원에 sin, 홀수 차원에 cos 함수를 사용합니다.

$$PE_{(pos, 2i)} = \sin\left(\frac{pos}{10000^{2i/d}}\right), \quad PE_{(pos, 2i+1)} = \cos\left(\frac{pos}{10000^{2i/d}}\right)$$

**RoPE**는 위치 벡터를 더하는 대신 회전시킵니다. 회전 각도는 위치가 뒤로 갈수록 커지지만, 두 토큰 사이의 상대적 회전각(거리)은 문장 내 절대 위치와 무관하게 항상 일정하게 보존됩니다. 절대 위치와 상대 위치 정보를 동시에 담을 수 있다는 이 성질 때문에 최근 대부분의 LLM이 RoPE를 채택합니다.

> Jianlin Su, Yu Lu, Shengfeng Pan 외, "RoFormer: Enhanced Transformer with Rotary Position Embedding", *arXiv:2104.09864* (2021)

## Self-Supervised 데이터셋 구성

GPT류 모델의 사전학습은 사람이 직접 라벨을 붙이지 않고, 텍스트 자체가 정답이 되는 **Self-Supervised** 방식을 씁니다. 원리는 단순합니다 — 긴 텍스트를 원하는 길이(컨텍스트 길이)만큼 자르고, 타깃(정답)은 입력을 한 토큰만큼 뒤로 민 것으로 만듭니다.

```
입력:  In the heart of  →  타깃: the heart of the
```

이 슬라이딩 윈도우 방식을 데이터셋 클래스로 구현하면 다음과 같습니다.

```python
import torch
from torch.utils.data import Dataset, DataLoader

class GPTDatasetV1(Dataset):
    def __init__(self, token_ids: list[int], max_length: int, stride: int):
        self.input_ids = []
        self.target_ids = []
        for i in range(0, len(token_ids) - max_length, stride):
            self.input_ids.append(torch.tensor(token_ids[i:i + max_length]))
            self.target_ids.append(torch.tensor(token_ids[i + 1:i + max_length + 1]))

    def __len__(self) -> int:
        return len(self.input_ids)

    def __getitem__(self, idx: int):
        return self.input_ids[idx], self.target_ids[idx]

dataset = GPTDatasetV1(token_ids=list(range(1000)), max_length=8, stride=4)
loader = DataLoader(dataset, batch_size=2, shuffle=True)
```

`max_length` 길이의 창을 `stride` 간격으로 밀어가며 입력 청크(`token_ids[i:i+max_length]`)와 타깃 청크(한 토큰 뒤로 민 것)를 쌍으로 만듭니다. `__len__`은 전체 샘플 개수, `__getitem__`은 인덱스에 해당하는 입력·타깃 쌍을 반환하며, `DataLoader`가 이를 배치 단위로 묶고 섞는(shuffle) 역할을 합니다. `stride`를 `max_length`보다 작게 잡으면 윈도우가 겹치면서 같은 텍스트 구간이 여러 샘플에 중복으로 포함됩니다.

## 흔한 오개념 — "위치 인코딩은 그냥 순서 번호를 붙이는 것이다"

위치 인코딩을 "1번째, 2번째, ..."처럼 순번을 매기는 것으로 단순화해 이해하기 쉽지만, 실제로 절대 위치 인코딩조차 정수를 그대로 쓰지 않고 sin·cos 함수로 변환합니다. 이유는 두 가지입니다. 첫째, 정수를 그대로 더하면 문장이 길어질수록 값의 크기가 무한정 커져 학습이 불안정해집니다. 둘째, sin·cos 조합은 차원마다 다른 주기를 갖도록 설계되어 있어, 가까운 위치끼리는 벡터가 비슷하고 먼 위치일수록 벡터가 달라지는 "거리에 비례한 유사도"를 자연스럽게 만들어냅니다. RoPE가 상대 위치 정보를 잘 보존하는 것도 이 성질을 회전이라는 형태로 더 명시적으로 구현했기 때문입니다.

다음 장에서는 이렇게 만들어진 입력 임베딩이 Self-Attention을 거치며 Query·Key·Value로 어떻게 나뉘고, 왜 굳이 세 가지로 나눠야 하는지를 다룹니다.
