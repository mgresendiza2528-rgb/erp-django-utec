import mimetypes
from decimal import ROUND_HALF_UP, Decimal
from pathlib import Path
from urllib.parse import unquote, urlparse

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.staticfiles import finders
from django.http import HttpResponse
from django.http.request import validate_host
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from django.utils import timezone

import weasyprint

from configuracion.models import ConfiguracionERP
from ventas.models import Venta


def _ruta_local(url_path: str) -> Path | None:
    """Traduce /static/... o /media/... a un archivo en disco (o None)."""
    static_prefix = "/" + settings.STATIC_URL.lstrip("/")
    media_prefix = "/" + settings.MEDIA_URL.lstrip("/")

    if url_path.startswith(static_prefix):
        relativa = url_path[len(static_prefix):]
        candidata = Path(settings.STATIC_ROOT) / relativa
        if candidata.is_file():
            return candidata
        encontrada = finders.find(relativa)
        return Path(encontrada) if encontrada else None

    if url_path.startswith(media_prefix):
        raiz = Path(settings.MEDIA_ROOT).resolve()
        candidata = (raiz / url_path[len(media_prefix):]).resolve()
        if raiz in candidata.parents and candidata.is_file():
            return candidata
    return None


def _url_fetcher_local(url: str, timeout: int = 10, ssl_context=None):
    """url_fetcher de WeasyPrint que lee /static/ y /media/ desde disco."""
    parsed = urlparse(url)
    if parsed.scheme in ("http", "https", "file"):
        ruta = _ruta_local(unquote(parsed.path))
        if ruta is not None:
            return {
                "string": ruta.read_bytes(),
                "mime_type": mimetypes.guess_type(ruta.name)[0],
                "filename": ruta.name,
            }
        propio = validate_host(
            parsed.hostname or "", ["localhost", "127.0.0.1", *settings.ALLOWED_HOSTS]
        )
        if parsed.scheme == "file" or propio:
            raise FileNotFoundError(url)
    return weasyprint.default_url_fetcher(url, timeout=timeout, ssl_context=ssl_context)


def calcular_totales(subtotal, iva_porcentaje) -> dict:
    """Subtotal, IVA y total con 2 decimales (redondeo comercial)."""
    centavos = Decimal("0.01")
    subtotal = Decimal(subtotal).quantize(centavos, ROUND_HALF_UP)
    iva = (subtotal * Decimal(iva_porcentaje) / 100).quantize(centavos, ROUND_HALF_UP)
    return {"subtotal": subtotal, "iva": iva, "total_con_iva": subtotal + iva}


@login_required
def venta_pdf(request, venta_id: int) -> HttpResponse:
    """Genera y descarga la factura de una venta en PDF (WeasyPrint)."""
    venta = get_object_or_404(
        Venta.objects.select_related("cliente").prefetch_related(
            "detalles__producto__categoria"
        ),
        pk=venta_id,
    )
    config = ConfiguracionERP.get_instance()
    context = {
        "venta": venta,
        "config": config,
        "hoy": timezone.localdate(),
        **calcular_totales(venta.total, config.iva_porcentaje),
    }

    html_string = render_to_string("ventas/factura_pdf.html", context, request=request)

    pdf_bytes = weasyprint.HTML(
        string=html_string,
        base_url=request.build_absolute_uri("/"),
        url_fetcher=_url_fetcher_local,
    ).write_pdf()

    response = HttpResponse(pdf_bytes, content_type="application/pdf")
    response["Content-Disposition"] = (
        f'attachment; filename="factura_{venta.pk:05d}.pdf"'
    )
    return response
from .pdf_views import venta_pdf  # noqa: E402,F811