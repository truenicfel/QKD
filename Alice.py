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

import Utility

# Sends 100 qubits to Bob and returns the used basis. The format
# of the result is a list containing 1s and 0s for hadamard basis
# and normal basis. It also returns the key bits.
def send100Qubits(cqcConnection):

	basisUsed = list()
	keyBits = list()

	for run in range(0, 10):
		# Create a qubit
		qubitToSend=qubit(cqcConnection)

		# randomly generate if not should be applied
		notOperation = random.randint(0, 1)
		# randomly generate if hadamard should be applied
		hadamardOperation = random.randint(0,1)

		# apply operations
		if notOperation:
			qubitToSend.X()
		if hadamardOperation:
			qubitToSend.H()

		# append hadamard basis used
		basisUsed.append(hadamardOperation)

		# append key bit (it is given by the notOperation: if not operation was
		# applied to the qubit the bit which will be send is 1)
		keyBits.append(notOperation)

		# Send qubit to Bob
		cqcConnection.sendQubit(qubitToSend, "Bob")

	return (basisUsed, keyBits)

# Initialize the connection
Alice=CQCConnection("Alice")

results = send100Qubits(Alice)

# send actually used basises to bob
Alice.sendClassical("Bob", results[0])

# receive basises used from bob
bobBasis = Alice.recvClassical()

# filter key
key = Utility.filterKey(results[0], bobBasis, results[1])

print("Key found by Alice: {}".format(key))

# Stop the connections
Alice.close()
