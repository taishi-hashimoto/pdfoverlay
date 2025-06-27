from pathlib import Path

HERE = Path(__file__).parent
BASE_FILE = HERE / "base.pdf"
LEGEND_FILE = HERE / "legend.pdf"


def prepare_test_files():
    "Write base and legend files for testing."
    import numpy as np
    import matplotlib.pyplot as plt
    from matplotlib.colors import Normalize
    from matplotlib.colorbar import ColorbarBase
    # Base file.
    fig, (_cax, ax) = plt.subplots(1, 2, figsize=(10, 5), gridspec_kw={"width_ratios": [1, 9]})
    _cax.remove()
    ax.pcolormesh(np.random.rand(10, 10), vmin=0, vmax=1)
    fig.tight_layout()
    fig.savefig(BASE_FILE)
    # Legend file.
    fig, cax = plt.subplots(figsize=(5, 1))
    ColorbarBase(cax, norm=Normalize(0, 1), orientation='horizontal')
    fig.tight_layout()
    fig.savefig(LEGEND_FILE)


def test_overlay_page():
    """Test that the overlay function works correctly."""
    from pypdf import PdfReader, PdfWriter
    from pdfoverlay import overlay_page, mm

    prepare_test_files()

    reader = PdfReader(LEGEND_FILE)
    base_reader = PdfReader(BASE_FILE)

    base_page = base_reader.pages[0]
    legend_page = reader.pages[0]

    # Overlay the legend page onto the base page
    result_page = overlay_page(
        base_page, legend_page,
        x=3*mm, y=2.5*mm,
        rotation=-90, scale=1.0,
        margin_left=0.0, margin_right=0.0, margin_top=0.0, margin_bottom=0.0,
        expand=True, over=True)

    # Write out the result.
    output_path = HERE / "overlay_output.pdf"
    with open(output_path, "wb") as output_file:
        writer = PdfWriter()
        writer.add_page(result_page)
        writer.write(output_file)


def test_pdfoverlay():
    """Test the command line interface for pdfoverlay."""
    from pdfoverlay import pdfoverlay, mm

    prepare_test_files()

    output_path = HERE / "overlay_output_pdfoverlay.pdf"

    # Run the CLI function
    pdfoverlay(
        in1=str(BASE_FILE),
        in2=str(LEGEND_FILE),
        out=str(output_path),
        x=3*mm, y=2.5*mm,
        rotation=-90, scale=1.0, expand=True, over=True
    )
