---

title: "[Linux] Change Ubuntu 14.04 from DHCP to Static IP Addredd"
description: "Change Ubuntu 14.04 from DHCP to Static IP Addredd"
categories: [Ubuntu,Linux]
tags: [Ubuntu, Linux, IP, setup, setting, Shell]
redirect_from:
  - /2019/02/26/
last_modified_at : 2022-04-15
---



# Use shell command
If the Ubuntu Server installer has set your server to use DHCP, you will want to change it to a static IP address so that people can actually use it.

Changing this setting without a GUI will require some text editing, but that ?s classic linux, right?

Open up the /etc/network/interfaces file

``` bash
vi /etc/network/interfaces
```

For the primary interface, which is usually eth0, you will see these lines:

``` bash
auto eth0
iface eth0 inet dhcp
```

As you can see, it ?s using DHCP right now. We are going to change dhcp to static, and then there are a number of options that should be added below it. Obviously you ?d customize this to your network.

``` bash
# The primary network interface
auto eth0
iface eth0 inet static
address xxx.xxx.xxx.xxx
netmask xxx.xxx.xxx.xxx
gateway xxx.xxx.xxx.xxx
dns-nameservers xxx.xxx.xxx.xxx
```

Now we will just need to restart the networking components:

``` bash
sudo /etc/init.d/networking restart
```
