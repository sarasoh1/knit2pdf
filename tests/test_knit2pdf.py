from knit2pdf.knit2pdf import Knit2PDF
from knit2pdf.config.knit2pdfoptions import Knit2PDFOptions

class TestKnit2PDF:
    def test_knit2pdf(self):
        cli = Knit2PDF(
            youtube_link="https://www.youtube.com/watch?v=8FVqflG1INo",
            video_language="en",
            dl_options=Knit2PDFOptions()
            )
        assert cli.youtube_link == "https://www.youtube.com/watch?v=8FVqflG1INo"
        assert cli.youtube_id == "8FVqflG1INo"
        assert cli.video_language == "en"