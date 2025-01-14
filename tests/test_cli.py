from click.testing import CliRunner
from knit2pdf.cli import cli

class TestKnit2PDFCli:
    def test_cli(self):
        runner = CliRunner()
        result = runner.invoke(cli, ["https://www.youtube.com/watch?v=8FVqflG1INo"])
        assert result.exit_code == 0