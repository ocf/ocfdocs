from pathlib import Path

from transpire.resources import Deployment, Ingress, Service, Secret
from transpire.types import Image
from transpire.utils import get_image_tag

name = "ocfdocs"


def objects():
    # Secrets, added through vault
    sec = Secret(
        name=name,
        string_data={
            "OUTLINE_API_KEY": "",
        },
    )
    
    # Deployment
    dep = Deployment(
        name=name,
        image=get_image_tag("ocfdocs"),
        ports=[15000],
    )
    # Export secrets to environment
    dep.pod_spec().with_configmap_env(name).with_secret_env(name)
    
    # Service
    svc = Service(
        name=name,
        selector=dep.get_selector(),
        port_on_pod=15000,
        port_on_svc=80,
    )

    # Ingress
    ing = Ingress(
        service_name=name,
        host="mkdocs.ocf.berkeley.edu",
        service_port=80,
    )
    
    yield dep.build()
    yield svc.build()
    yield ing.build()
    yield sec.build()


def images():
    yield Image(name="ocfdocs", path=Path("/"), registry="ghcr")
    
