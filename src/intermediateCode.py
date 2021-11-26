class IntermediateCode:

    labelCounter = 0
    variableCounter = 0

    def __init__(self, commands):
        self.commands = commands

    def parseCommand(self, command):
        if type(command) is not tuple:
            return command

        order = command[0]

        if order == "print":
            inner_command = self.parseCommand(command[1])
            self.out_code.write('print ({}) \n'.format(inner_command))

        elif order == "declare":
            dataType = command[1]
            id = command[2]
            self.out_code.write('{}dec ({}) \n'.format(dataType, id))

        elif order == "declare_assign":
            dataType = command[1]
            id = command[2]
            self.out_code.write('{}dec ({}) \n'.format(dataType, id))
            inner_command = self.parseCommand(command[3])
            self.out_code.write('{} := {} \n'.format(id, inner_command))

        elif order == "assign":
            id = command[1]
            inner_command = self.parseCommand(command[2])
            self.out_code.write('{} := {} \n'.format(id, inner_command))

        elif order == "operation":
            left_command = self.parseCommand(command[1])
            logic_operator = command[2]
            right_command = self.parseCommand(command[3])
            tmp_variable = self.nextTmpVariable()

            self.out_code.write('{} = {} {} {} \n'.format(tmp_variable, left_command, logic_operator, right_command))

            return tmp_variable

        elif order == "condition":
            if_command = command[1]
            else_if_command_list = command[2]
            else_command = command[3]

            logic = self.parseCommand(if_command[1])
            current_label = self.nextLabel()
            goto_label = self.nextLabel()
            instructions = if_command[2]
            self.out_code.write('if !{} goto {}\n'.format(logic, current_label))

            for instruction in instructions:
                self.parseCommand(instruction)
            self.out_code.write('goto {}\n'.format(goto_label))
            self.out_code.write('{}\n'.format(current_label))

            for else_if_command in else_if_command_list:
                logic = self.parseCommand(else_if_command[1])
                instructions = else_if_command[2]
                current_label = self.nextLabel()

                self.out_code.write('if !{} goto {}\n'.format(logic, current_label))

                for instruction in instructions:
                    self.parseCommand(instruction)

                self.out_code.write('goto {}\n'.format(goto_label))
                self.out_code.write('{}\n'.format(current_label))

            if else_command:
                instructions = else_command[1]

                for instruction in instructions:
                    self.parseCommand(instruction)

            self.out_code.write('{}\n'.format(goto_label))

        elif order == "for":
            self.parseCommand(command[1])
            nested_instructions = command[4]

            current_label = self.nextLabel()
            goto_label = self.nextLabel()

            self.out_code.write('{}\n'.format(current_label))

            logic = self.parseCommand(command[2])
            self.out_code.write('if !{} goto {}\n'.format(logic, goto_label))

            for instruction in nested_instructions:
                self.parseCommand(instruction)

            self.out_code.write('goto {}\n'.format(current_label))
            self.out_code.write('{}\n'.format(goto_label))

        elif order == "while":
            instructions = command[2]
            current_label = self.nextLabel()
            goto_label = self.nextLabel()
            logic = self.parseCommand(command[1])

            self.out_code.write('{}\n'.format(current_label))
            self.out_code.write('if !{} goto {}\n'.format(logic, goto_label))

            for instruction in instructions:
                self.parseCommand(instruction)

            self.out_code.write('goto {}\n'.format(current_label))
            self.out_code.write('{}\n'.format(goto_label))

        elif order == "do-while":
            instructions = command[2]
            current_label = self.nextLabel()

            self.out_code.write('goto {}\n'.format(current_label))

            for instruction in instructions:
                self.parseCommand(instruction)

            logic = self.parseCommand(command[1])
            self.out_code.write('if !{} goto {}\n'.format(logic, current_label))

        else:
            self.out_code.write('>>>>>>ERROR: Invalid Command: {}<<<<<<\n'.format(order))


    def nextLabel(self):
        self.labelCounter += 1
        return "L" + str(self.labelCounter)


    def nextTmpVariable(self):
        self.variableCounter += 1
        return "t" + str(self.variableCounter)

    
    def write(self, file_path:str = "output.txt"):
        self.out_code = open(file_path, "w")
        for command in self.commands:
            self.parseCommand(command)
        self.out_code.close()