#
# Eve.py
#
#	Example for Quantum Key Distribution using the BB84 protocol. Communicates
#	with Bob.py and Alice.py. Eve just simulates an eavesdropper not an actual
#   attacker. The way she tries to steal only helps us to see how Alice and Bob
#   can later detect the eavesdropper.
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

# this will intercept a key and the status messages. Then perform operations
# on the qubit and send status unchanged to bob and the hopefully unchanged
# qubit to Bob. Returns the key bits.
def interceptKey(cqcConnection, serverSocket):
    # stores the key bits
    keyBits = list()

    # receive first status information from alice (0 not finished; 1 finished)
    # we simulate the interception by alice sending the qubit to us instead of bob
    status = ClassicConnection.receiveInt(serverSocket)

    # forward status to Bob
    ClassicConnection.sendIntToLocalhost(status, ClassicConnection.bobPort)

    # keep going until alice says we are done
    while status == 0:

        # alice should now send a qubit that she prepared to contain a key bit
        # we simulate the interception by alice sending the qubit to us instead of bob
        receivedQubit = cqcConnection.recvQubit(print_info=False)

        eavesdrop = False

        if eavesdrop:
            # to obtain the bit encoded into the qubit we have to measure
            # decide if measurement should happen in hadamard basis
            hadamardBasis = random.randint(0,1)

            # apply operation
            if hadamardBasis:
            	receivedQubit.H(print_info=False)

            # measure to obtain classical bit
            keyBit = receivedQubit.measure(print_info=False)

            # append to key bits list
            # (this is lazy usually you would also intercept the classical channel
            # to determine if we measured in the right basis and throw away the
            # wrong keybit. This way we dont even have the right key length!)
            keyBits.append(keyBit)

            # we now need to send something to bob so he does not know about the
            # interception
            # we assume that we measured right
            # create qubit
            qubitToSend = qubit(cqcConnection, print_info=False)

            # prepare as we measured
            if keyBit:
                qubitToSend.X(print_info=False)
            if hadamardBasis:
            	qubitToSend.H(print_info=False)

            # send to Bob
            cqcConnection.sendQubit(qubitToSend, "Bob", print_info=False)
        else:
            # send as received to bob
            cqcConnection.sendQubit(receivedQubit, "Bob", print_info=False)

        # get status info if we should continue
        status = ClassicConnection.receiveInt(serverSocket)

        # forward status to Bob
        ClassicConnection.sendIntToLocalhost(status, ClassicConnection.bobPort)

    # key bits should all be received

    return keyBits

# Initialize the connection
Eve = CQCConnection("Eve")

# initialize sockets
eveServer = ClassicConnection.createLocalhostServerSocket(ClassicConnection.evePort)

time.sleep(3)

key = interceptKey(Eve, eveServer)

print("Key found by Eve: {}".format(key))

# Stop the connections
Eve.close()

ClassicConnection.closeSocket(eveServer)
