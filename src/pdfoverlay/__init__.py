from pypdf import PdfReader, PdfWriter, PageObject, Transformation


mm = 25.4 / 72  # 1mm in points
cm = mm * 10  # 1cm in points


def overlay_page(
    base: PageObject,
    page: PageObject,
    x: float = 0.0,
    y: float = 0.0,
    rotation: int = 0,
    scale: float = 1.0,
    margin: float = 0.0,
    expand: bool = False,
    over: bool = True,
) -> PageObject:
    """Overlay a page onto the base page with optional rotation, scaling, and margin.
    X/Y coordinates are relative to the lower-left corner of pages and in points, where 1 point = 1/72 inch, or 25.4 / 72 mm.

    Parameters
    ==========
    base : PageObject
        The base page onto which the overlay will be applied.
    page : PageObject
        The page to overlay on the base page.
    x : float, optional
        The x-coordinate to place the overlay page (default is 0.0).
    y : float, optional
        The y-coordinate to place the overlay page (default is 0.0).
    rotation : int, optional
        The rotation angle in degrees to apply to the overlay page (default is 0).
        Must be a multiple of 90.
    scale : float, optional
        The scale factor to apply to the overlay page (default is 1.0).
    margin : float, optional
        The margin to apply around the overlay page (default is 0.0).
    expand : bool, optional
        If True, expands the base page to fit the overlay page (default is False).
    over : bool, optional
        If True, overlays the page on top of the base page (default is True).

    Returns
    =======
    PageObject
        The base page with the overlay applied.
    """
    # Rotate and scale the overlay page
    width = page.mediabox.width
    height = page.mediabox.height
    trans = (
        Transformation()
        .translate(-width / 2, -height / 2)
        .rotate(rotation)
        .scale(scale)
        .translate(height / 2, width / 2)
        .translate(x, y)
    )
    page.add_transformation(trans)
    page.mediabox.lower_left = (-margin, -margin)
    page.mediabox.upper_right = (height + margin, width + margin)
    page.cropbox.lower_left = (-margin, -margin)
    page.cropbox.upper_right = (height + margin, width + margin)

    base.merge_page(page, expand=expand, over=over)
    return base


def pdfoverlay(
    in1: str,
    in2: str,
    out: str,
    in1_page: int = 0,
    in2_page: int = 0,
    x: float = 0.0,
    y: float = 0.0,
    rotation: int = 0,
    scale: float = 1.0,
    margin: float = 0.0,
    expand: bool = False,
    over: bool = True,
) -> None:
    """Convenience function to overlay one PDF page onto another.
    
    Parameters
    ==========
    in1 : str
        Path to the base PDF file, or other that PdfReader accepts.
    in2 : str
        Path to the overlay PDF file, or other that PdfReader accepts.
    out : str
        Path to the output PDF file, or other that PdfReader accepts.
    in1_page : int, optional
        Page number in the base PDF to overlay onto (default is 0).
    in2_page : int, optional
        Page number in the overlay PDF to use (default is 0).
    x : float, optional
        X-coordinate for the overlay position (default is 0.0).
    y : float, optional
        Y-coordinate for the overlay position (default is 0.0).
    rotation : int, optional
        Rotation angle in degrees for the overlay page (default is 0).
    scale : float, optional
        Scale factor for the overlay page (default is 1.0).
    margin : float, optional
        Margin around the overlay page (default is 0.0).
    expand : bool, optional
        If True, expands the base page to fit the overlay page (default is False).
    over : bool, optional
        If True, overlays the page on top of the base page (default is True).
    """
    with (
        PdfReader(in1) as base_reader,
        PdfReader(in2) as overlay_reader,
        PdfWriter() as writer
    ):
        base = base_reader.pages[in1_page]
        page = overlay_reader.pages[in2_page]
        new = overlay_page(
            base, page, x, y, rotation, scale, margin, expand, over
        )
        writer.add_page(new)
        writer.write(out)
