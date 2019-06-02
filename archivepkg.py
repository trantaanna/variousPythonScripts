import os
import errno
from shutil import copytree, ignore_patterns, copy, rmtree, make_archive
from pathlib import Path
import subprocess
import logging
import zipfile

WORKING_DIR = r'C:\Dirty\cylance-engine'
#WORKING_DIR = os.environ['WORKSPACE']
BUILD_Path = os.path.join(WORKING_DIR, 'build')
DIST_Path = os.path.join(WORKING_DIR, 'dist')

IGNORE_PATTERNS = '*.pdb'

SV2F = r"Tools/SampleVectorsToFilesApp/SampleVectorsToFilesApp.csproj"
SSA = r"Tools/SampleScoringApp/SampleScoringApp.csproj"
CA = r"Tools/CentroidApp/CentroidApp.csproj"
SS3EB = r"SampleScoring3/SS3EnsembleBuilder/SS3EnsembleBuilder.csproj"
MDST = r"Tools/ModelDeliverySmokeTester/ModelDeliverySmokeTester.csproj"
DAA = r"Tools/DiscrepancyAnalyzerApp/DiscrepancyAnalyzerApp.csproj"
EB = r"SampleScoring/EnsembleBuilder/EnsembleBuilder.csproj"
UFO = r"Tools/UnusedFeaturesObserver/UnusedFeaturesObserver.csproj"
ET = r"Tools/EnsembleTool/EnsembleTool.csproj"

path_to_tool_csproj = {
    'CentroidApp': CA,
    'DiscrepancyAnalyzerApp': DAA,
    'EnsembleBuilder': EB,
    'EnsembleTool': ET,
    'SampleScoringApp': SSA,
    'SampleVectorsToFiles': SV2F,
    'SmokeTester': MDST,
    'SS3EnsembleBuilder': SS3EB,
    'UnusedFeaturesObserver' : UFO,
    }

# Function return full path to tool package
# Switcher is dictionary data type here
def get_path_to_tool_csproj(tool):
    return path_to_tool_csproj.get(tool, 'SS3EB')


def copy_build_to_staging_location(tool):
    logging.info("INFO: Start copying build to staging location...")

    if not os.path.exists(BUILD_Path):
        logging.info("INFO: Create folder {}".format(BUILD_Path))
        os.mkdir(BUILD_Path)
    else:
        logging.info('DEBUG: Directory already exist')

    #copy from net462 (i.e: cylance-engine\Tools\EnsembleTool\bin\Release\net462\)
    logging.info("DEBUG: os.path.dirname(get_path_to_tool_csproj): {}".format(os.path.dirname(get_path_to_tool_csproj(tool))))
    source = os.path.join(WORKING_DIR, os.path.dirname(get_path_to_tool_csproj(tool)), 'bin', 'Release', 'net462')
    destination = os.path.join(BUILD_Path, 'net462')
    if os.path.exists(destination):
        rmtree(destination)
    try:
        logging.info("INFO: Start copying from net462 folder ...")
        copytree(source, destination,  ignore=ignore_patterns(IGNORE_PATTERNS))
    except OSError as e:
        if e.errno == errno.ENOTDIR:
            copy(source, destination)
        else:
            logging.info('DEBUG: Directory not copied. Error: %s' % e)

    # copy from netcoreapp2.1\publish (i.e: cylance-engine\Tools\EnsembleTool\bin\Release\netcoreapp2.1\publish)
    source = os.path.join(os.getcwd(), os.path.dirname(get_path_to_tool_csproj(tool)), 'bin', 'Release', 'netcoreapp2.1', 'publish')
    destination = os.path.join(BUILD_Path, 'netcoreapp2.1')
    if os.path.exists(destination):
        rmtree(destination)
    try:
        logging.info("INFO: Start copying from netcoreapp2.1 folder ...")
        copytree(source, destination, ignore=ignore_patterns(IGNORE_PATTERNS))
    except OSError as e:
        if e.errno == errno.ENOTDIR:
            copy(source, destination)
        else:
            logging.info('DEBUG: Directory not copied. Error: %s' % e)


def create_zip_pkg(tool, ver):
    target = os.path.join(DIST_Path, "{0}-{1}".format(tool, ver))
    source = BUILD_Path #os.path.join(BUILD_Path, r"/")
    make_archive(target, 'zip', source)

    #zf = zipfile.ZipFile(target, "w")
    #for dirname, subdirs, files in os.walk(source):
        #zf.write(dirname)
    #    for filename in files:
    #        zf.write(os.path.join(dirname, filename))
    #zf.close()

def create_zip_pkg_using7z(tool, ver):

    loc_7z = r"7z.exe"
    target = os.path.join(DIST_Path, "{0}-{1}.zip".format(tool, ver))
    source = os.path.join(BUILD_Path, r"*.*")
    logging.info("INFO: Packaging content of " + source)

    # If this directory does not exist, it will need to be created
    if not os.path.exists(DIST_Path):
        os.makedirs(DIST_Path)

    # Now use the subprocess command to run 7zip. Warning- all paths should be
    # enclosed in quotation marks just in case there are any spaces in the path
    # The "a" command given to 7z.exe means "add to archive"
    # the "r" mean to recursively adding all folder's content
    archive_command = r'"{}" a -r "{}" "{}"'.format(loc_7z, target, source)
    logging.info("INFO: Start zipping package using cmd: {}".format(archive_command))
    subprocess.call(archive_command, shell=True)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    # Set working directory
    os.chdir(WORKING_DIR)
    logging.info("INFO: Current working directory {}".format(os.getcwd()))

    #tool = os.environ['TOOL_NAME']
    #version = os.environ['VERSION']
    tool = 'CentroidApp'
    version = '11'

    logging.info("INFO: Start script to publish tool: {} version {}".format(tool, version))
    copy_build_to_staging_location(tool)
    create_zip_pkg(tool, version)
