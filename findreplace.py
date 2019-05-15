

SOURCE_FILE = r"..\hashScoreFiles\PE_Flexo-Dukowski_HashScores.dat"
RESULT_FILE = "..\hashScoreFiles\PE_Flexo-Dukowski_HashScores.dat"

def find_text_replace(src, dest):
    """
    This function replace delimiter comma ',' with colon ':'
    :param src:
    :param dest:
    :return:
    """
    #Read file
    with open(src, 'r') as file:
        filedata = file.read()

    #Replace target text
    filedata = filedata.replace(',', ':')

    #write to output
    with open(dest, 'w', newline='') as file:
        file.write(filedata)


if __name__== "__main__":
    find_text_replace(SOURCE_FILE, RESULT_FILE)
