This small library provide an easy way to run some tasks in batch and track progress on the CLI.

An example of output you can get is the following::

    [ 1/6 ] Put oil in the pan
    [ ... ] ...
    [ 2/6 ] Turn fire on
    [ ... ] ...
    [ 3/6 ] Cooking the eggs
    [  ?  ] How many eggs? (1|2|3) [1] 2
    [ ... ] Break the eggs ...
    [ ... ] Throw the eggshell ...
    [ ... ] Put the eggs into the pan ...
    [ 4/6 ] Wait the eggs is cooked
    [ ... ] ...
    [ 5/6 ] Put the egg in the dish
    [ ... ] ...
    [ 6/6 ] Add salt to the egg and eat it!
    [ ... ] ...


The module provide an api to define tasks and add them to a task engine::

    cli = SimpleCli()
    engine = TaskEngine(cli)

    engine.addTask(Print("Put oil in the pan"))
    engine.addTask(Print("Turn fire on"))
    engine.addTask(CookingEggs("Cooking the eggs"))
    engine.addTask(Print("Wait the eggs is cooked"))
    engine.addTask(Print("Put the egg in the dish"))
    engine.addTask(Print("Add salt to the egg and eat it!"))

    engine.run()

In the example above Print is a class extending Task (defined in the module)::

     class Print(Task):
        "Simple Task: do nothing more than printing ..."

        def run(self, cli):
            cli.newMessage

The same for CookingEggs that is able to ask an input to the user::

    class CookingEggs(Task):
        "Simple Task: do nothing more than printing ..."

        def run(self, cli):
            eggs = cli.ask("How many eggs?", ["1", "2", "3"], "1")
            cli.newMessage("Break the eggs ...")
            cli.newMessage("Throw the eggshell ...")
            cli.newMessage("Put the eggs into the pan ...")

In case a task fails the task engine stops immediately and return from the method run.
