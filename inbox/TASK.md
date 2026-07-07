DIAGNOSTIKA — atsiskaityk lietuviškai, TIK tirk/skaityk, NIEKO nekeisk ir necommitink.

Kontekstas: vartotojas per Telegram įkėlė failą į „PARSER"/„HERA" botą. Botas atsakė:
„📥 Failas priimtas — kompas dabar nepasiekiamas, HERA apdoros kai atsibus."
Reikia rasti tą botą VPS'e ir suprasti, kodėl worker'is („kompas"/HERA) neveikia.

1. Ieškok VISUR: grep -ri po /root /opt /home /etc dėl: HERA, PARSER,
   "Failas priimtas", "nepasiekiamas", "atsibus", "apdoros", telegram bot token.
2. n8n: `docker exec -u node n8n-n8n-1 n8n list:workflow` — ar yra parser/HERA workflow;
   jei yra, parodyk jo webhook/nodes esmę.
3. Kas veikia: `ps aux | grep -iE 'hera|parser|bot|telegram'`,
   `systemctl list-units --type=service | grep -iE 'hera|parser|bot'`,
   `crontab -l; ls -la /etc/cron.d`, `docker ps`.
4. Kur atsiguli priimti failai (queue katalogas/DB/volume)? Ar vartotojo failas ten yra?
5. Nustatyk: (a) kur botas PRIIMA failus, (b) kur turi APDOROTI (HERA worker),
   (c) KODĖL worker'is „nepasiekiamas" — ar užkoduotas laptopo host/IP/kelias?

Į Telegram atsiskaityk trumpai: rastas botas ar ne, kur guli kodas, kas veikia / kas ne,
ar įkeltas failas eilėje saugus, ir KĄ reikia pataisyti, kad HERA suktųsi VPS'e. Nieko nekeisk.
