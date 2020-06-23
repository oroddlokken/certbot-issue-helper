#!/usr/bin/env python3

import os.path
import subprocess
import shutil

# https://certbot.eff.org/docs/using.html


def main(args):
    # Best email validation ever
    if not args.disable_email_validation and "@" not in args.email:
        raise ValueError(
            "Are you sure {} is a valid email address".format(args.email))

    if not args.print_cmd_only and not shutil.which(args.certbot_path):
        raise OSError("Certbot is not installed or in your PATH")

    os.makedirs(args.tmp_path, exist_ok=True)

    certbot_cmd = [args.certbot_path, 'certonly',
                   '-n',
                   '--renew-by-default',
                   '--expand',
                   '--agree-tos',
                   '--email', args.email,
                   '-a', 'webroot',
                   '--webroot-path={}'.format(args.tmp_path)]

    if args.test_cert:
        certbot_cmd += ["--test-cert", ]

    for d in args.domains:
        certbot_cmd += ['-d', d]

    print("Certbot command: ")
    print(subprocess.list2cmdline(certbot_cmd))

    if not args.print_cmd_only:
        subprocess.call(certbot_cmd)

        if args.reload_cmd:
            reload_cmd = args.reload_cmd.split(" ")
            subprocess.call(reload_cmd)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="Fetch a certificate from Let's Encrypt")
    parser.add_argument('email', type=str,
                        help='The email to associate the domain with.')
    parser.add_argument('domains', metavar='domain', type=str, nargs='+',
                        help='The domains to grab a certificate for.')

    parser.add_argument('--tmp-path', default="/tmp/letsencrypt-auto",
                        help='Temporary folder for certbot')

    parser.add_argument('--certbot-path', default="certbot",
                        help='Override the path for certbot')
    parser.add_argument('--print-cmd-only', default=False, action="store_true",
                        help="Only print the certbot command, don't run it.")
    parser.add_argument('--disable-email-validation',
                        default=False, action="store_true",
                        help="Don't attempt to validate the email address.")
    parser.add_argument('--reload-cmd', default=False,
                        help='Run a command after obtaining the certificate')

    parser.add_argument('--test-cert',
                        default=False, action="store_true",
                        help="Obtain a test certificate from a staging server")

    args = parser.parse_args()

    main(args)
