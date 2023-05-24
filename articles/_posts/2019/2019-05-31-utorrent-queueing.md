---
title: "[µtorrent] µtorrent queueing policy"
categories: [uTorrent]
tags: [Torrent, µTorrent, uTorrent, seeding, queueing, Goal]
---

# Queueing

## Queue Settings

* The **Maximum number of active torrents** field defines the maximum number of unforced torrent jobs that µTorrent will allow to be active before placing it on the queue. Torrent jobs are counted regardless of whether they're seeding or downloading torrents, as long as they are uploading at rates above the value specified by queue.slow_ul_threshold or downloading at rates above the value specified by queue.slow_dl_threshold.
* The **Maximum number of active downloadls** field defines the maximum number of unforced torrent jobs that µTorrent will allow to be downloaded before making it wait on the download queue. This option only applies to torrent jobs that are downloading or are to be placed in downloading mode.

## Seeding Goal

* The **Minimum ratio** field allows you to set the ratio that you wish to reach before µTorrent throttles the speed for the torrent job (or stops it, if you set it to do so). Setting the ratio to -1 is equivalent to setting it to unlimited. Setting this value to 0 tells µTorrent to ignore this value and look only at the seeding time limit. This value is interpreted as a percentage. µTorrent will throttle the seeding process only after both this and time limit have been reached.
* The **Minimum seeding time** field allows you to specify the minimum amount of time you wish for the torrent job to continue seeding at normal speeds after it has finished downloading. µTorrent will throttle the seeding process only after both this and the ratio threshold have been reached. This value is interpreted in minutes.
* **Seeding tasks have higher priority than downloading tasks** will give seeding tasks higher priority than downloads, so if your maximum number of active torrents is reached, and a torrent job reaches seeding state, the downloading tasks will not force it into queued seeding state.
* Minimum number of available seeds  will keep seeding till the specified number of seeds are available for this torrent

> Note: These values only affect torrent jobs added after they are set. Existing torrent jobs will retain their current seeding goals, even if these default settings are modified.

## When µTorrent Reaches the Seeding Goal

* The **Limit the upload rate to** field allows you to set the speed that µTorrent throttles the upload speed for a torrent job to when it reaches the seeding goal set. Setting this value to 0 is equivalent to telling µTorrent to stop the torrent job. A change to this value affects only torrent jobs that have not yet reached their seeding goals. This value is interpreted in KiB/s, so please enter it as such.