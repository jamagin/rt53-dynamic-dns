import subprocess

def ipv4():
	return subprocess.check_output('dig +short @resolver1.opendns.com myip.opendns.com', shell=True)
