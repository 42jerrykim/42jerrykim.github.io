---
title: "Remove all docker container"
description: "Remove all docker container"
categories: [Docker]
tags: [Docker, Container, Delete, Stop]
---

도커에서 컨테이너를 사용하는 방법에 대해서 알아 본다.

# 1. Remove a container
To delete a container, you first need to know the ID of the container. The ID of the container can be obtained through ```docker ps -a```

You can delete one or more containers by typing ```docker rm [CONTAINER]``` in the terminal

In addition, check the following:
```
$ docker rm --help

Usage:	docker rm [OPTIONS] CONTAINER [CONTAINER...]

Remove one or more containers

Options:
  -f, --force     Force the removal of a running container (uses SIGKILL)
  -l, --link      Remove the specified link
  -v, --volumes   Remove the volumes associated with the container
```

# 2. List up containers
To see active docker container, type below shell script to terminal
```
docker ps
```

If you want to see all the container that not active, add ```-a``` or ```--all``` option
```
docker ps -a
docker ps --all
```

# 3. Remove all container
You can delete the container one by one using the above command, but you can delete all containers at once by using the ```-q``` option and ```$( ... )```

Since the container will not be deleted while it is in operation, use ```docker stop [CONTAINER]``` to stop the container and remove it.
```
docker stop $(docker ps -a -q)
docker rm $(docker ps -a -q)
```

In addition, check the following:
```
$ docker rm --help

Usage:	docker rm [OPTIONS] CONTAINER [CONTAINER...]

Remove one or more containers

Options:
  -f, --force     Force the removal of a running container (uses SIGKILL)
  -l, --link      Remove the specified link
  -v, --volumes   Remove the volumes associated with the container
```
```
$ docker stop --help

Usage:	docker stop [OPTIONS] CONTAINER [CONTAINER...]

Stop one or more running containers

Options:
  -t, --time int   Seconds to wait for stop before killing it (default 10)
```
