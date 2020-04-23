import os

path_to_opus_lib = os.path.join(os.path.dirname(os.path.abspath(__file__)), "opuslibwin")


def configuration():
    if os.name == "nt" and path_to_opus_lib not in os.environ["PATH"]:
        os.environ["PATH"] += os.pathsep + path_to_opus_lib
