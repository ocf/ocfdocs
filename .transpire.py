from pathlib import Path

from transpire.resources import Deployment, Ingress, Service, Secret
from transpire.types import Image
from transpire.utils import get_image_tag

name = "ocfdocs"


def objects():
    dep = Deployment(
        name=name,
        image=get_image_tag("ocfdocs"),
        ports=[15000],
    )

    svc = Service(
        name=name,
        selector=dep.get_selector(),
        port_on_pod=15000,
        port_on_svc=80,
    )
    
    ing = Ingress.from_svc(
        svc=svc,
        # TODO: Define domain name
        host="mkdocs.ocf.berkeley.edu",
        path_prefix="/",
    )

    # TODO: Secrets
    sec = Secret(
        name=name,
        string_data={
            "OUTLINE_API_KEY": "",
        },
    )
    
    yield dep.build()
    yield svc.build()
    yield ing.build()
    yield sec.build()


def images():
    yield Image(name="ocfdocs", path=Path("/"), registry="ghcr")
    
