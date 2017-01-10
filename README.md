# Git-History-Scanner
run regexes against git history ideally to discover secrets. I make no guarantee that it is a currently working version as it is still in development.


To eddit the regexes, modify them in the check_for_creds fuction up top. each is an array of compiled regexes separated into secret type.

a new for loop will need to be made for each cred type (I know this is not efficient but it got it working).
