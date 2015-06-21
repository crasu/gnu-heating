def manchester_decode(pulseStream):
    i = 1
    #while pulseStream[i] != pulseStream[i-1]:
    #    i = i + 1
    #    print str(i) + " => " + str(pulseStream[i])
    
    bits = ''
    
    # here pulseStream[i] is "guaranteed" to be the beginning of a bit
    while i < len(pulseStream):
        if pulseStream[i] == pulseStream[i-1]:
            # if so, sync has slipped
            # try to resync
            print "<slip: " + str(i) + "> in " + pulseStream
            i = i - 1
        if pulseStream[i] == '1':
            bits += '1'
        else:
            bits += '0'
        i = i + 2
        
    return bits
