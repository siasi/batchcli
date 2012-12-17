"""Batch CLI provide a simple API to manage batch process CLI.
The API can be used when one or more tasks need to be executed
providing output messages to the user. 
It is also possible to request input to the user.

Author: siasi@cisco.com
Date: December 2013
"""

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

    def __init__(self, cli):
        self.startMarker = '['
        self.endMarker = ']'
        self.cli = cli
        self.tasksCount = 0
        self.currentTask = 0
        self.__buildHeaderTokens()

    def expectTaskCount(self, tasksCount):
        self.tasksCount = tasksCount

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

class Cli():
    "The CLI expected by BatchCli."

    def log(self, message):
        "Print the message to the CLI"
        print message

    def ask(self, message):
        "Print the message to the CLI and read and return the input of the CLI."
        return raw_input(message)


class Task():
    "A task executed by the Task Engine"

    def __init__(self, name):
        self.name = name
        self.failed = False

    def run(self, cli):
        pass

    def __key(self):
        return self.name

    def __eq__(x, y):
        if type(x) != type(y):
            return False

        return x.__key() == y.__key()

    def __hash__(self):
        return hash(self.__key())  

    def __repr__(self):
        return self.name

class TaskEngine():
    """The task engine able to run multiple Tasks in sequence.
    Stop immediately when a task fails.
    """

    def __init__(self, batchCli):
        "Needs a BatchCli to read/print input and output before runnign the tasks"
        
        self.tasks = []
        self.cli = batchCli

    def addTask(self, task):
        "Add a task to be run. The method should be invocked before run()."
        self.tasks.append(task)

    def run(self):
        """Run all the tasks added by invocking the add method.
        Stop immediately if a task fails.
        """

        self.cli.expectTaskCount(self.taskToRun())
        for task in self.tasks:
            self.cli.newTask(task.name)
            task.run(self.cli)
            if task.failed:
                return

    def taskToRun(self):
        "Return the number of tasks to run."
        return len(self.tasks)

class SimpleCli():
    """A simple implementation of the CLI expected by BatchCli.
    Print and read from Standard Input and Standard Output.
    """

    def log(self, message):
        "Print the message to Standard Ouput"
        print message

    def ask(self, message):
        "Print the message to Standard Ouput and read the input from Standard Input."
        return raw_input(message)




if __name__ == "__main__":

    class Print(Task):
        "Simple Task: do nothing more than printing ..."

        def run(self, cli):
            cli.newMessage("...")

    cli = SimpleCli()
    bcli = BatchCli(cli)
    engine = TaskEngine(bcli)
    engine.addTask(Print("Put oil in the pan"))
    engine.addTask(Print("Turn fire on"))
    engine.addTask(Print("Break the egg"))
    engine.addTask(Print("Put the egg in the pan"))
    engine.addTask(Print("Wait the egg is cooked"))
    engine.addTask(Print("Put the egg in the dish"))
    engine.addTask(Print("Add salt to the egg and eat it!"))
    engine.run()



