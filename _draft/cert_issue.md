Title: acme.sh and the wildcard DNS
Date: 2026-3-3
Tags: bullshit, tech,
Category: Blog
Author: hugu
Summary: wildcard subdomain is wild


---

periodically i renew the ssl certifications for my personal blog (another pelican shit but in chinese) and some other shady crazy xyz domains which mostly for *proxy testing* on my vps with [acme.sh](https://acme.sh), a bash script renewing certifications by creating cron jobs, it works so fucking smooth that i haven't configured it for many years but recently there was a weird problem: the auto renew process dose not work as usual, it outputted something like 'can not write the txt DNS records', and afterwards died.

thus i began to search and complain in chatGPT, several years ago both zerossl and let's encrypt ended the wildcard subdomain certs for free tier users and it did caused some vaguely similar problems so i checked the acme config, actually i deleted all the outdated certs and pushed cmd 'acme.sh --renew -f' through... it failed again.

so i regenerated a new fucking API key on namesilo, the old slow shit website where my domains are hosted, and then rewrote the DNS nameservers with the namesilo default ones ...btw the chatGPT thought the default nameservers on namesilo is something "namesilo.com" but actulally it is all DNSOWL.COM etc etc. 

after the api refresh and nameserver panic the acme script was still malfunctioning unfortunately. so i made the desperate move and put `--log` in acme renew cmd, yes indeed, i really readed the fucking log file on my console, with my own eyes, it said "cannot write txt DNS records while wildcard subdomain DNS records being written", something like that.

with all respect to the devs working on something like acme.sh, the log part is uncontroversially the most notorious job for everyone, i, for one, do really hate reading logs. 

by the way, kuma the monitor is a great monitor service for checking website certs validity and accessibility especially when you have a telegram notification key, it just works.


my eyes still hurts a little bit.




<br><br><br><br><br><br>

