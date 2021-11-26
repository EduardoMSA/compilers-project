import sys

from src.parser import Parser
from src.intermediateCode import IntermediateCode

if __name__ == "__main__":

    analysis = Parser()

    if len(sys.argv) >= 3:
        try:
            analysis.parse(sys.argv[1])
        except FileNotFoundError:
            print('File {} does not exists'.format(sys.argv[1]))
        try:
            IntermediateCode(analysis.commands).write(sys.argv[2])
        except FileNotFoundError:
            print('Path {} not valid'.format(sys.argv[2]))
    elif len(sys.argv) == 2:
        try:
            analysis.parse(sys.argv[1])
        except FileNotFoundError:
            print('File {} does not exists'.format(sys.argv[1]))
        IntermediateCode(analysis.commands).write()
    else:
        analysis.parse()
        IntermediateCode(analysis.commands).write()