#Inspired by https://github.com/dxa4481/truffleHog
#except using regexes instead of searching for high entropy strings
#Requirement: Python3 and GitPython 2.1.1

import sys
import math
import datetime
import argparse
import tempfile
from git import Repo
import re
from prettytable import PrettyTable
# check if python v2 or v3, we want v3
if sys.version_info[0] == 2:
	reload(sys)
	sys.setdefaultencoding('utf8')

# define output table
table = PrettyTable(['Type', 'Line', 'Line Number', 'Commit'])

# creating a regex match function to call from the blob loop
def check_for_creds(line, linenumber, commit): #, committosearch):

	# could probably build these from a file similar to here:
	# http://stackoverflow.com/questions/3199171/append-multiple-values-for-one-key-in-python-dictionary
	ConnStringRE = [
	re.compile('(g0tmi1k)'),
	re.compile('(AlpheusDigital1010)')
	]

	ConfRE = [
	]

	KeyRE = [
	]

	SecretsRE = [
	]

	DefaultCredRE = [
	]

	DomainPassRE = [
	]


	for regex in ConnStringRE:
		if regex.search(line):
			table.add_row(['Connection String', line, linenumber, commit])
			




def search_git(git_url):
	# TODO check if branch is already cloned to avoid unnessecary duplication
	project_path = tempfile.mkdtemp() # make temp directory as securely as possible
	Repo.clone_from(git_url, project_path) 
	repo = Repo(project_path)


	already_searched = set()


	# fetch all the branch names and attempt to checkout
	for remote_branch in repo.remotes.origin.fetch():
		branch_name = str(remote_branch).split('/')[1] #remove origin/
		try:
			repo.git.checkout(remote_branch, b=branch_name)
		except:
			pass

		prev_commit = None
		
		for curr_commit in repo.iter_commits():
			if not prev_commit:
				pass
			else:
				# try not to search the same diffs
				hashes = str(prev_commit) + str(curr_commit)
				if hashes in already_searched:
					prev_commit = curr_commit
					continue
				already_searched.add(hashes)

				diff = prev_commit.diff(curr_commit, create_patch=True)
				for blob in diff:
					printableDiff = blob.diff.decode()
					if printableDiff.startswith("Binary files"):
						continue
					
					# this is mainly where the differences to trufflehog is
					# should search for the regex within each line of the git history

					lines = blob.diff.decode().split("\n")
					linenumber = 0
					for line in lines:
						linenumber += 1
						try:
							#want to add line number and commit has to the function call
							check_for_creds(line, linenumber, curr_commit)
						except:
							pass
			prev_commit = curr_commit
		#print the table after it has gone through all commits
		print(table)
	return project_path



if __name__ == "__main__":
	# TODO throw into argaprse function
	parser = argparse.ArgumentParser(description='Find known secrets in git history.')
	parser.add_argument('git_url', type=str, help='Git URL to search')
	args = parser.parse_args()
	print("Running the scan on: " + str(args.git_url))
	try:
		search_git(args.git_url)
	except (KeyboardInterrupt, SystemExit):
		raise
