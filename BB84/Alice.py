#
# Alice.py
#
#	Example for Quantum Key Distribution using the BB84 protocol. Communicates
#	with Bob.py and Eve.py.
#
# Author: Nico Daßler <dassler@hm.edu>

#
# Copyright (c) 2017, Stephanie Wehner and Axel Dahlberg
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the distribution.
# 3. All advertising materials mentioning features or use of this software
#    must display the following acknowledgement:
#    This product includes software developed by Stephanie Wehner, QuTech.
# 4. Neither the name of the QuTech organization nor the
#    names of its contributors may be used to endorse or promote products
#    derived from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDER ''AS IS'' AND ANY
# EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER BE LIABLE FOR ANY
# DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
# ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

from SimulaQron.cqc.pythonLib.cqc import *
import random
import time

import ClassicConnection

# This will take a part of the key (one third) and do a statistical analysis
# to check if eve tried to listen in.
def verifyKeyWithBob(cqcConnection, key):

	# number of elements to analyze (integer division)
	numberOfBitsToCheck = len(key) // 3

	# these bits (given by index) are already checked
	alreadyChecked = list()

	for counter in range(0, numberOfBitsToCheck):
		# keep trying indices until one was found which has not been checked
		index = random.randint(0, len(key) - 1)
		while (index in alreadyCheck):
			index = random.randint(0, len(key) - 1)


# takes cqcConnection and returns key as array. Alice will be the initiator
# of the whole process.
def createKey(cqcConnection, serverSocket, keyLength):
	# counts the key bits that have been established
	keyCounter = 0

	# stores the key bits
	keyBits = list()

	# keep going until we have the desired key length
	while keyCounter < keyLength:

		# send Eve if we are finished (0 not finished; 1 finished) (status)
		# this is how we simulate an interception
		ClassicConnection.sendIntToLocalhost(0, ClassicConnection.evePort)

		# Create a qubit
		qubitToSend = qubit(cqcConnection, print_info=False)

		# prepare qubit
		# randomly generate if not should be applied
		notOperation = random.randint(0, 1)
		# randomly generate if hadamard should be applied
		hadamardOperation = random.randint(0,1)

		# apply operations
		if notOperation:
			qubitToSend.X(print_info=False)
		if hadamardOperation:
			qubitToSend.H(print_info=False)

		# dont forget to send the qubit to Bob
		# this is how we simulate the interception
		cqcConnection.sendQubit(qubitToSend, "Eve", print_info=False)


		# now wait until bob sends the basis he used (0 for normal; 1 for hadamard)
		bobBasis = ClassicConnection.receiveInt(serverSocket)

		# if they used the same basis everything is alright and we got our first bit
		if (bobBasis == hadamardOperation):
			# loop condition and save to key
			keyCounter += 1
			keyBits.append(notOperation)

		# doesn't matter if bob used the right basis we have to tell him
		# which one we used
		ClassicConnection.sendIntToLocalhost(hadamardOperation, ClassicConnection.bobPort)

	# key bits should have keyLength length now

	# we can now tell bob that the key transmission is finished
	# this is how we simulate the interception
	ClassicConnection.sendIntToLocalhost(1, ClassicConnection.evePort)

	return keyBits

print("")
print("Results:")
print("#########################")
# Initialize the connection
Alice=CQCConnection("Alice")

# initialize sockets
aliceServer = ClassicConnection.createLocalhostServerSocket(ClassicConnection.alicePort)

time.sleep(3)

key = createKey(Alice, aliceServer, 10)

print("Key found by Alice: {}".format(key))

# Stop the connections
Alice.close()

ClassicConnection.closeSocket(aliceServer)
