# Certbot-helper

I don't like certbot trying to edit my nginx.conf, I'd much rather have control over that myself.  But it's not like I remember how to use certbot manually either.  
This is my little helper script for issuing certificates with certbot.  

To renew them I use `certbot renew`.

## Example:
```
./certbot-helper.py "post1@example.com" a.e.f.4.example.com
Certbot command: 
certbot certonly -n --renew-by-default --expand --agree-tos --email post1@example.com -a webroot --webroot-path=/tmp/letsencrypt-auto -d a.e.f.4.example.com
Saving debug log to /var/log/letsencrypt/letsencrypt.log
Plugins selected: Authenticator webroot, Installer None
Obtaining a new certificate
Performing the following challenges:
http-01 challenge for a.e.f.4.example.com
Using the webroot path /tmp/letsencrypt-auto for all unmatched domains.
Waiting for verification...
Cleaning up challenges

IMPORTANT NOTES:
 - Congratulations! Your certificate and chain have been saved at:
   /usr/local/etc/letsencrypt/live/a.e.f.4.example.com/fullchain.pem
   Your key file has been saved at:
   /usr/local/etc/letsencrypt/live/a.e.f.4.example.com/privkey.pem
   Your cert will expire on 2020-08-14. To obtain a new or tweaked
   version of this certificate in the future, simply run certbot
   again. To non-interactively renew *all* of your certificates, run
   "certbot renew"
 - If you like Certbot, please consider supporting our work by:

   Donating to ISRG / Let's Encrypt:   https://letsencrypt.org/donate
   Donating to EFF:                    https://eff.org/donate-le
```

## My nginx.config:
```
    # HTTP - Catch all
    server {
        listen 80 default;
        server_name localhost;

        location '/.well-known/acme-challenge' {
            default_type "text/plain";
            root /tmp/letsencrypt-auto;
        }

        location / {
            return         301 https://$host$request_uri;
        }

    }

    # HTTPS - a.e.f.4.example.com
    server {
        listen 443 ssl;
        server_name a.e.f.4.example.com;

        ssl_certificate /usr/local/etc/letsencrypt/live/a.e.f.4.example.com/fullchain.pem;
        ssl_certificate_key /usr/local/etc/letsencrypt/live/a.e.f.4.example.com/privkey.pem;

        access_log /zroot/data/www/logs/nginx/a.e.f.4.example.com.log;

        autoindex on;
        charset utf-8;

        location / {
            proxy_pass http://172.25.10.81/;
            proxy_set_header        X-Real-IP       $remote_addr;
            proxy_set_header        X-Forwarded-For $proxy_add_x_forwarded_for;
        }

    }
```
