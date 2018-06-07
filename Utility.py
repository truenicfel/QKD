# takes alices basises and bobs basises and returns the valid bits that can
# be used for the key
def filterKey(aliceBasis, bobBasis, measurements):
    key = list()
    for index in range(0, len(measurements)):
        # append if same basis was used
        if aliceBasis[index] == bobBasis[index]:
            key.append(measurements[index])
    return key
