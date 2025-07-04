"pdfoverlay"
from pypdf import PdfReader, PdfWriter, PageObject, Transformation
from pint import UnitRegistry, Quantity

_ureg = UnitRegistry()
mm = _ureg.mm
cm = _ureg.cm
inch = _ureg.inch
pt = _ureg.point


def overlay_page(
    base: PageObject,
    page: PageObject,
    x: float | Quantity = 0.0,
    y: float | Quantity = 0.0,
    rotation: int = 0,
    scale: float = 1.0,
    margin_left: float | Quantity = 0.0,
    margin_right: float | Quantity = 0.0,
    margin_bottom: float | Quantity = 0.0,
    margin_top: float | Quantity = 0.0,
    expand: bool = False,
    over: bool = True,
) -> PageObject:
    """Overlay a page onto the base page with optional rotation, scaling, and margin.
    X/Y coordinates are relative to the lower-left corner of pages and in points.

    Parameters
    ==========
    base : PageObject
        The base page onto which the overlay will be applied.
    page : PageObject
        The page to overlay on the base page.
    x : float | Quantity, optional
        The x-coordinate to place the overlay page (default is 0.0).
    y : float | Quantity, optional
        The y-coordinate to place the overlay page (default is 0.0).
    rotation : int, optional
        The rotation angle in degrees to apply to the overlay page (default is 0).
        Must be a multiple of 90.
    scale : float, optional
        The scale factor to apply to the overlay page (default is 1.0).
    margin_left : float | Quantity, optional
        The left margin to apply around the overlay page (default is 0.0).
    margin_right : float | Quantity, optional
        The right margin to apply around the overlay page (default is 0.0).
    margin_bottom : float | Quantity, optional
        The bottom margin to apply around the overlay page (default is 0.0).
    margin_top : float | Quantity, optional
        The top margin to apply around the overlay page (default is 0.0).
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
    if isinstance(x, Quantity):
        x = x.to(pt).magnitude
    if isinstance(y, Quantity):
        y = y.to(pt).magnitude
    if isinstance(margin_left, Quantity):
        margin_left = margin_left.to(pt).magnitude
    if isinstance(margin_right, Quantity):
        margin_right = margin_right.to(pt).magnitude
    if isinstance(margin_bottom, Quantity):
        margin_bottom = margin_bottom.to(pt).magnitude
    if isinstance(margin_top, Quantity):
        margin_top = margin_top.to(pt).magnitude
    trans = (
        Transformation()
        .translate(-width / 2, -height / 2)
        .rotate(rotation)
        .scale(scale)
        .translate(height / 2, width / 2)
        .translate(x, y)
    )
    page.add_transformation(trans)
    page.mediabox.lower_left = (-margin_left, -margin_bottom)
    page.mediabox.upper_right = (height + margin_top, width + margin_right)
    page.cropbox.lower_left = (-margin_left, -margin_bottom)
    page.cropbox.upper_right = (height + margin_top, width + margin_right)

    base.merge_page(page, expand=expand, over=over)
    return base


def pdfoverlay(
    in1: str,
    in2: str,
    out: str,
    in1_page: int = 0,
    in2_page: int = 0,
    x: float | Quantity = 0.0,
    y: float | Quantity = 0.0,
    rotation: int = 0,
    scale: float = 1.0,
    margin_left: float | Quantity = 0.0,
    margin_right: float | Quantity = 0.0,
    margin_bottom: float | Quantity = 0.0,
    margin_top: float | Quantity = 0.0,
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
    x : float | Quantity, optional
        X-coordinate for the overlay position (default is 0.0).
    y : float | Quantity, optional
        Y-coordinate for the overlay position (default is 0.0).
    rotation : int, optional
        Rotation angle in degrees for the overlay page (default is 0).
    scale : float, optional
        Scale factor for the overlay page (default is 1.0).
    margin_left : float | Quantity, optional
        The left margin to apply around the overlay page (default is 0.0).
    margin_right : float | Quantity, optional
        The right margin to apply around the overlay page (default is 0.0).
    margin_bottom : float | Quantity, optional
        The bottom margin to apply around the overlay page (default is 0.0).
    margin_top : float | Quantity, optional
        The top margin to apply around the overlay page (default is 0.0).
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
            base, page, x, y, rotation, scale,
            margin_left, margin_right, margin_bottom, margin_top,
            expand, over
        )
        writer.add_page(new)
        writer.write(out)
