#
# Bob.py
#
#	Example for Quantum Key Distribution using the BB84 protocol. Communicates
#	with Alice.py and Eve.py.
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

# takes cqcConnection and returns key as array. This has to wait for Alice
# to start the process.
def receiveToCreateKey(cqcConnection):
	# stores the key bits
	keyBits = list()

	# receive first status information from alice (0 not finished; 1 finished)
	status = int.from_bytes(cqcConnection.recvClassical(timout=10, msg_size=1),  byteorder='little')

	# keep going until alice says we are done
	while status == 0:

		# alice should now send us a qubit that she prepared to contain a key bit
		receivedQubit = cqcConnection.recvQubit()

		# decide if measurement should happen in hadamard basis
		hadamardBasis = random.randint(0,1)

		# apply operation
		if hadamardBasis:
			receivedQubit.H()

		# measure to obtain classical bit
		potentialKeyBit = receivedQubit.measure()

		# send the basis we used to Alice
		cqcConnection.sendClassical("Alice", hadamardBasis)

		# now wait until alice sends the basis she actually used
		# (0 for normal; 1 for hadamard)
		aliceBasis = int.from_bytes(cqcConnection.recvClassical(timout=10, msg_size=1),  byteorder='little')

		# if they used the same basis everything is alright and we got our first bit
		if (aliceBasis == hadamardBasis):
			# append to keyBits
			keyBits.append(potentialKeyBit)

		# get status info if we should continue
		status = int.from_bytes(cqcConnection.recvClassical(timout=10, msg_size=1),  byteorder='little')

	# key bits should all be received

	return keyBits

# Initialize the connection
Bob=CQCConnection("Bob")
Bob.startClassicalServer()

key = receiveToCreateKey(Bob)

# print Key
print("Key found by Bob: {}".format(key))

# Stop the connection
Bob.closeClassicalServer()
Bob.close()
