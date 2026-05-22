# Stupor Bowl API

This is the API for the yearly word-of-mouth competition amongst friends/family known as the Stupor Bowl.

Interesting points:
- no money is involved, but users answer a series of "prop bet" style questions to earn points and when the game is over, the "real" answers are posted and the system tallies the results, with the "winner" being the one with most points.
- API is Python 3.13 served by a MariaDB database and hosted on a single EC2 in AWS running Docker
- data access is through GraphQL using Django/Strawberry
- admin access is controlled through Django
- users self-register using an email address and name (no other PI is stored)
- SSL service done through self-signed certs (let's encrypt)
- access to subdomains handled through a Traefik reverse proxy
