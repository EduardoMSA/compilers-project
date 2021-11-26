from src.parser import Parser
from src.intermediateCode import IntermediateCode

analysis = Parser()
analysis.parse()
IntermediateCode(analysis.commands).write()