def deepdump(info, indent, resolver):
    output = ""
    for key in info:
        val = info[key]
        if(type(val) is dict):
            output += (indent + '* ' + key + "\n")
            output += deepdump(val, "  " + indent, resolver)
        else:
            if(val and key == 'Name'):
                output += (indent + "[" + str(val) + "]\n")
            elif(val and key != 'Id' and key != 'Uri'):
                output += (indent + key + ": " + str(val) + "\n")
            if(val and key == 'Uri' and resolver(val)):
                output += (indent + "+ " + resolver(val) + "\n")
    return output

def animal(animal, resolver):
    return deepdump(animal, "", resolver)
