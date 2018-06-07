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

import Utility

# Receives a single Qubit and randomly decides in which basis to measure
def receiveQubit(cqcConnection, hadamardBasis):

	# Receive qubit from Alice (via Eve)
	qubit=cqcConnection.recvQubit()

	# apply hadamard if we want to measure in hadamardBasis
	if hadamardBasis:
		qubit.H()

	# measure in standard basis
	message = qubit.measure()

	return message

# Receive 100 qubits. The first results element is the basis' that were used in
# list containing 0s (normal basis) and 1s (hadamard basis). The other result is
# the actual result of the measurements.
def receive100Qubits(cqcConnection):

	# stores the results of measurements
	measurements = list()

	# stores the basis' used
	basisUsed = list()

	# receive 100 times
	for run in range(0, 10):

		# decide in which basis to measure
		hadamardBasis = random.randint(0, 1)

		# append used basis
		basisUsed.append(hadamardBasis)

		# add to measurements list
		measurements.append(receiveQubit(cqcConnection, hadamardBasis))

	return (basisUsed, measurements)


# Initialize the connection
Bob=CQCConnection("Bob")

# start a classical server
Bob.startClassicalServer()

# now receive the 100 qubits
results = receive100Qubits(Bob);

# send the basises used to alice
Bob.sendClassical("Alice", results[0])

# receive basises used from alice
aliceBasis = Bob.recvClassical()

key = Utility.filterKey(aliceBasis, results[0], results[1])

# print Key
print("Key found by Bob: {}".format(key))

# Stop the connection
Bob.close()
