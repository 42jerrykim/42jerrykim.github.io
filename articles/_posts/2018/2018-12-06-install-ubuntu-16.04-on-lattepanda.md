---
title: "Install Ubuntu 16.04 on LattePanda Alpha"
description: "install Ubuntu 16.04 on LattePanda Alpha"
categories: [LattePanda]
tags: [lattepanda, ubuntu, linux]
redirect_from:
  - /2018/12/06/
---

라테판다에 이미지 설치 하는 방법

# Get Ubuntu 16.04 LTS
Get a Ubuntu ISO from: http://releases.ubuntu.com/xenial/ -amd64.iso
# Make booting USB
Use your favourite disk writing tool (Etcher, Rufus, etc) to burn the ISO on to the USB or SD Card.
# Install Ubuntu 
1. Once that is done, boot on to your LattePanda, press the <kbd>DEL</kbd> key until you see the BIOS and disable secure boot in Security->Secure Boot->Secure Boot Enable = Disabled and set Secure Boot Mode to Custom.
2. Save changes and exit.
2. Insert your USB/SD Card and press <kbd>F7</kbd> for the boot menu and select the ubuntu UEFI entry (Should come up as 'UEFI Generic....')
3. Select 'Install Ubuntu'.
4. Once it boots to the desktop, go through the options that you need until you hit 'Installation Type' (You can either wipe Windows or Install along side it if you want to keep Windows.)
5. After this step, it seems to be a typical Ubuntu Installation process.
