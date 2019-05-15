import json
import os


SCRIPTS_PATH = os.path.dirname(os.path.realpath(__file__))
FILE_PATH = os.path.join(SCRIPTS_PATH, "filePaths.json")


class FilePath(object):
    @staticmethod
    def ReadJSONContent(file):
        with open(file, 'r') as jsonContent:
            jsonStr = jsonContent.read()
            return FilePath(jsonStr)

    def __init__(self, jsonStr):
        self.filePath = json.loads(jsonStr)

    def HasAuthKey(self):
        return 'AuthKey' in self.filePath and self.filePath['AuthKey']

    def GetAuthKey(self):
        if not self.HasAuthKey():
            return None
        return self.filePath['AuthKey']

    def HasAuthPwd(self):
        return 'AuthPwd' in self.filePath and self.filePath['AuthPwd']

    def GetAuthPwd(self):
        if not self.HasAuthKey():
            return None
        return self.filePath['AuthPwd']

    def IsPathsToSync(self):
        return 'PathsToSync' in self.filePath

    def GetPathsToSync(self):
        #return self.filePath['PathsToSync'] if 'PathsToSync' in self.filePath else None
        return self.filePath['PathsToSync'] if self.IsPathsToSync() else None

    def PathsCount(self):
        paths = self.GetPathsToSync()
        return len(paths) if paths else 0

if __name__== "__main__":
    json_obj = FilePath.ReadJSONContent(FILE_PATH)
    print('Key: ' + json_obj.GetAuthKey())
    print('Pwd: ' + json_obj.GetAuthPwd())
    paths = json_obj.GetPathsToSync()
    for path in paths:
        print("{0} {1}".format(path['src'], path['dest']))
    print("to be implemented")
