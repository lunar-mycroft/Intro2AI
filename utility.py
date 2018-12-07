def getOpts(argv):
    opts={}
    lastKey='nokey'
    opts[lastKey]=[]

    while argv:
        if argv[0][0]=='-':
            lastKey=argv[0]
            opts[lastKey]=[]
        else:
            try:
                opts[lastKey].append(argv[0])
            except:
                break
        argv=argv[1:]

    return opts