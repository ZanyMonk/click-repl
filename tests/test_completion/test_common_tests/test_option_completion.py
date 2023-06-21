import click
from click_repl import ClickCompleter
from prompt_toolkit.document import Document


@click.group()
def root_command():
    pass


c = ClickCompleter(root_command, click.Context(root_command))


def test_option_choices():
    @root_command.command()
    @click.option("--handler", type=click.Choice(("foo", "bar")))
    def option_choices(handler):
        pass

    completions = list(c.get_completions(Document("option-choices --handler ")))
    assert {x.text for x in completions} == {"foo", "bar"}


def test_boolean_option():
    @root_command.command()
    @click.option("--foo", type=click.BOOL)
    def bool_option(foo):
        pass

    completions = list(c.get_completions(Document("bool-option --foo ")))
    assert {x.text for x in completions} == {"true", "false"}

    completions = list(c.get_completions(Document("bool-option --foo t")))
    assert {x.text for x in completions} == {"true"}


def test_shortest_only_mode():
    @root_command.command()
    @click.option("--foo", "-f", is_flag=True)
    @click.option("-b", "--bar", is_flag=True)
    @click.option("--foobar", is_flag=True)
    def shortest_only(foo, bar, foobar):
        pass

    c.shortest_only = True

    completions = list(c.get_completions(Document("shortest-only ")))
    assert {x.text for x in completions} == {"-f", "-b", "--foobar"}

    completions = list(c.get_completions(Document("shortest-only -")))
    assert {x.text for x in completions} == {"-f", "--foo", "-b", "--bar", "--foobar"}

    completions = list(c.get_completions(Document("shortest-only --f")))
    assert {x.text for x in completions} == {"--foo", "--foobar"}

    c.shortest_only = False

    completions = list(c.get_completions(Document("shortest-only ")))
    assert {x.text for x in completions} == {"-f", "--foo", "-b", "--bar", "--foobar"}
