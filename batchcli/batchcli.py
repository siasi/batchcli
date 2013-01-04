"""Batch CLI provide a simple API to manage batch process CLI.
The API can be used when one or more tasks need to be executed
providing output messages to the user. 
It is also possible to request input to the user.

Author: siasi@cisco.com
Date: December 2013
"""

class TaskEngine():
    """The Task Engine is able to run multiple Tasks in sequence.
    Stop immediately when a task fails. Uses a BatchCli to collect input
    and provide output for each Task.
    """

    def __init__(self, cli):
        "Needs a BatchCli to read/print input and output before runnign the tasks"
        
        self.tasks = []
        self.cli = BatchCli(cli)

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


class Task():
    "A task executed by the Task Engine"

    def __init__(self, name):
        self.name = name
        self.failed = False

    def run(self, cli):
        "Perform the work of this task."
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
        "Set the number of tasks the BatchCli is expected to run."
        self.tasksCount = tasksCount

    def newMessage(self, message):
        "Send a new message to the cli."

        output = self.__buildMessageOutput(message)
        self.cli.log(output)

    def newTask(self, taskName):
        """Send to the CLI a message saying the task passed as 
        parameter is starting execution."""

        if self.currentTask == self.tasksCount:
            raise RuntimeError("No more tasks expected")

        self.currentTask += 1
        output = self.__buildTaskOutput(taskName)
        self.cli.log(output)

    def confirm(self, question):
        """Send the question to the CLI and wait for an answer.
        Return True if the answer is Y or y.
        """

        answer = self.ask(question, ['Y', 'N'], 'Y')
        return answer.upper() == 'Y' or answer == ""

    def negate(self, question, suggest=['Y','N'], default=['N']):
        """Send the question to the CLI and wait for an answer.
        Return True if the answer is N or n.
        """
        answer = self.ask(question, ['Y', 'N'], 'N')
        return answer.upper() == 'N' or answer == ""

    
    def ask(self, question, options=[], default=None):
        """Ask a question to the CLI and return the answer.
        Caller can specify a list of options for the answer and 
        the default answer. The default answer is returned if the CLI
        receives a carriage return character.

        If options are provided the answer must match one of the option
        otherwise it is not accepted and a new request is doen by the CLI.

        If options are provided by default is not raises a RuntimeError.
        """
        if options and not default:
            raise RuntimeError("Cannot call ask with options and no default")

        if not options:
            options_str = self.__getOptionsString(options, default)
            answer = self.__getAnswer(question, options_str)
            return self.__emptyStringToDefault(answer, default)
        else:
            return self.__askWithOptions(question, options, default)


    def __askWithOptions(self, question, options, default):
        options_str = self.__getOptionsString(options, default)

        while True:
            answer = self.__getAnswer(question, options_str)

            validAnswers = [option.lower() for option in options]
            validAnswers.extend(options)
            
            if answer in validAnswers:
                return answer
            elif answer == "":
                return default  

    def __emptyStringToDefault(self, answer, default):
            if answer == "":
                return default
            else:
                return answer

    def __getOptionsString(self, options, default):
            result = []
            optionOpenBracket = "["

            if options:
                result.append("(")
                result.append("|".join(options))
                result.append(")")
                optionOpenBracket = " ["

            if default:
                result.append(optionOpenBracket)
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
            newTokens = list(self.tokens)
            newTokens.append(options)
            return " ".join(newTokens)

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
    "The CLI expected by BatchCli. Should be implemented by subclassing."

    def log(self, message):
        pass

    def ask(self, message):
        pass


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
    engine = TaskEngine(cli)
    engine.addTask(Print("Put oil in the pan"))
    engine.addTask(Print("Turn fire on"))
    engine.addTask(Print("Break the egg"))
    engine.addTask(Print("Put the egg in the pan"))
    engine.addTask(Print("Wait the egg is cooked"))
    engine.addTask(Print("Put the egg in the dish"))
    engine.addTask(Print("Add salt to the egg and eat it!"))
    engine.run()



