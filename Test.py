import unittest
from batchcli import BatchCli, Cli, TaskEngine, Task


class BatchCliTest(unittest.TestCase):

    def setUp(self):
    	self.cli = FakeCli()
    	self.c = BatchCli(2, self.cli)


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
        self.c = BatchCli(2, self.cli)
        self.e = TaskEngine(self.c)

    def test_can_add_tasks(self):
        self.e.addTask(Task("T1"))
        self.e.addTask(Task("T2"))

    def test_run(self):
        self.e.addTask(Task("T1"))
        self.e.addTask(Task("T2"))
        self.e.run()

class FakeCli(Cli):

	def __init__(self):
		self.countAsk = 0
		self.predefinedAnswer = []

	def log(self, message):
		self.latestMessage = message
		
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


if __name__ == "__main__":
	unittest.main()
