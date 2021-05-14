import os
import platform
import subprocess

import pdfkit


def _get_pdfkit_config():
    """wkhtmltopdf lives and functions differently depending on Windows or Linux. We
     need to support both since we develop on windows but deploy on Heroku.

    Returns:
        A pdfkit configuration
    """
    if platform.system() == 'Windows':
        return pdfkit.configuration(
            wkhtmltopdf=os.environ.get('WKHTMLTOPDF_BINARY', 'C:\\Program Files\\wkhtmltopdf\\bin\\wkhtmltopdf.exe'))
    else:
        WKHTMLTOPDF_CMD = subprocess.Popen(['which', os.environ.get('WKHTMLTOPDF_BINARY', 'wkhtmltopdf')],
                                           stdout=subprocess.PIPE).communicate()[0].strip()
        return pdfkit.configuration(wkhtmltopdf=WKHTMLTOPDF_CMD)

def make_pdf_from_url(url, options=None):
    """Produces a pdf from a website's url.
    Args:
        url (str): A valid url
        options (dict, optional): for specifying pdf parameters like landscape
            mode and margins
    Returns:
        pdf of the website
    """
    return pdfkit.from_url(url, False, configuration=_get_pdfkit_config(), options=options)

def make_pdf_from_raw_html(html, options=None):
    """Produces a pdf from raw html.
    Args:
        html (str): Valid html
        options (dict, optional): for specifying pdf parameters like landscape
            mode and margins
    Returns:
        pdf of the supplied html
    """
    return pdfkit.from_string(html, False, configuration=_get_pdfkit_config(), options=options)