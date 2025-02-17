from pathlib import Path

from transpire.resources import Deployment, Ingress, Service
from transpire.types import Image
from transpire.utils import get_image_tag

name = "ocfdocs"


def objects():
    dep = Deployment(
        name="ocfdocs",
        image=get_image_tag("ocfdocs"),
        ports=[15000],
    )

    svc = Service(
        name="ocfdocs",
        selector=dep.get_selector(),
        port_on_pod=15000,
        port_on_svc=80,
    )
    
    ing = Ingress(
        svc=svc,
        # TODO: Define domain name
        host="//mkdocs.ocf.berkeley.edu",
        path_prefix="/",
    )

    # TODO: Secrets
    
    yield dep.build()
    yield svc.build()
    yield ing.build()


def images():
    yield Image(name="ocfdocs", path=Path("/"), registry="ghrc")
    
