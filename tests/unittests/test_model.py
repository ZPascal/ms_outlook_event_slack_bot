from unittest import TestCase
from unittest.mock import MagicMock, patch

from grafana_api.model import (
    APIModel,
    FindAnnotationObject,
    AnnotationObject,
    AnnotationGraphiteObject,
)
from grafana_api.annotations import Annotations


class AnnotationsTestCase(TestCase):