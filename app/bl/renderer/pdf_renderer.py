import os
from pathlib import Path

from weasyprint import HTML

from app.bl import util

output_folder = util.read_env_var('OUTPUT_FOLDER')


def render_pdf(html_filename, output_filename):
    output_filepath = get_pdf_output_filename(output_filename)
    Path(os.path.dirname(output_filepath)).mkdir(parents=True, exist_ok=True)
    HTML(html_filename).write_pdf(output_filepath)
    return output_filepath


def get_pdf_output_filename(output_filename):
    return os.path.join(output_folder, output_filename)
