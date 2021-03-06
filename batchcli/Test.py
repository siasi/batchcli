import unittest
from batchcli import BatchCli, Cli, TaskEngine, Task


class BatchCliTest(unittest.TestCase):

    def setUp(self):
    	self.cli = FakeCli()
    	self.c = BatchCli(self.cli)
        self.c.expectTaskCount(2)

    def test_ask(self):
    	self.cli.pleaseAnswer("an answer")
    	answer = self.c.ask("A question")
    	
    	self.assertEquals(self.cli.latestMessage, "[  ?  ] A question")
    	self.assertEquals(answer, "an answer")

    def test_newMessage(self):
    	self.c.newMessage("Message1")
    	
    	self.assertEquals(self.cli.latestMessage, "[ ... ] Message1")
    	self.c.newMessage("Message2")
    	self.assertEquals(self.cli.latestMessage, "[ ... ] Message2")

    def test_taskNewTask(self):
    	self.c.newTask("Task 1")
    	self.assertEquals(self.cli.latestMessage, "[ 1/2 ] Task 1")
    	
    	self.c.newTask("Task 2")
    	self.assertEquals(self.cli.latestMessage, "[ 2/2 ] Task 2")

    def test_cannotExceedTaskCount(self):
    	with self.assertRaises(RuntimeError):
    	    self.c.newTask("Task 1")
    	    self.c.newTask("Task 2")
    	    self.c.newTask("Task 3")

    def test_confirm_ouput(self):
    	self.cli.pleaseAnswer("Y")
    	self.c.confirm("Can you confirm?")
    	self.assertEquals(self.cli.latestMessage, "[  ?  ] Can you confirm? (Y|N) [Y]")

    def test_confirm_when_user_answer_Y(self):
    	self.cli.pleaseAnswer("Y")
    	answer = self.c.confirm("any question")
    	self.assertTrue(answer)

    	self.cli.pleaseAnswer("y")
    	answer = self.c.confirm("any question")
    	self.assertTrue(answer)

    	self.cli.pleaseAnswer("\n")
    	answer = self.c.confirm("any question")
    	self.assertTrue(answer)

    def test_confirm_when_user_answer_N(self):
    	self.cli.pleaseAnswer("N")
    	answer = self.c.confirm("any question")
    	self.assertFalse(answer)

    	self.cli.pleaseAnswer("n")
    	answer = self.c.confirm("any question")
    	self.assertFalse(answer)

    def test_confirm_when_user_answer_wrong(self):
        self.cli.pleaseAnswer("an unexpected answer", "Y")

        answer = self.c.confirm("any question")
        self.assertEquals(2, self.cli.countAsk)
        self.assertTrue(answer)

    def test_select(self):
        values = ['v1', 'v2', 'v3']
        self.cli.pleaseAnswer("v1")
        answer = self.c.select("Please enter Origin or (L)ist possible values:", values)

        self.assertEquals(self.cli.latestMessage, "[  ?  ] Please enter Origin or (L)ist possible values: [v1]")
        self.assertEquals('v1', answer)

    def test_choose(self):
        values = ['v1', 'v2', 'v3']
        self.cli.pleaseAnswer("2")
        answer = self.c.choose("Please select Origin:", values)

        self.assertEquals(self.cli.latestMessage, "[  ?  ] Please select Origin: [v1]")
        self.assertEquals('v2', answer)

    def test_select_when_not_valid_value_is_returned(self):
        values = ['v1', 'v2', 'v3']
        self.cli.pleaseAnswer("bad value", "v1")
        answer = self.c.select("Please enter Origin or (L)ist possible values:", values)

        self.assertEquals(self.cli.latestMessage, "[  ?  ] Please enter Origin or (L)ist possible values: [v1]")
        self.assertEquals('v1', answer)

    def test_select_print_all_values(self):
        values = ['v1', 'v2', 'v3']
        self.cli.pleaseAnswer('L', 'v1')
        self.cli.expect(['[  -  ]   v1', '[  -  ]   v2', '[  -  ]   v3'])
        answer = self.c.select("Please select Origin:", values)

        self.cli.verify()

    def test_choose_print_all_values(self):
        values = ['v1', 'v2', 'v3']
        self.cli.pleaseAnswer('L', '2')
        self.cli.expect(['[  -  ]   1. v1', '[  -  ]   2. v2', '[  -  ]   3. v3'])
        answer = self.c.choose("Please choose Origin or (L)ist possible values:", values)

        self.cli.verify()


    def test_ask_when_user_aswer_right(self):
        self.cli.pleaseAnswer("E")
        answer = self.c.ask("Do you want to (C)ontinue, (S)kip or (E)xit?", ['C','S','E'], 'E')
        self.assertEquals(self.cli.latestMessage, "[  ?  ] Do you want to (C)ontinue, (S)kip or (E)xit? (C|S|E) [E]")
        self.assertEquals('E', answer)
		
        self.cli.pleaseAnswer("c")
        answer = self.c.ask("Do you want?", ['C','S','E'], 'E')
        self.assertEquals('c', answer)

        self.cli.pleaseAnswer("\n")
        answer = self.c.ask("Do you want?", ['C','S','E'], 'E')
        self.assertEquals('E', answer)

    def test_ask_when_user_answer_wrong(self):
        self.cli.pleaseAnswer("an unexpected answer", "s")

        answer = self.c.ask("Do you want to (C)ontinue, (S)kip or (E)xit?", ['C','S','E'], 'E')
        self.assertEquals(2, self.cli.countAsk)
        self.assertEquals('s', answer)

    def test_ask_with_no_options_and_default(self):
        self.cli.pleaseAnswer("\n")
        answer = self.c.ask("Which colour?", default='Yellow')
        self.assertEquals("[  ?  ] Which colour? [Yellow]", self.cli.latestMessage,)
        self.assertEquals('Yellow', answer)

    def test_multiple_ask(self):
        self.cli.pleaseAnswer("\n")
        answer = self.c.ask("Which colour?", default='Yellow')
        self.assertEquals("[  ?  ] Which colour? [Yellow]", self.cli.latestMessage,)
        self.assertEquals('Yellow', answer)

        self.cli.pleaseAnswer("\n")
        answer = self.c.ask("Which size?", default='Medium')
        self.assertEquals("[  ?  ] Which size? [Medium]", self.cli.latestMessage,)
        self.assertEquals('Medium', answer)

        self.cli.pleaseAnswer("\n")
        answer = self.c.ask("Which shape?", default='Long')
        self.assertEquals("[  ?  ] Which shape? [Long]", self.cli.latestMessage,)
        self.assertEquals('Long', answer)

    def test_cannot_pass_suggest_but_default(self):
        with self.assertRaises(RuntimeError):
            self.c.ask("question without default", ['A','B'])

    def test_negate_ouput(self):
        self.cli.pleaseAnswer("N")
        self.c.negate("Can you confirm?")
        self.assertEquals(self.cli.latestMessage, "[  ?  ] Can you confirm? (Y|N) [N]")

    def test_negate_when_user_answer_N(self):
        self.cli.pleaseAnswer("N")
        answer = self.c.negate("any question")
        self.assertTrue(answer)

        self.cli.pleaseAnswer("n")
        answer = self.c.negate("any question")
        self.assertTrue(answer)

        self.cli.pleaseAnswer("\n")
        answer = self.c.negate("any question")
        self.assertTrue(answer)

    def test_negate_when_user_answer_Y(self):
        self.cli.pleaseAnswer("Y")
        answer = self.c.negate("any question")
        self.assertFalse(answer)

        self.cli.pleaseAnswer("y")
        answer = self.c.negate("any question")
        self.assertFalse(answer)

    def test_negate_when_user_answer_wrong(self):
        self.cli.pleaseAnswer("an unexpected answer", "N")

        answer = self.c.negate("any question")
        self.assertEquals(2, self.cli.countAsk)
        self.assertTrue(answer)



class TaskEngineTest(unittest.TestCase):

    def setUp(self):
        self.cli = FakeCli()
        self.e = TaskEngine(self.cli)

    def test_can_add_tasks(self):
        self.e.addTask(Task("T1"))
        self.e.addTask(Task("T2"))

    def test_run(self):
        self.e.addTask(Task("T1"))
        self.e.addTask(Task("T2"))
        self.e.run()

    def test_failure(self):


        task1 = MockTask("T1")
        failingTask = MockTask("T2")
        failingTask.failed = True
        task3 = MockTask("T3")

        self.e.addTask(task1)
        self.e.addTask(failingTask)

        self.e.run()

        self.assertTrue(task1.executed)
        self.assertTrue(failingTask.executed)
        self.assertFalse(task3.executed)

    def test_addTask_count_tasks(self):
       
        self.e.addTask(MockTask("T1"))
        self.e.addTask(MockTask("T2"))
        self.e.addTask(MockTask("T3"))

        self.assertEquals(3, self.e.taskToRun())

class MockTask(Task):

    def __init__(self, name):
        Task.__init__(self, name)
        self.executed = False

    def run(self, cli):
        self.executed = True

class FakeCli(Cli):

    def __init__(self):
        self.countAsk = 0
        self.predefinedAnswer = []
        self.expectedMessages = []
        self.messages = []
        self.latestMessage = ""

    def log(self, message):
        self.latestMessage = message
        self.messages.append(message)
		
    def ask(self, message):
        self.latestMessage = message
        return self.__getAnswer()

    def __getAnswer(self):
        answer = self.predefinedAnswer[self.countAsk]
        self.countAsk = self.countAsk + 1
        return answer

    def pleaseAnswer(self, *answer):
        self.countAsk = 0
        self.predefinedAnswer = list(answer)

    def expect(self, messages):
        self.expectedMessages = messages

    def verify(self):
        if self.expectedMessages:
            if not self.expectedMessages == self.messages:
                raise AssertionError('Expected message "' + str(self.expectedMessages) + '" in sequence, but was "'  + str(self.messages) + '"')

class FakeBatchCli(Cli):

    def __init__(self):
        self.countAsk = 0
        self.countLog = 0
        self.predefinedAnswer = []
        self.expectedMessages = []
        self.messages = []
        self.latestMessage = ""


    def newMessage(self, message):
        self.latestMessage = message
        self.messages.append(message)

    def ask(self, message, default=None):
        self.latestMessage = message
        self.messages.append(message)
        return self.__getAnswer()

    def negate(self, message, default=None):
        self.latestMessage = message
        return False

    def __getAnswer(self):
        if self.countAsk not in range(0, len(self.predefinedAnswer)):
            raise AssertionError("Unexpected call to ask method!")
        answer = self.predefinedAnswer[self.countAsk]
        self.countAsk = self.countAsk + 1
        return answer

    def pleaseAnswer(self, *answer):
        self.countAsk = 0
        self.predefinedAnswer = list(answer)


if __name__ == "__main__":
	unittest.main()
