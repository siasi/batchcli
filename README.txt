This small library provide an easy way to run some tasks in batch and track progress on the CLI.

An example of output you can get is the following::

	[ 1/7 ] Put oil in the pan
	[ ... ] ...
	[ 2/7 ] Turn fire on
	[ ... ] ...
	[ 3/7 ] Break the egg
	[ ... ] ...
	[ 4/7 ] Put the egg in the pan
	[ ... ] ...
	[ 5/7 ] Wait the egg is cooked
	[ ... ] ...
	[ 6/7 ] Put the egg in the dish
	[ ... ] ...
	[ 7/7 ] Add salt to the egg and eat it!
	[ ... ] ...

The module provide an api to define tasks and add them to a task engine::

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

In the example above Print is a class extending Task (defined in the module)::

     class Print(Task):
        "Simple Task: do nothing more than printing ..."

        def run(self, cli):
            cli.newMessage

In case a task fails the task engine stops immediately and return from the method run.
