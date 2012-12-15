"""Batch CLI provide a simple API to manage batch process CLI.
The API can be used when one or more tasks need to be executed
providing output messages to the user. 
It is also possible to request input to the user.

Author: siasi@cisco.com
Date: December 2013
"""

class Cli():

    def __init__(self):
        pass

    def log(self, message):
        pass

    def ask(self, message):
        pass

class BatchCli():
    """This class provides a simple API to ask input to the user and 
       track the progress of tasks execution sending message to a cli.

       User create an instance of this class specifying the number of total
       tasks that must be executed and the cli to which the output shall be
       sent.

       The progress of execution of tasks is tracked with progressive numbers
       in the form of current / total where the current value is the sequence 
       number of the current task, and the total number is the total number of tasks.
       The current value is automatically determined when the method newMessage is called.
       """

    def __init__(self, tasksCount, cli):
        self.startMarker = '['
        self.endMarker = ']'
        self.cli = cli
        self.tasksCount = tasksCount
        self.currentTask = 0
        self.__buildHeaderTokens()

    def newMessage(self, message):
        "Send a new message to the cli."

        output = self.__buildMessageOutput(message)
        self.cli.log(output)

    def newTask(self, taskName):
        """Send to the cli a message saying the task passed as 
        parameter is starting execution."""

        if self.currentTask == self.tasksCount:
            raise RuntimeError("No more tasks expected")

        self.currentTask += 1
        output = self.__buildTaskOutput(taskName)
        self.cli.log(output)

    def confirm(self, question):
        answer = self.ask(question, ['Y', 'N'], 'Y')
        return answer.upper() == 'Y' or answer == ""

    def negate(self, question, suggest=['Y','N'], default=['N']):
        answer = self.ask(question, ['Y', 'N'], 'N')
        return answer.upper() == 'N' or answer == ""

    
    def ask(self, question, suggest=[], default=None):
        "Ask a question to the user and return the answer."
        
        if suggest and not default:
            raise RuntimeError("Cannot call ask with suggest and no default")

        if not suggest:
            output = self.__buildQuestionOutput(question)
            return self.cli.ask(output)

        if suggest and default:
            options_str = self.__getOptionsString(suggest, default)

            while True:
                #answer = raw_input(question + " (Y/N) [Y]").strip()
                answer = self.__getAnswer(question, options_str)

                validAnswers = [option.lower() for option in suggest]
                validAnswers.extend(suggest)

                if answer in validAnswers:
                    return answer
                elif answer == "":
                    return default

    def __getOptionsString(self, options, default):
            result = []
            result.append("(")
            result.append("|".join(options))
            result.append(") [")
            result.append(default)
            result.append("]")
            return "".join(result)

    def __getAnswer(self, question, options):
        output = self.__buildQuestionOutput(question, options)
        return self.cli.ask(output).strip()

    def __buildQuestionOutput(self, message, options=""):
        self.tokens[1] = " ? "
        self.tokens[3] = message
        if options != "":
            self.tokens.append(options)
        return " ".join(self.tokens)

    def __buildTaskOutput(self, message):
        self.tokens[1] = self.__getProgressIndex()
        self.tokens[3] = message
        return " ".join(self.tokens)

    def __buildMessageOutput(self, message):
        self.tokens[1] = "..."
        self.tokens[3] = message
        return " ".join(self.tokens)

    def __buildHeaderTokens(self):
        self.tokens = []
        self.tokens.append(self.startMarker)
        self.tokens.append("")
        self.tokens.append(self.endMarker)
        self.tokens.append("")
        
    def __getProgressIndex(self):
        return str(self.currentTask) + "/" + str(self.tasksCount)

class Task():

    def __init__(self, name):
        self.name = name

    def run(self, cli):
        pass

class TaskEngine():

    def __init__(self, cli):
        self.tasks = []
        self.cli = cli

    def addTask(self, task):
        self.tasks.append(task)

    def run(self):
        for task in self.tasks:
            self.cli.newTask(task.name)
            task.run(self.cli)




