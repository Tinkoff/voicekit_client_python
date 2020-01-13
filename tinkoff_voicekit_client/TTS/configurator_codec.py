import os
import sys

path_to_opus_lib = os.path.join(sys.exec_prefix, "opuslibwin")


def configuration():
    if os.name == "nt" and path_to_opus_lib not in os.environ["PATH"]:
        os.environ["PATH"] += os.pathsep + path_to_opus_lib
