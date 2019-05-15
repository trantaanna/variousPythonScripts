import csv
import os

SOURCE_FILE = r"..\hashScoreFiles\dukowski_scores.csv"
RESULT_FILE = "..\hashScoreFiles\PE_Flexo-Dukowski_HashScores.dat"


def delete_column_from_csv_file(sourcePath, resultPath):
    """
    This function drop a column from csv file
    """
    if os.path.exists(sourcePath):
        with open(sourcePath, "r") as source:
            rdr= csv.reader(source)
            with open(resultPath, "w", newline='') as result:
                wtr= csv.writer(result)
                for r in rdr:
                    wtr.writerow((r[0], r[2]))

if __name__== "__main__":
    delete_column_from_csv_file(SOURCE_FILE, RESULT_FILE)
