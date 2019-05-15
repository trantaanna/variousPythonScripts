import subprocess
from argparse import ArgumentParser
import boto3
from boto3.session import Session
from parseFilePathJson import FilePath
import os


ACCESS_KEY = "YOUR KEY HERE"
SECRET_KEY = "SECRET KEY"

SCRIPTS_PATH = os.path.dirname(os.path.realpath(__file__))
PATHS_TO_SYNC = os.path.join(SCRIPTS_PATH, "filePaths.json")
CONFIGURE_AWS = False

def aws_configure():
    print("Configure AWS session...")
    return Session(aws_access_key_id=ACCESS_KEY,
            aws_secret_access_key=SECRET_KEY)

def invoke_aws_cli(cmd, args):
    """
    This function will invoke aws cli:
    aws s3 <Command> [<Arg> ...]
    :param cmd: STRING commands (i.e: 'cp', 'ls', 'sync'
    :param arg: STRING arguments
    :return:
    """
    try:
        aws_cmd = "aws s3 {} {}".format(cmd, args)
        print("Invoking: '{}'".format(aws_cmd))
        subprocess.check_call(aws_cmd, shell=True)
    except subprocess.CalledProcessError as e:
        print("Fail to call {} with error: {}".format(aws_cmd, e.output))




if __name__== "__main__":

    print("DEBUG: syncS3Data CurrentDirectory=" + os.getcwd())

    ###############
    # Get list of file paths
    ###############
    json_obj = FilePath.ReadJSONContent(PATHS_TO_SYNC)

    if (CONFIGURE_AWS):
        session = aws_configure()
        s3 = session.resource('s3')
    else:
        s3 = boto3.resource('s3')

    paths_collection = json_obj.GetPathsToSync()
    for paths in paths_collection:
        #print("Src={0} , Dest={1}".format(paths['src'], paths['dest']))
        arg = "{} {}".format(paths['src'], os.path.join(SCRIPTS_PATH,paths['dest']))
        invoke_aws_cli(paths['cmd'], arg)

    ###############
    # copy over required model ensemble files, samplescoring dlls
    ###############
    #parser = ArgumentParser(description="Download S3 data for test run")
    #parser.add_argument("-b", "--build", dest="engine_build",
    #                    help="engine build number to download model ensemble files")

    #args = parser.parse_args()
    #src = r"s3://cylance.engine/cylance_engine_builds/{}/dist".format(args.engine_build)
    #dest = os.path.join(SCRIPTS_PATH, r"../dist")
    #arg = "{} {}".format(src, dest)
    #invoke_aws_cli("sync", arg)

    #src = "s3://cylance.engine/cylance_engine_builds/{}/bin/Debug".format(args.engine_build)
    #dest = os.path.join(SCRIPTS_PATH, "../bin/Debug")
    #arg = "{} {}".format(src, dest)
    #invoke_aws_cli("sync", arg)


