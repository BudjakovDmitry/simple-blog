from pathlib import Path

from django.core.management.base import BaseCommand
import markdown

from blog.models import Article


MARKDOWN_EXTENSIONS = [
    "extra",
    "fenced_code",
    "codehilite",
    "toc",
]

MARKDOWN_EXTENSION_CONFIG = {
    "codehilite": {
        "guess_lang": False,
        "use_pygments": True,
        "noclasses": False,  # use CSS-classes rather than inline-styles
    },
    "toc": {
        "permalink": True,
    },
}


def render_markdown(text: str):
    return markdown.markdown(
        text,
        extensions=MARKDOWN_EXTENSIONS,
        extension_configs=MARKDOWN_EXTENSION_CONFIG,
        output_format="html5",
    )


class Command(BaseCommand):
    help = "Upload md article, and convert it to html"

    def add_arguments(self, parser):
        parser.add_argument("article_path", type=str)

    def handle(self, *args, **options):
        article_md = Path(options["article_path"])
        if not article_md.exists():
            self.stderr.write(f"can't find file {article_md}")
            return

        md_text = article_md.read_text()
        html_text = render_markdown(md_text)
        
        # Index where lead ends
        lead_end_index = html_text.find("</p>")

        article = Article(
            title=article_md.stem,
            lead=html_text[:lead_end_index],
            origin_text=md_text,
            formatted_text=html_text,
        )

        article.save()
        self.stdout.write("Uploaded successfully!")
