#
# File: git.py
# Methods for common Git operations
#
# Author:
#    Adam Presley
#
# History:
#    * 2013-05-02 - Created
#
import subprocess
import os

###############################################################################
# Section: Public methods
###############################################################################
def getFilesByRevision(revision, returnStatus=False):
	if returnStatus:
		result = []
		response = _splitLines(_doGitCommand("diff-tree", ["--name-status", "-r", revision]))

		for line in response:
			status = line[0]
			fileName = line[1:].strip()

			result.append((status, fileName))

	else:
		result = _splitLines(_doGitCommand("diff-tree", ["--name-only", "-r", revision]))

	return result

def getHeadCommitRevisionHash():
	args = ["-1", "--format=\"%H\""]
	result = _doGitCommand("log", args).strip()

	return result

def getRevisionsAfterDate(date, reverse=False):
	result = []
	args = ["--after=%s" % (date,), "--pretty=format:%H", "--name-status"]

	if reverse:
		args.append("--reverse")
		
	response = _doGitCommand("log", args).split("\n\n")
	
	for block in response:
		lines = block.strip().split("\n")

		if len(lines) > 1:
			item = {
				"revision": lines[0].strip(),
				"files": []
			}

			for i in range(len(lines) - 1):
				line = lines[i + 1]
				status = line[0]
				fileName = line[1:].strip()

				item["files"].append((status, fileName))

			result.append(item)

	return result

def getRevisionByTicketNumber(ticketNumber):
	return _splitLines(_doGitCommand("log", ["--grep=\"#%s\"" % (ticketNumber,), "--pretty=format:%H"]))


###############################################################################
# Section: Private methods
###############################################################################

def _doGitCommand(command, arguments=[]):
	cmd = "git %s " % command

	if len(arguments):
		cmd += " ".join(arguments)

	process = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
	result = process.communicate()[0]
	return result.strip()

def _splitLines(input):
	return input.split("\n")
